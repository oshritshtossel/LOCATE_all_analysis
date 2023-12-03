# LOCATE - overall analysis code including statistical analysis, comparisons, and visualizations

This code is attached to the paper "Gut microbiome-metabolome interactions predict host condition". We propose **LOCATE (Latent variables Of miCrobiome And meTabolites rElations)**
a machine learning tool to predict the metabolite concentration from the microbiome composition and produce a latent representation of the interaction. This representation is then used to predict the host condition.

LOCATE's accuracy in predicting the metabolome is higher than all current predictors. The metabolite concentration prediction accuracy significantly decreases cross datasets, and cross conditions, especially in 16S data.

LOCATE’s latent representation predicts the host condition better than either microbiome or the metabolome. This representation is strongly correlated with host demographics. A significant improvement in accuracy (0.793 vs. 0.724 average accuracy) is obtained even with a small number of metabolite samples ($\sim 50$).

## How to apply LOCATE

LOCATE's code is available at a separate [GitHub](https://github.com/oshritshtossel/LOCATE/) as well as a [PyPi](https://pypi.org/project/LOCATE-model/).

## Comparison to other existing state-of-the-art models
During our work, we compared our results to other state-of-the-art models in the field. 
All the models' codes are available in the **Models** directory.

### INTEGRATED-LEARNER

1. "integrated_learner_preprocess.py" - Apply all the preprocessing needed to the microbiome datasets as well as the metabolites datasets according to the [Integrated-Learner paper](https://doi.org/10.1101/2022.11.06.514786).
2. The implementation of the model (in R) over the datasets tested in the manuscript is available in [Google Colab](https://colab.research.google.com/drive/1MFsncDnYAux05xdIuhNDxpZMSQGPRR9X).

### MELONNPAN
1. "melonnpan_condition.py" - Adjust the condition (phenotype) of each dataset to the prediction task.
2. "melonnpan_preprocess.py" - Apply all the preprocessing needed to the microbiome datasets as well as the metabolites datasets according to the [MelonnPan paper](https://doi.org/10.1038/s41467-019-10927-1).
3. The implementation of the model in R is available in [MelonnPan site](https://huttenhower.sph.harvard.edu/melonnpan).



