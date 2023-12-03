import pandas as pd
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    for name in ["Jacob"]: #"Ben_Gurion", "He","Jacob","Parkinson"
        metab_test = pd.read_csv(f"melon_pan_data/{name}/metab.csv",index_col=0)[:60]
        metab_pred = pd.read_csv(f"melon_pan_data/{name}/preds/MelonnPan_Predicted_Metabolites.csv",index_col=0)[:60]
        common  = list(set(metab_test.columns).intersection(metab_pred.columns))
        metab_test = metab_test[common]
        metab_pred = metab_pred[common]
        if name == "Ben_Gurion":
            tag = pd.read_csv("Data//Ben_Gurion/tag_fatty_liver.csv", index_col=0)
            tag.index = [f"{int(i[-3:])}_0" if "PBLN" in i else f"{int(i[-3:])}_{int(i[-6:-4])}" for i in tag.index]
        elif name == "He":
            tag = pd.read_csv("Raw_Data/HE_INFANTS_MFGM_efrat/63189_mapping_file__small.csv", index_col=0)
            # make binary groups
            tag[tag["diet"] == "Breast milk"] = 0.0
            tag[tag["diet"] == "Standard infant formula"] = 1.0
            tag[tag["diet"] == "Experimental infant formula"] = 2.0

            tag = tag["diet"]
            tag.index = [i[6:].replace(".", "-") for i in tag.index]

        elif name == "Jacob":
            tag = pd.read_csv("Data/Jacob_efrat/Pediatric_family_cohort_map.csv", index_col=0)
            # make binary groups
            tag[tag["IBD_Status"] == "Normal"] = 0.0
            tag[tag["IBD_Status"] != 0.0] = 1.0
            tag = tag["IBD_Status"]

        elif name == "Parkinson":
            tag = pd.read_csv("Data/Parkinson_linoy/parkinson_or_control.csv", index_col=0)
            tag[tag.values == "P"] = 1.0
            tag[tag.values == "C"] = 0.0

        tag = tag.loc[metab_test.index]

         # calculate real corrs:
        dict_real = dict()
        dict_pred = dict()
        for metab in metab_test.columns:
            dict_real[metab] = spearmanr(metab_test[metab],tag)[0]
            dict_pred[metab] = spearmanr(metab_pred[metab],tag)[0]

        corr_real_series = pd.Series(dict_real).dropna()
        corr_pred_series = pd.Series(dict_pred).dropna()
        common = list(corr_real_series.index.intersection(corr_pred_series.index))
        corr_real_series = corr_real_series.loc[common]
        corr_pred_series = corr_pred_series.loc[common]

        c, p = spearmanr(corr_real_series.values, corr_pred_series.values)
        print(name)
        print(f"SCC:{c} ,p-value:{p}")
        print("_______________________")

        # plot
        fig, ax = plt.subplots()
        ax.scatter(list(dict_real.values()), list(dict_pred.values()), label=f"SCC:{np.round(c, 3)}")
        lims = [
            np.min([ax.get_xlim(), ax.get_ylim()]),  # min of both axes
            np.max([ax.get_xlim(), ax.get_ylim()]),  # max of both axes
        ]

        # now plot both limits against eachother
        ax.plot(lims, lims, 'k-', alpha=0.75, zorder=0)
        ax.set_aspect('equal')
        ax.set_xlim(lims)
        ax.set_ylim(lims)
        plt.xlabel("Real correlation")
        plt.ylabel("Predicted correlation")
        plt.title(name)
        plt.legend()
        plt.savefig(f"melon_pan_data/condition_melon_pan/{name}.png")
        plt.show()

        x=4
