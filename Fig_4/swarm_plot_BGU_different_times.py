import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statannot import add_stat_annotation
import numpy as np
import matplotlib as mpl

def choose_best_config(folder,pair):
    list_of_dfs = list()
    list_of_dfs1 = list()
    for i in range(16):
        if (pair != "ERAWIJANTARI_GASTRIC_CANCER_2020") and (pair != "YACHIDA_CRC_2019")and(pair != "iHMP_IBDMDB_2019")and(pair != "FRANZOSA_IBD_2019")and(pair != "iHMP_IBDMDB_2019")and(pair != "WANG_ESRD_2020")and(pair != "MARS_IBS_2020"):
            df1 =pd.read_csv(f"{folder}/1external_test_{pair}_corr_{i}.csv",index_col=0)
            df =pd.read_csv(f"{folder}/1internal_test_train_BGU_0_testBGU_6_corr_{i}.csv",index_col=0)
        else:
            df = pd.read_csv(f"{folder}/{pair}/02_val_corr_{i}.csv", index_col=0)

        list_of_dfs.append(df)
        list_of_dfs1.append(df1)

    all = pd.concat(list_of_dfs)
    all1 = pd.concat(list_of_dfs1)
    new = all.groupby(all.index).max()
    new1 = all1.groupby(all1.index).max()
    performance = pd.DataFrame(columns=["Internal","External"],index = df.index)
    performance["Internal"] = new["0"]
    performance["External"] = new1["0"]
    return performance


if __name__ == '__main__':

    mpl.rc('font', family='Times New Roman')
    our_folder = "p_vals_inv_10/bgu_trans_groups"
    list_of_pairs =["BGU_0_test_BGU_6"]
    for pair in list_of_pairs:
        ours = choose_best_config(our_folder,pair)
        ours.to_csv(f"{our_folder}/final_{pair}.csv")

        df_to_plot = pd.DataFrame(columns=["Internal","External"],index=ours.index)
        df_to_plot["Internal"] = ours["Internal"]
        df_to_plot["External"] = ours["External"]

        df_to_plot["sum"] = df_to_plot.sum(axis=1)
        df_to_plot = df_to_plot.sort_values("sum", ascending=False)
        del df_to_plot["sum"]
        df_to_plot = df_to_plot.head(1000)
        plt.figure(1, figsize=(7, 7))
        ax = sns.swarmplot(data=df_to_plot,palette=["blue", "cornflowerblue"])
        boxes = [df_to_plot["Internal"],df_to_plot["External"]]
        ax = sns.boxplot(data=boxes, boxprops={'facecolor': 'None'}
                         )
        test_results = add_stat_annotation(ax, data=pd.DataFrame(data=boxes, index=["A", "B"]).T,
                                           box_pairs=[("A", "B")],

                                           perform_stat_test=True,
                                           test="t-test_ind", text_format='star',
                                           loc='inside', verbose=2)
        plt.xticks(ticks=np.arange(2),
                   labels=["Internal",f"External"], fontsize=20, family='Times New Roman')
        plt.title("T0 vs T6", fontsize=30, family='Times New Roman',
                  fontweight="bold")


        plt.ylabel("SCC",family='Times New Roman',fontdict={"fontsize":20})
        plt.yticks(fontsize=20)
        plt.tight_layout()
        plt.savefig(f"final_fig/supp/BGU_different_times/{pair}_.png",dpi=300)

        plt.show()
