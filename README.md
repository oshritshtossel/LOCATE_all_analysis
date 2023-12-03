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
3. The implementation of the model in R is available on [MelonnPan site](https://huttenhower.sph.harvard.edu/melonnpan).

### MIMENET
1. "mimenet_src" - Directory contains different models' architectures for MiMeNet as described in the [MiMeNet paper](https://doi.org/10.1371/journal.pcbi.1009021).
2. "mimenet_condition.py" - Adjust the condition (phenotype) of each dataset to the prediction task.
3. "mimenet_preprocess.py" - Apply all the preprocessing needed to the microbiome datasets as well as the metabolites datasets according to the [MiMeNet paper](https://doi.org/10.1371/journal.pcbi.1009021).
4. "mimenet_runner.py" - Run the MiMeNet model on each of the tested datasets in the manuscript according to the [MiMeNet paper](https://doi.org/10.1371/journal.pcbi.1009021) protocol.

### MNODE
1. "mnode_preprocess.py" - Apply all the preprocessing needed to the microbiome datasets as well as the metabolites datasets according to the [mNODE paper](https://doi.org/10.1038/s42256-023-00627-3).
2. The implementation of the model in Julia is available in [mNODE GitHub](https://github.com/wt1005203/mNODE).

### MULTIVIEW
1. multi_view_preprocess.py" - Apply all the preprocessing needed to the microbiome datasets as well as the metabolites datasets according to the [Multiview paper](https://doi.org/10.1073/pnas.2202113119).
2. The implementation of the model (in R) over the datasets tested in the manuscript is available in [Google Colab](https://colab.research.google.com/drive/1MFsncDnYAux05xdIuhNDxpZMSQGPRR9X).

### SPARSENED
1. "sparse_ned_L0_regularization" - Directory contains different models' architectures and layers implementations as described in the [Sparse-NED paper](https://doi.org/10.1186/s12864-020-6652-7).
2. "sparse_ned_snip" - Directory contains useful utils for the Sparse-NED models.
3. "sparse_ned_biome_ae.py" - Dataloader, training, loss functions as described in [Sparse-NED GitHub](https://github.com/vuongle2/BiomeNED)
4. "sparse_ned_condition.py" - Adjust the condition (phenotype) of each dataset to the prediction task.
5. "sparse_ned_models.py" - Forward and backward implementations and some architectures as further described in [Sparse-NED GitHub](https://github.com/vuongle2/BiomeNED).
6. "sparse_ned_preprocess.py" - Apply all the preprocessing needed to the microbiome datasets as well as the metabolites datasets according to the [Sparse-NED paper](https://doi.org/10.1186/s12864-020-6652-7).
7. "sparse_ned_runner.py" -  Run the Sparse-NED model on each of the tested datasets in the manuscript according to the [Sparse-NED paper](https://doi.org/10.1186/s12864-020-6652-7) protocol.
8. "sparse_ned_utils.py" - Necessary utils for the sparse_ned_runner code.

## Statistical analysis, comparisons and visualizations
The analyses are presented according to the figures in the manuscript.

### Fig_2 -  The relation between the microbiome and the metabolites is not linear and is dominated by a few taxa

1. **"hist_ours_vs_shuffled.py"** -
   
   * Plot histograms of the coefficients of the NMF model which relates metabolite concentrations and the microbiome frequencies (real in dark purple) and of a random model
    with the microbes shuffled before the prediction (light purple) of the metabolite C2H4O2 **(A)** and C4H5N3O **(B)**.

2. **"swarm_plot_with_bars.py"** -
   * Draw swarm plots of all the expectations of the relative contribution of the coefficients of each metabolite for all the 16S rRNA gene-based **(C)** and the WGS datasets **(D)**. The
    expectations of the real models are represented in dark purple dots, while the expectations of the shuffled models are in light dots. Bar plots represent the median of each group.

    * Apply a two-sided t-test between the two models for each dataset. The stars represent the p-values, such that *-p-value ≤ 0.05, **-p-value ≤ 0.01, ***-p-value ≤ 0.001.
  
3. **frequency_bar_plot_of_highest_NMF_coef.py"** -

   * Plot Bar plots of the frequency of the microbes associated with the 10 highest coefficients in the NMF models of C5H11NO2S **(E)** and C4H7NO4 **(F)**.
     
   * Draw a scatter plot of the coefficients in the log NMF model of the taxa with the highest coefficients vs. the logged frequency of the same taxa, with no clear correlation between them **(G)**.

### Fig_3 - LOCATE can be used to predict metabolites in each dataset separately better than all existing methods

1. **swarm_plot_different_models_metab_predictions.py** -

   * Compare between LOCATE and all state-of-the-art metabolites prediction models over the different 16S datasets He **(B)**, Poyet **(C)**, Jacob **(D)**, Direct Plus **(E)**.
     
   * Draw swarm plots of the results, such that each point represents the SCC of a single metabolite in the dataset.

   * Apply a two-sided t-test was applied between the SCCs of the different models. The stars represent the p-values, such that *p−value ≤ 0.05, **p-value ≤ 0.01, ***p − value ≤ 0.001, ****p−value ≤ 0.0001.
  
2. **bar_plot_all_avg_all_data.py** -

   * Plot average SCCs over all metabolites and all the datasets per model, the 16S averages **(F)** and the WGS averages **(G)**. The black error bars represent the standard errors over all metabolites and all the datasets.

### Fig_4 - Microbiome-metabolite relations are dataset-specific

1. **heatmap_significant_SCC_micro_SCFA_5_cohorts.py** -

   * Draw a heatmap of significant SCCs between microbes and SCFA over different WGS datasets (ERAWIJANTARI, FRANZOSA, MARS, WANG, YACHIDA). Each row represents a microbe-metabolite pair and each column represents a different dataset. Red/blue colors represent       negative/positive correlations **(A)**.  

2. **heatmap_significant_SCC_micro_metab_gastric.py** - 

   * Draw a heatmap of significant SCCs between all common microbes and metabolites over different gastric problems WGS datasets (ERAWIJANTARI, FRANZOSA, MARS, YACHIDA). Similar
to **A**. each row represents a microbe-metabolite pair and each column represents a different dataset. **A** and **B** share the same color bar.

    * Cluster the metabolites according to their correlations.

3. **heatmap_significant_micro_metab_litrature_16S.py** -

   * 











