import pandas as pd
from scipy.stats import spearmanr
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    melon_pan = True
    for name in ["Ben_Gurion", "He","Jacob","Parkinson"]: #"Ben_Gurion", "He","Jacob","Parkinson"
        metab_test = pd.read_csv(f"results/{name}/CV/0/3/test_metabolites.csv",index_col=0)
        metab_pred = pd.read_csv(f"results/{name}/CV/0/3/prediction.csv",index_col=0)
        if name == "Ben_Gurion":
            if melon_pan:
                melon = pd.read_csv("melon_pan_data/Ben_Gurion/metab.csv", index_col=0)
                metab_test = metab_test[melon.columns]
                metab_pred = metab_pred[melon.columns]
            tag = pd.read_csv("Data//Ben_Gurion/tag_fatty_liver.csv", index_col=0)
            tag.index = [f"{int(i[-3:])}_0" if "PBLN" in i else f"{int(i[-3:])}_{int(i[-6:-4])}" for i in tag.index]

        elif name == "He":
            if melon_pan:
                melon = pd.read_csv("melon_pan_data/He/metab.csv", index_col=0)
                metab_test = metab_test[melon.columns]
                metab_pred = metab_pred[melon.columns]
            tag = pd.read_csv("Raw_Data/HE_INFANTS_MFGM_efrat/63189_mapping_file__small.csv", index_col=0)
            # make binary groups
            tag[tag["diet"] == "Breast milk"] = 0.0
            tag[tag["diet"] == "Standard infant formula"] = 1.0
            tag[tag["diet"] == "Experimental infant formula"] = 2.0

            tag = tag["diet"]
            tag.index = [i[6:].replace(".", "-") for i in tag.index]

        elif name == "Jacob":
            if melon_pan:
                melon = pd.read_csv("melon_pan_data/Jacob/metab.csv", index_col=0)
                common_ = list(melon.columns.intersection(metab_test.columns))
                metab_test = metab_test[common_]
                metab_pred = metab_pred[common_]
            tag = pd.read_csv("Data/Jacob_efrat/Pediatric_family_cohort_map.csv", index_col=0)
            # make binary groups
            tag[tag["IBD_Status"] == "Normal"] = 0.0
            tag[tag["IBD_Status"] != 0.0] = 1.0
            tag = tag["IBD_Status"]

        elif name == "Parkinson":
            if melon_pan:
                melon = pd.read_csv("melon_pan_data/Parkinson/metab.csv", index_col=0)
                metab_test = metab_test[melon.columns]
                metab_pred = metab_pred[melon.columns]
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
        plt.savefig(f"results/condition_mimenet/3/melon_metab/{name}.png")
        plt.show()

        x=4
