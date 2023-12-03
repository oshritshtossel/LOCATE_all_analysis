# LOCATE - overall analysis code including statistical analysis, comparisons, and visualizations

This code is attached to the paper "Gut microbiome-metabolome interactions predict host condition". We propose **LOCATE (Latent variables Of miCrobiome And meTabolites rElations)**
a machine learning tool to predict the metabolite concentration from the microbiome composition and produce a latent representation of the interaction. This representation is then used to predict the host condition.

LOCATE's accuracy in predicting the metabolome is higher than all current predictors. The metabolite concentration prediction accuracy significantly decreases cross datasets, and cross conditions, especially in 16S data.

LOCATE’s latent representation predicts the host condition better than either microbiome or the metabolome. This representation is strongly correlated with host demographics. A significant improvement in accuracy (0.793 vs. 0.724 average accuracy) is obtained even with a small number of metabolite samples ($\sim 50$).

![A schematic figure of LOCATE’s training](https://github.com/oshritshtossel/LOCATE_all_analysis/blob/master/img/mid_schematic.png)

https://github.com/oshritshtossel/LOCATE_all_analysis/blob/master/img/mid_schematic.png

## How to apply LOCATE

LOCATE's code is available at a separate [GitHub](https://github.com/oshritshtossel/LOCATE/) as well as a [PyPi](https://pypi.org/project/LOCATE-model/).

## Comparison to other existing state-of-the-art models
During our work, we compared our results to other state-of-the-art models in the field. 
All the models' codes are available in the **Models** directory.

### INTEGRATED-LEARNER

1. **"integrated_learner_preprocess.py"** - Apply all the preprocessing needed to the microbiome datasets as well as the metabolites datasets according to the [Integrated-Learner paper](https://doi.org/10.1101/2022.11.06.514786).
2. The implementation of the model (in R) over the datasets tested in the manuscript is available in [Google Colab](https://colab.research.google.com/drive/1MFsncDnYAux05xdIuhNDxpZMSQGPRR9X).

### MELONNPAN
1. **"melonnpan_condition.py"** - Adjust the condition (phenotype) of each dataset to the prediction task.
2. **"melonnpan_preprocess.py"** - Apply all the preprocessing needed to the microbiome datasets as well as the metabolites datasets according to the [MelonnPan paper](https://doi.org/10.1038/s41467-019-10927-1).
3. The implementation of the model in R is available on [MelonnPan site](https://huttenhower.sph.harvard.edu/melonnpan).

### MIMENET
1. **"mimenet_src"** - Directory contains different models' architectures for MiMeNet as described in the [MiMeNet paper](https://doi.org/10.1371/journal.pcbi.1009021).
2. **"mimenet_condition.py"** - Adjust the condition (phenotype) of each dataset to the prediction task.
3. **"mimenet_preprocess.py"** - Apply all the preprocessing needed to the microbiome datasets as well as the metabolites datasets according to the [MiMeNet paper](https://doi.org/10.1371/journal.pcbi.1009021).
4. **"mimenet_runner.py"** - Run the MiMeNet model on each of the tested datasets in the manuscript according to the [MiMeNet paper](https://doi.org/10.1371/journal.pcbi.1009021) protocol.

### MNODE
1. **"mnode_preprocess.py"** - Apply all the preprocessing needed to the microbiome datasets as well as the metabolites datasets according to the [mNODE paper](https://doi.org/10.1038/s42256-023-00627-3).
2. The implementation of the model in Julia is available in [mNODE GitHub](https://github.com/wt1005203/mNODE).

### MULTIVIEW
1. **"multi_view_preprocess.py"** - Apply all the preprocessing needed to the microbiome datasets as well as the metabolites datasets according to the [Multiview paper](https://doi.org/10.1073/pnas.2202113119).
2. The implementation of the model (in R) over the datasets tested in the manuscript is available in [Google Colab](https://colab.research.google.com/drive/1MFsncDnYAux05xdIuhNDxpZMSQGPRR9X).

### SPARSENED
1. **"sparse_ned_L0_regularization"** - Directory contains different models' architectures and layers implementations as described in the [Sparse-NED paper](https://doi.org/10.1186/s12864-020-6652-7).
2. **"sparse_ned_snip"** - Directory contains useful utils for the Sparse-NED models.
3. **"sparse_ned_biome_ae.py"** - Dataloader, training, loss functions as described in [Sparse-NED GitHub](https://github.com/vuongle2/BiomeNED)
4. **"sparse_ned_condition.py"** - Adjust the condition (phenotype) of each dataset to the prediction task.
5. **"sparse_ned_models.py"** - Forward and backward implementations and some architectures as further described in [Sparse-NED GitHub](https://github.com/vuongle2/BiomeNED).
6. **"sparse_ned_preprocess.py"** - Apply all the preprocessing needed to the microbiome datasets as well as the metabolites datasets according to the [Sparse-NED paper](https://doi.org/10.1186/s12864-020-6652-7).
7. **"sparse_ned_runner.py"** -  Run the Sparse-NED model on each of the tested datasets in the manuscript according to the [Sparse-NED paper](https://doi.org/10.1186/s12864-020-6652-7) protocol.
8. **"sparse_ned_utils.py"** - Necessary utils for the sparse_ned_runner code.

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
  
3. **"frequency_bar_plot_of_highest_NMF_coef.py"** -

   * Plot Bar plots of the frequency of the microbes associated with the 10 highest coefficients in the NMF models of C5H11NO2S **(E)** and C4H7NO4 **(F)**.
     
   * Draw a scatter plot of the coefficients in the log NMF model of the taxa with the highest coefficients vs. the logged frequency of the same taxa, with no clear correlation between them **(G)**.

### Fig_3 - LOCATE can be used to predict metabolites in each dataset separately better than all existing methods

1. **"swarm_plot_different_models_metab_predictions.py"** -

   * Compare between LOCATE and all state-of-the-art metabolites prediction models over the different 16S datasets He **(B)**, Poyet **(C)**, Jacob **(D)**, Direct Plus **(E)**.
     
   * Draw swarm plots of the results, such that each point represents the SCC of a single metabolite in the dataset.

   * Apply a two-sided t-test was applied between the SCCs of the different models. The stars represent the p-values, such that *p−value ≤ 0.05, **p-value ≤ 0.01, ***p − value ≤ 0.001, ****p−value ≤ 0.0001.
  
2. **"bar_plot_all_avg_all_data.py"** -

   * Plot average SCCs over all metabolites and all the datasets per model, the 16S averages **(F)** and the WGS averages **(G)**. The black error bars represent the standard errors over all metabolites and all the datasets.

### Fig_4 - Microbiome-metabolite relations are dataset-specific

1. **"heatmap_significant_SCC_micro_SCFA_5_cohorts.py"** -

   * Draw a heatmap of significant SCCs between microbes and SCFA over different WGS datasets (ERAWIJANTARI, FRANZOSA, MARS, WANG, YACHIDA). Each row represents a microbe-metabolite pair and each column represents a different dataset. Red/blue colors represent       negative/positive correlations **(A)**.  

2. **"heatmap_significant_SCC_micro_metab_gastric.py"** - 

   * Draw a heatmap of significant SCCs between all common microbes and metabolites over different gastric problems WGS datasets (ERAWIJANTARI, FRANZOSA, MARS, YACHIDA). Similar
to **A**. each row represents a microbe-metabolite pair and each column represents a different dataset. **A** and **B** share the same color bar.

    * Cluster the metabolites according to their correlations.

3. **"heatmap_significant_micro_metab_litrature_16S.py"** -

   * Draw a heatmap of SCC between microbes and metabolites over different 16S datasets (He, Kim, and Jacob) vs. the relations that are reported in the literature **(C)**.

4. **"core_microbiome.py"** -

   * Find the core microbiome of 10 different cohorts. There are about 20 orders which are common to most of the datasets. These orders are also the most frequent taxa in the population of the cohorts. The x-axis represents the fraction of the population in the order       that exists in each cohort. If the order appears in all the populations of all the cohorts, it sums to 10. The y-axis represents the different orders. Each color represents a cohort **(D)**.
  
5. **"swarm_plot_BGU_different_times.py"** -

   * Draw a swarm plot of LOCATE’s predicted metabolites SCCs in the cross-times test over the Direct Plus cohort **(E)**.
  
   * Apply a two-sided t-test was applied between the SCCs of the different models. The stars represent the p-values, such that *p−value ≤ 0.05, **p-value ≤ 0.01, ***p − value ≤ 0.001, ****p−value ≤ 0.0001.
  
6. **"swarm_plot_between_cohorts_all_models.py"** -

   *  Draw swarm plots of all of the cross-datasets predictions between couples of datasets on the shared metabolites and microbes, such as He-Direct Plus **(F)**, He-Kim **(G)**, He-Jacob **(H)**.
   
   * Model is trained on the intersection of the microbiome and metabolites of the pair but predicts on an internal test of the same dataset, “in-
learning” (the dark points, referred to as “model-in”)

   * Model is trained on one dataset and is tested on the other dataset, “ex-learning” (the light points, referred to as “model-ex”).
  
   * Apply a two-sided t-test was applied between the SCCs of the different models. The stars represent the p-values, such that *p−value ≤ 0.05, **p-value ≤ 0.01, ***p − value ≤ 0.001, ****p−value ≤ 0.0001.
  
### Fig_5 - Internal representation improves outcome prediction compared with microbiome and metabolites and is associated with dataset features

1. **"cca_plot.py"** -

   * Plot average SCC between the CCA outputs of the microbiome and metadata over 16S datasets (pink,**A**), the metabolites and metadata (yellow,**A**), and LOCATE’s representation and the metadata (blue, **A**).

   * Apply a one-sided t-test is applied between the models. The stars follow the previous figures.
  
2. **"weights_CCA_LOCATE_metadata.py"** -

   * Plot weights of the CCA between LOCATE’s representations and the metadata on its two first components on He **(B)**, Jacob **(C)**, and Poyet **(D)**. When the variable is categorical, all the weights are stacked together in different colors (for the categorical
information see Supp. Mat. Table S7). The first component values are in blue colors and the second component values are in green.

3. **"auc_comparison.py"** -

   * Plot bar plots of the average AUC over 16S datasets **(E)** and of the predicted outcomes over different datasets and different tasks. The pink
colors represent the different microbiome-based models. The light pink represents an iMic model trained on the microbiome data only (referred to as ”Mic. iMic”). The dark pink represents an iMic model trained on the microbiome and the metadata together (referred to as ”Mic., meta iMic”). The yellow colors represent the metabolites-based models. The light yellow represents a logistic regression (LR) model in E or a Ridge model in F trained only on the metabolites
(referred to as ”Met. LR”) and the dark yellow represents an iMic model trained on both the metabolites and microbiome (referred to as ”Mic., Met. iMic”). The blue colors represent the
models based on LOCATE. The lightest light blue represents the Log network (referred to as ”Log-log LR”). The intermediate blue represents a model trained on LOCATE’s representation
(referred to as ”Z LOCATE LR”), while the darkest blue represents a model trained on both LOCATE’s representation and the metadata (referred to as ”Z LOCATE, meta LR”). The
standard errors between the 10 cross-validations are in black.

   * Apply a  one-sided t-test was applied between the models. The stars follow the previous figures.

4. **"scc_comparison.py"** -

   * Plot bar plots of the average SCC over 16S datasets **(F)** and of the predicted outcomes over different datasets and different tasks. The pink
colors represent the different microbiome-based models. The light pink represents an iMic model trained on the microbiome data only (referred to as ”Mic. iMic”). The dark pink represents an iMic model trained on the microbiome and the metadata together (referred to as ”Mic., meta iMic”). The yellow colors represent the metabolites-based models. The light yellow represents a logistic regression (LR) model in E or a Ridge model in F trained only on the metabolites
(referred to as ”Met. LR”) and the dark yellow represents an iMic model trained on both the metabolites and microbiome (referred to as ”Mic., Met. iMic”). The blue colors represent the
models based on LOCATE. The lightest light blue represents the Log network (referred to as ”Log-log LR”). The intermediate blue represents a model trained on LOCATE’s representation
(referred to as ”Z LOCATE LR”), while the darkest blue represents a model trained on both LOCATE’s representation and the metadata (referred to as ”Z LOCATE, meta LR”). The
standard errors between the 10 cross-validations are in black.

   * Apply a one-sided t-test was applied between the models. The stars follow the previous figures.
  
5. **"effect_num_training_pairs_performance.py"** -

   * Plot the effect of a decreasing number of metabolites for LOCATE’s representation on the condition predictions in He **(G)**, Jacob **(H)** and Poyet **(I)**. The x-axis represents the number of pairs of microbiome and metabolites used for the training of LOCATE, the y-axis represents the difference between the average AUC (over 10 runs) of the predicted outcome based on LOCATE’s representation and the average AUC (over 10 runs) of the predicted outcome based on the microbiome only. In most of the datasets, 50 metabolites are enough for LOCATE’s representation to be better than the microbiome. The pink line represents the zero value, and the
dashed yellow line represents the metabolites’ contribution (of all samples) to the microbiome. When LOCATE is better the point is above the pink line.

6. **"auc_comparison_integration_methods_vs_LOCATE.py"** -

   * Plot bar plots of the average AUC **(J)** and the average SCC **(K)** of the predicted outcomes over different 16S datasets and different tasks. The orange color represents the Multiview model’s results. The red colors represent the
IntegratedLearner different models. The pink-red color represents an IntegratedLearner variant of microbiome only, the orange-red color represents an IntegratedLearner variant of metabolites
only, the red color represents an IntegratedLearner variant of stacked, and the dark red color represents an IntegretatedLearner variant of concatenated. The blue color represents LOCATE.
The standard errors between the 10 cross-validations are in black.

   * Apply a one-sided t-test was applied between the models. The stars follow the previous figures.
  
### Fig_6 - Internal representation improves outcome prediction compared with the microbiome and when possible also metabolites and is associated with datasets features - on WGS datasets. 

1. **"cca_plot_sg.py"** -

   * Plot average SCC between the CCA outputs of the microbiome and metadata over WGS datasets (pink,**A**), the metabolites and metadata (yellow,**A**), and LOCATE’s representation and the metadata (blue, **A**).

   * Apply a one-sided t-test is applied between the models. The stars follow the previous figures.
  
2. **weights_CCA_LOCATE_metadata_sg.py** -

   * Plot weights of the CCA between LOCATE’s representations and the metadata on its two first components on ERAWIJANTARI **(B)**, FRANZOSA **(C)**, and WANG **(D)**. When the variable is categorical, all the weights are stacked together in different colors (for the categorical
information see Supp. Mat. Table S7). The first component values are in blue colors and the second component values are in green.

3. **"auc_comparison_sg.py"** -

   * Plot bar plots of the average AUC over WGS datasets **(E)** and of the predicted outcomes over different datasets and different tasks. The pink
colors represent the different microbiome-based models. The light pink represents an iMic model trained on the microbiome data only (referred to as ”Mic. iMic”). The dark pink represents an iMic model trained on the microbiome and the metadata together (referred to as ”Mic., meta iMic”). The yellow colors represent the metabolites-based models. The light yellow represents a logistic regression (LR) model in E or a Ridge model in F trained only on the metabolites
(referred to as ”Met. LR”) and the dark yellow represents an iMic model trained on both the metabolites and microbiome (referred to as ”Mic., Met. iMic”). The blue colors represent the
models based on LOCATE. The lightest light blue represents the Log network (referred to as ”Log-log LR”). The intermediate blue represents a model trained on LOCATE’s representation
(referred to as ”Z LOCATE LR”), while the darkest blue represents a model trained on both LOCATE’s representation and the metadata (referred to as ”Z LOCATE, meta LR”). The
standard errors between the 10 cross-validations are in black.

   * Apply a  one-sided t-test was applied between the models. The stars follow the previous figures.

  
5. **"effect_num_training_pairs_performance_sg.py"** -

   * Plot the effect of a decreasing number of metabolites for LOCATE’s representation on the condition predictions in ERAWIJANTARI **(F)**, FRANZOSA **(G)** and WANG **(H)**. The x-axis represents the number of pairs of microbiome and metabolites used for the training of LOCATE, the y-axis represents the difference between the average AUC (over 10 runs) of the predicted outcome based on LOCATE’s representation and the average AUC (over 10 runs) of the predicted outcome based on the microbiome only. In most of the datasets, 50 metabolites are enough for LOCATE’s representation to be better than the microbiome. The pink line represents the zero value, and the
dashed yellow line represents the metabolites’ contribution (of all samples) to the microbiome. When LOCATE is better the point is above the pink line.

6. **"auc_comparison_integration_methods_vs_LOCATE_sg.py"** -

   * Plot bar plot of the average AUC **(I)**  of the predicted outcomes over different WGS datasets and different tasks. The orange color represents the Multiview model’s results. The red colors represent the
IntegratedLearner different models. The pink-red color represents an IntegratedLearner variant of microbiome only, the orange-red color represents an IntegratedLearner variant of metabolites
only, the red color represents an IntegratedLearner variant of stacked, and the dark red color represents an IntegretatedLearner variant of concatenated. The blue color represents LOCATE.
The standard errors between the 10 cross-validations are in black.

   * Apply a one-sided t-test was applied between the models. The stars follow the previous figures.
  

## Cite us 
Shtossel, Oshrit, et al. "Microbiome-metabolome interactions predict host phenotype." (2022).

## Contact us
[Oshrit Shtossel](oshritvig@gmail.com)















