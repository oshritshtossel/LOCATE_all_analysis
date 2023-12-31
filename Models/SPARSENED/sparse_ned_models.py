import torch
import torch.nn as nn
import numpy as np
from Models.SPARSENED.sparse_ned_L0_regularization.models import L0MLP
from Models.SPARSENED.sparse_ned_utils import idx2onehot

def make_mlp(type, dim_list, activation=None, batch_norm=True, dropout=0, N=200):
    layers = []
    if type is None:
        for dim_in, dim_out in zip(dim_list[:-1], dim_list[1:]):
            layers.append(nn.Linear(dim_in, dim_out))
            if batch_norm:
                layers.append(nn.BatchNorm1d(dim_out))

            if activation == 'relu':
                layers.append(nn.ReLU())
            elif activation == 'leakyrelu':
                layers.append(nn.LeakyReLU())
            elif activation == 'tanh':
                layers.append(nn.Tanh())
            elif activation == 'sigmoid':
                layers.append(nn.Sigmoid())
            elif activation in [None,'None']:
                pass
            else:
                assert 0,"Unknown activation %s"%activation
            if dropout > 0:
                layers.append(nn.Dropout(p=dropout))
        return nn.Sequential(*layers)
    elif type in ["L0"]:
        l0mlp = L0MLP(dim_list[0], dim_list[-1], layer_dims=dim_list[1:-1],N=N)
        return l0mlp
    else:
        assert 0, "unknown mlp type=%s"%type


class VAE(nn.Module):

    def __init__(self, encoder_layer_sizes, latent_size, decoder_layer_sizes,
                 conditional=False, num_labels=0):

        super().__init__()

        if conditional:
            assert num_labels > 0

        assert type(encoder_layer_sizes) == list
        assert type(latent_size) == int
        assert type(decoder_layer_sizes) == list

        self.latent_size = latent_size

        self.encoder = Encoder(
            encoder_layer_sizes, latent_size, conditional, num_labels)
        self.decoder = Decoder(
            decoder_layer_sizes, latent_size, conditional, num_labels)

    def forward(self, x, c=None):

        if x.dim() > 2:
            x = x.view(-1, 28*28)

        batch_size = x.size(0)

        means, log_var = self.encoder(x, c)

        std = torch.exp(0.5 * log_var)
        eps = torch.randn([batch_size, self.latent_size]).cuda()
        z = eps * std + means

        recon_x = self.decoder(z, c)

        return recon_x, z, means, log_var

    def inference(self, n=1, c=None):

        batch_size = n
        z = torch.randn([batch_size, self.latent_size]).cuda()

        recon_x = self.decoder(z, c)

        return recon_x

class AE(nn.Module):

    def __init__(self, encoder_layer_sizes, latent_size,decoder_layer_sizes, activation, batch_norm, dropout,
                 mlp_type = None, conditional=False, num_labels=0):

        super().__init__()

        if conditional:
            assert num_labels > 0

        assert type(encoder_layer_sizes) == list
        assert type(latent_size) == int
        assert type(decoder_layer_sizes) == list

        self.latent_size = latent_size

        encoder_activation = activation.split("_")[0]
        decoder_activation = activation.split("_")[1]
        self.encoder = Encoder(
            encoder_layer_sizes, latent_size, encoder_activation, batch_norm, dropout, conditional, num_labels, mlp_type=mlp_type)
        self.decoder = Decoder(
            decoder_layer_sizes, latent_size, decoder_activation, batch_norm, dropout, conditional, num_labels, mlp_type=mlp_type)

    def forward(self, x, c=None):
        if x.dim() > 2:
            x = x.view(-1, 28*28)
        z = self.encoder(x, c)
        recon_x = self.decoder(z, c)
        return recon_x,  z, None, None

    def inference(self, n=1, c=None):
        batch_size = n
        z = torch.randn([batch_size, self.latent_size]).cuda()
        recon_x = self.decoder(z, c)
        return recon_x

    def param_l0(self):
        return {"Encoder":self.encoder.param_l0(),
                "Decoder":self.decoder.param_l0(),}

    def regularization(self):
        #NOTE: Weighting encoder/decoder here
        return self.encoder.regularization() + self.decoder.regularization()

    def get_influence_matrix(self):
        return np.multiply(self.encoder.get_influence_matrix(),self.decoder.get_influence_matrix())

