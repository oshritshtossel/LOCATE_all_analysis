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
            df =pd.read_csv(f"{folder}/{pair}/{i}_val_corr_.csv",index_col=0)
        else:
            df = pd.read_csv(f"{folder}/{pair}/02_val_corr_{i}.csv", index_col=0)

        list_of_dfs.append(df)


    all = pd.concat(list_of_dfs)
    new = all.groupby(all.index).max()
    performance = pd.DataFrame(columns=["Internal","External"],index = df.index)
    performance["External"] = new["0"]
    return performance

def choose_best_config_loglog(folder,pair):
    list_of_dfs = list()
    list_of_dfs1 = list()
    for i in range(5):
        df = pd.read_csv(f"{folder}/{pair}_{pair}_{i}.csv", index_col=0)

        list_of_dfs.append(df)


    all = pd.concat(list_of_dfs)
    new = all.groupby(all.index).max()
    performance = pd.DataFrame(columns=["Internal","External"],index = df.index)
    performance["External"] = new["x axis"]
    return performance

if __name__ == '__main__':
    mpl.rc('font', family='Times New Roman')
    loglog_folder = "corr_2_datasets_ours_for_swarm_with_intersect_self"
    linear_folder = "corr_nmf_single"
    locate_folder = "learning_val_results/all_cond_inside"
    sparse_ned_folder = "all_performances"
    melon_folder = "all_performances"
    mnode_folder ="mnode"

    #list_of_pairs =["Poyet","BGU", "He", "Jacob", "Kim"]#"Poyet","BGU", "He", "Jacob", "Kim"
    list_of_pairs =["YACHIDA_CRC_2019"]#"Poyet","BGU", "He", "Jacob", "Kim","YACHIDA_CRC_2019","FRANZOSA_IBD_2019","WANG_ESRD_2020","MARS_IBS_2020"
    for pair in list_of_pairs:
        ours = choose_best_config(locate_folder,pair)
        ours.to_csv(f"{locate_folder}/final_{pair}.csv")
        loglog = choose_best_config_loglog(loglog_folder,pair)

        loglog = loglog
        linear = pd.read_csv(f"{linear_folder}/{pair}_{pair}.csv",index_col=0)["x axis"]
        linear = linear
        mnode = pd.read_csv(f"{mnode_folder}/{pair}/metabolites_corr.csv")

        if (pair != "ERAWIJANTARI_GASTRIC_CANCER_2020") and (pair != "YACHIDA_CRC_2019")and(pair != "FRANZOSA_IBD_2019")and(pair != "iHMP_IBDMDB_2019")and(pair != "WANG_ESRD_2020")and(pair != "MARS_IBS_2020") :
            sparse = pd.read_csv(f"{sparse_ned_folder}/{pair}.csv",index_col=0)["Sparse NED"]
        else:
            sparse = pd.read_csv(f"sparse_ned_corrs/{pair}/test_corrs_5_cv.csv",index_col=0)

        try:
            melon = pd.read_csv(f"{melon_folder}/{pair}.csv",index_col=0)["MelonPann"]

        except:
            melon = [0.0 for i in range(len(loglog.index))]


        try:
            if (pair != "ERAWIJANTARI_GASTRIC_CANCER_2020") and (pair != "YACHIDA_CRC_2019")and(pair != "FRANZOSA_IBD_2019")and(pair != "iHMP_IBDMDB_2019")and(pair != "WANG_ESRD_2020")and(pair != "MARS_IBS_2020"):
                mimenet = pd.read_csv(f"{sparse_ned_folder}/{pair}.csv", index_col=0)["MimeNet"]
            else:
                mimenet = pd.read_csv(f"results/results/{pair}/cv_correlations.csv",index_col=0)["Mean"]
        except:
            mimenet = [0.0 for i in range(len(loglog.index))]


        df_to_plot = pd.DataFrame(columns=["LOCATE","Log network","Linear network","SparseNED","MelonnPan", "MimeNet","mNODE"],index=loglog.index)
        df_to_plot["LOCATE"] = ours["External"]
        df_to_plot["Log network"] = loglog["External"]
        df_to_plot["Linear network"] = linear
        df_to_plot["SparseNED"] = sparse
        df_to_plot["MelonnPan"] = melon
        df_to_plot["MimeNet"] = mimenet
        df_to_plot["mNODE"] = list(mnode.values.flatten())
        df_to_plot["sum"] = df_to_plot.sum(axis=1)
        df_to_plot = df_to_plot.sort_values("sum", ascending=False)
        del df_to_plot["sum"]
        df_to_plot = df_to_plot
        plt.figure(1, figsize=(6, 4))
        ax = sns.swarmplot(data=df_to_plot,palette=["blue", "lightskyblue","lightsteelblue","orange","red", "green","mediumpurple"],zorder=0)
        boxes = [df_to_plot["LOCATE"],df_to_plot["Log network"],df_to_plot["Linear network"].dropna(),df_to_plot["SparseNED"],df_to_plot["MelonnPan"].dropna(),df_to_plot["MimeNet"],df_to_plot["mNODE"]]
        ax = sns.boxplot(data=boxes, boxprops={'facecolor': 'None'}
                         )
        test_results = add_stat_annotation(ax, data=pd.DataFrame(data=boxes, index=["A", "B", "C","D","E","F","G"]).T,
                                           box_pairs=[("A", "B"),("A", "C"),
                                                      ("B","C"),("A","D"),("A","E"),("A","F"),("A","G")],

                                           perform_stat_test=True,
                                           test="t-test_ind", text_format='star',
                                           loc='inside', verbose=2)
        plt.xticks(ticks=np.arange(7),
                   labels=["LOCATE",f"Log\nnetwork", f"Linear\n network",f"Sparse\nNED", f"Melonn\nPan","MimeNet","m\nNODE"], fontsize=14, family='Times New Roman')
        if pair  == "BGU":
            plt.title(pair.replace("BGU","Direct Plus"), fontsize=30, family='Times New Roman',
                      fontweight="bold")
        elif pair =="ERAWIJANTARI_GASTRIC_CANCER_2020":
            plt.title(pair.replace("ERAWIJANTARI_GASTRIC_CANCER_2020", "ERAWIJANTARI"), fontsize=30, family='Times New Roman',
                      fontweight="bold")
        elif pair == "YACHIDA_CRC_2019":
            plt.title(pair.replace("YACHIDA_CRC_2019", "YACHIDA"), fontsize=30,
                      family='Times New Roman',
                      fontweight="bold")
        elif pair == "FRANZOSA_IBD_2019":
            plt.title(pair.replace("FRANZOSA_IBD_2019", "FRANZOSA"), fontsize=30,
                      family='Times New Roman',
                      fontweight="bold")
        elif pair == "WANG_ESRD_2020":
            plt.title(pair.replace("WANG_ESRD_2020", "WANG"), fontsize=30,
                      family='Times New Roman',
                      fontweight="bold")
        elif pair == "MARS_IBS_2020":
            plt.title(pair.replace("MARS_IBS_2020", "MARS"), fontsize=30,
                      family='Times New Roman',
                      fontweight="bold")


        plt.ylabel("SCC",family='Times New Roman',fontdict={"fontsize":15})
        plt.yticks(fontsize=15)
        plt.tight_layout()
        plt.savefig(f"final_fig/revision/Fig_2/inside_swarms/{pair}.png",dpi=300)

        plt.show()

