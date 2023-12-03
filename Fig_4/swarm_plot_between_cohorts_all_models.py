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
        df =pd.read_csv(f"{folder}/{pair}/{i}_val_corr_.csv",index_col=0)
        df1 =pd.read_csv(f"learning_val_results/all_cond_intersection/{pair}/{i}_val_corr_.csv",index_col=0)
        list_of_dfs.append(df)
        list_of_dfs1.append(df1)

    all = pd.concat(list_of_dfs)
    all1 = pd.concat(list_of_dfs1)
    new = all.groupby(all.index).max()
    new1 = all1.groupby(all1.index).max()
    performance = pd.DataFrame(columns=["Internal","External"],index = df.index)
    performance["Internal"] = new1["0"]
    performance["External"] = new["0"]
    return performance


if __name__ == '__main__':
    mpl.rc('font', family='Times New Roman')
    our_folder = "learning_val_results/all_cond_between"
    sparse_ned_folder = "p_vals_inv_10/sparse_ned"
    melon_folder = "melon_pan_between/results/results_for_swarm_plot"
    mnode_folder_between = "mnode/between"
    mnode_folder_internal = "mnode/between/Internal"
    list_of_pairs =["He_BGU", "He_Kim", "He_Jacob", "BGU_Kim", "BGU_Jacob",
                     "Kim_Jacob"]
    for pair in list_of_pairs:
        ours = choose_best_config(our_folder,pair)
        ours.to_csv(f"{our_folder}/final_{pair}.csv")

        mnode_ex = pd.read_csv(f"{mnode_folder_between}/{pair}/metabolites_corr.csv")
        mnode_in = pd.read_csv(f"{mnode_folder_internal}/{pair}/metabolites_corr.csv")

        name1 = pair.split("_")[0]
        name2 = pair.split("_")[1]
        ex_sparse = pd.read_csv(f"{sparse_ned_folder}/external_test_{name1}_test_{name2}_corr.csv",index_col=0)
        in_sparse = pd.read_csv(f"{sparse_ned_folder}/internal_test_train_{name1}_test{name2}_corr.csv",index_col=0)
        try:
            ex_melon = pd.read_csv(f"{melon_folder}/external_test_{pair}.csv",index_col=0)
            in_melon = pd.read_csv(f"{melon_folder}/internal_test_{pair}.csv",index_col=0)
        except:
            ex_melon = [0.0 for i in range(len(ex_sparse.index))]
            in_melon = [0.0 for i in range(len(in_sparse.index))]

        df_to_plot = pd.DataFrame(columns=["Ours - internal","SparseNED - internal","MelonnPan - internal","mNODE - internal", "Ours - external","SparseNED - external","MelonnPan - external","mNODE - external"],index=ex_sparse.index)
        df_to_plot["Ours - internal"] = ours["Internal"]
        df_to_plot["Ours - external"] = ours["External"]
        df_to_plot["SparseNED - internal"] = in_sparse
        df_to_plot["SparseNED - external"] = ex_sparse
        df_to_plot["MelonnPan - external"] = ex_melon
        df_to_plot["MelonnPan - internal"] = in_melon
        df_to_plot["mNODE - internal"] = list(mnode_in.values.flatten())
        df_to_plot["mNODE - external"] = list(mnode_ex.values.flatten())
        plt.figure(1, figsize=(6, 5))
        ax = sns.swarmplot(data=df_to_plot,palette=["blue", "orange","red","mediumpurple", "cornflowerblue", "sandybrown","tomato","plum"])
        boxes = [df_to_plot["Ours - internal"],df_to_plot["SparseNED - internal"],df_to_plot["MelonnPan - internal"].dropna(),df_to_plot["mNODE - internal"],df_to_plot["Ours - external"],df_to_plot["SparseNED - external"],df_to_plot["MelonnPan - external"].dropna(),df_to_plot["mNODE - external"]]
        ax = sns.boxplot(data=boxes, boxprops={'facecolor': 'None'}
                         )
        test_results = add_stat_annotation(ax, data=pd.DataFrame(data=boxes, index=["A", "B", "C", "D","E","F","G","H"]).T,
                                           box_pairs=[("A", "B"),("A", "C"),("A","D"),
                                                      ("E", "F"), ("E", "G"),("E","H")],

                                           perform_stat_test=True,
                                           test="t-test_ind", text_format='star',
                                           loc='inside', verbose=2)
        plt.xticks(ticks=np.arange(8),
                   labels=["LOCATE\n in",f"Sparse\nNED\n in", f"Melonn\nPan\n in","m\nNODE\n in","LOCATE\n ex",f"Sparse\nNED\n ex",f"Melonn\nPan\n ex","m\nNODE\n ex"], fontsize=13, family='Times New Roman')
        plt.yticks(fontsize=14)
        plt.title(pair.replace("_","-").replace("BGU","Direct Plus"), fontsize=30, family='Times New Roman',
                  fontweight="bold")
        plt.ylabel("SCC",family='Times New Roman',fontdict={"fontsize": 15})
        plt.tight_layout()

        plt.savefig(f"final_fig/revision/Fig_3/between/{pair}.png",dpi=300)
        plt.show()