class MLPerceptron(nn.Module):
    def __init__(self, layer_sizes, activation, batch_norm, dropout, mlp_type=None):
        super().__init__()
        self.mlp_type = mlp_type
        self.layer_sizes = layer_sizes
        self.MLP = make_mlp(
                mlp_type,
                layer_sizes,
                activation=activation,
                batch_norm=batch_norm,
                dropout=dropout,
            )
    def forward(self, x, c=None):
        return self.MLP(x)

    def param_l0(self):
        #Count all non-zeros param
        nonzero_count = 0
        for layer in self.modules():
            if isinstance(layer, nn.Conv2d) or isinstance(layer, nn.Linear):
                nonzero_count +=(layer.weight!=0.0).sum().item()
        return nonzero_count

class Encoder(nn.Module):

    def __init__(self, layer_sizes, latent_size, activation, batch_norm, dropout,  conditional, num_labels, mlp_type=None):

        super().__init__()
        self.mlp_type = mlp_type
        self.latent_size = latent_size
        self.layer_sizes = layer_sizes
        self.conditional = conditional
        if self.conditional:
            layer_sizes[0] += num_labels

        self.MLP = make_mlp(
                mlp_type,
                layer_sizes+[latent_size],
                activation=activation,
                batch_norm=batch_norm,
                dropout=dropout,
            )
    def forward(self, x, c=None):

        if self.conditional:
            c = idx2onehot(c, n=10)
            x = torch.cat((x, c), dim=-1)

        z = self.MLP(x)

        return z

    def param_l0(self):
        if self.mlp_type == "L0":
            return self.MLP.get_exp_flops_l0()[1]
        else:
            #Count all non-zeros param
            nonzero_count = 0
            for layer in self.modules():
                if isinstance(layer, nn.Conv2d) or isinstance(layer, nn.Linear):
                    nonzero_count +=(layer.weight!=0.0).sum().item()
            return nonzero_count
    def regularization(self):
        return self.MLP.regularization()

    def get_influence_matrix(self):
        """
        :return: binary matrix showing influence of input to output
        """
        m = None
        for layer in self.modules():
            if isinstance(layer, nn.Linear):
                if m is None:
                    m = np.find(layer.weight)
                else:
                    m = m* np.find(layer.weight)
        return m

class Decoder(nn.Module):

    def __init__(self, layer_sizes,latent_size, activation ,batch_norm, dropout, conditional, num_labels, mlp_type=None):

        super().__init__()
        self.mlp_type = mlp_type
        self.latent_size = latent_size
        self.layer_sizes = layer_sizes
        self.MLP = nn.Sequential()

        self.conditional = conditional
        if self.conditional:
            input_size = latent_size + num_labels
        else:
            input_size = latent_size

        self.MLP = make_mlp(
                mlp_type,
                [latent_size]+layer_sizes,
                activation=activation,
                batch_norm=batch_norm,
                dropout=dropout
            )

    def forward(self, z, c=None):

        if self.conditional:
            c = idx2onehot(c, n=10).cuda()
            z = torch.cat((z, c), dim=-1)

        x = self.MLP(z)

        return x

    def param_l0(self):
        if self.mlp_type == "L0":
            return self.MLP.get_exp_flops_l0()[1]
        else:
            #Count all non-zeros param
            nonzero_count = 0
            for layer in self.modules():
                if isinstance(layer, nn.Conv2d) or isinstance(layer, nn.Linear):
                    nonzero_count +=(layer.weight!=0.0).sum().item()
            return nonzero_count

    def regularization(self):
        return self.MLP.regularization()

    def get_influence_matrix(self):
        """
        :return: binary matrix showing influence of input to output
        """
        m = None
        for layer in self.modules():
            if isinstance(layer, nn.Linear):
                if m is None:
                    m = np.find(layer.weight)
                else:
                    m = m* np.find(layer.weight)
        return m