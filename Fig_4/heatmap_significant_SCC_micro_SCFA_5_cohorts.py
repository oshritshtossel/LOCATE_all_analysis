import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

def plot_heatmap(df,labels, title="", save=""):
    del df["metab"]

    plt.figure(figsize=(7, 12))
    min_ = df.min().min()
    max_ = df.max().max()
    ax=sns.heatmap(df.astype(float), cmap="coolwarm_r",vmin=-0.5,vmax=0.5,cbar=False)
    ax.tick_params(right=True)
    ax2 = ax.twinx()
    ax2 = sns.heatmap(df.astype(float), cmap="coolwarm_r", vmin=-0.5, vmax=0.5,cbar=False)#, cbar_kws={'orientation': 'horizontal'}
    ax2.set_yticklabels(labels,fontdict=None, minor=False)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(save)
    plt.show()

def choose_significant(df,p_val):
    df = df[df["p"]<=p_val]
    return df
if __name__ == '__main__':
    font = {'family': 'Times New Roman',
            'size': 15}

    mpl.rc('font', **font)
    df1 = pd.read_csv(f"consistent_scfa/tax7_inter/ERAWIJANTARI_GASTRIC_CANCER_2020.csv",index_col=0)
    df2 = pd.read_csv(f"consistent_scfa/tax7_inter/FRANZOSA_IBD_2019.csv",index_col=0)
    df3 = pd.read_csv(f"consistent_scfa/tax7_inter/WANG_ESRD_2020.csv",index_col=0)
    df4 = pd.read_csv(f"consistent_scfa/tax7_inter/MARS_IBS_2020.csv",index_col=0)
    df5 = pd.read_csv(f"consistent_scfa/tax7_inter/YACHIDA_CRC_2019.csv",index_col=0)
    p =0.05
    df1 = choose_significant(df1,p)
    df2 = choose_significant(df2,p)
    df3 = choose_significant(df3,p)
    df4 = choose_significant(df4,p)
    df5 = choose_significant(df5,p)
    common = list(df1.index.intersection(df2.index).intersection(df3.index).intersection(df4.index).intersection(df5.index))#common 5
    #common = list(df1.index.intersection(df3.index).intersection(df4.index).intersection(df5.index))# common 4
    # 5 common
    df1_5 = df1.loc[common]
    df2_5 = df2.loc[common]
    df3_5 = df3.loc[common]
    df4_5 = df4.loc[common]
    df5_5 = df5.loc[common]
    df_to_plot = pd.DataFrame(columns=["ERAWIJANTARI","FRANZOSA","WANG","MARS","YACHIDA"])# common 5
    #df_to_plot = pd.DataFrame(columns=["ERAWIJANTARI","WANG","MARS","YACHIDA"])# common 4
    df_to_plot["ERAWIJANTARI"] =df1["corr"]
    df_to_plot["FRANZOSA"] =df2["corr"]
    df_to_plot["WANG"] =df3["corr"]
    df_to_plot["MARS"] =df4["corr"]
    df_to_plot["YACHIDA"] =df5["corr"]
    df_to_plot = df_to_plot.dropna()
    indexes = [i.split("-")[0] for i in df_to_plot.index]
    labels = [i.split("-")[-1] for i in df_to_plot.index]
    df_to_plot["metab"]=labels
    df_to_plot.index = indexes
    df_to_plot.index = [i.split(";")[-1].split("__")[-1]+" ("+i.split(";")[-1].split("__")[0]+")" for i in df_to_plot.index]
    plot_heatmap(df_to_plot,labels=df_to_plot["metab"],save="final_fig/Fig_3/new/common5_significant.png")

    c=0
