import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.cluster.hierarchy as sch

def plot_heatmap(df,labels, title="", save=""):

    metab = df["metab"]
    del df["metab"]

    plt.figure(figsize=(5, 15))
    # retrieve clusters using fcluster
    d = sch.distance.pdist(df)
    L = sch.linkage(d, method='average')
    # 0.2 can be modified to retrieve more stringent or relaxed clusters
    clusters = sch.fcluster(L, 0.38 * d.max(), 'distance')

    # clusters indicices correspond to incides of original df
    for i, cluster in enumerate(clusters):
        print(df.index[i], cluster)

    # group the features according to their clusters
    df["clusters"] = list(clusters)
    df["Clusters"] = ["k" for i in range(len(df.index))]
    df["Clusters"][df["clusters"] ==1] = "lightgrey"
    df["Clusters"][df["clusters"] ==2] = "darkgrey"
    df["Clusters"][df["clusters"] ==3] = "dimgrey"

    ax = sns.clustermap(df[["ERAWIJANTARI","FRANZOSA","MARS","YACHIDA"]].astype(float), cmap="coolwarm_r", vmin=-0.5, vmax=0.5,row_colors=df["Clusters"])

    plt.title(title)
    plt.tight_layout()
    plt.savefig(save)
    plt.show()

def choose_significant(df,p_val):
    df = df[df["p"]<=p_val]
    return df

def calculate_consistency(df):
    del df["metab"]

if __name__ == '__main__':
    mpl.rc('font', family='Times New Roman')
    # ONLY GASTRIC PROBLEMS
    df1 = pd.read_csv(f"consistent_scfa/all4/ERAWIJANTARI_GASTRIC_CANCER_2020.csv",index_col=0)
    df2 = pd.read_csv(f"consistent_scfa/all4/FRANZOSA_IBD_2019.csv",index_col=0)
    df4 = pd.read_csv(f"consistent_scfa/all4/MARS_IBS_2020.csv",index_col=0)
    df5 = pd.read_csv(f"consistent_scfa/all4/YACHIDA_CRC_2019.csv",index_col=0)
    p =0.05
    df1 = choose_significant(df1,p)
    df2 = choose_significant(df2,p)

    df4 = choose_significant(df4,p)
    df5 = choose_significant(df5,p)
    common = list(df1.index.intersection(df2.index).intersection(df4.index).intersection(df5.index))# common 4
    # 5 common
    df1_5 = df1.loc[common]
    df2_5 = df2.loc[common]
    df4_5 = df4.loc[common]
    df5_5 = df5.loc[common]
    df_to_plot = pd.DataFrame(columns=["ERAWIJANTARI","FRANZOSA","MARS","YACHIDA"])# common 4 only gastric
    df_to_plot["ERAWIJANTARI"] =df1_5["corr"]
    df_to_plot["FRANZOSA"] =df2_5["corr"]
    df_to_plot["MARS"] =df4_5["corr"]
    df_to_plot["YACHIDA"] =df5_5["corr"]
    df_to_plot = df_to_plot.dropna()
    indexes = [i.split("-")[0] for i in df_to_plot.index]
    labels = [i.split("-")[-1] for i in df_to_plot.index]
    df_to_plot.index = [i.split(";")[-1] for i in df_to_plot.index]
    df_to_plot["metab"]=labels

    print((df_to_plot[["ERAWIJANTARI","FRANZOSA","MARS","YACHIDA"]].var(axis=1)).mean())

    plot_heatmap(df_to_plot,labels=df_to_plot["metab"],save="final_fig/Fig_6/all_cm_common4_all_metab.png")

