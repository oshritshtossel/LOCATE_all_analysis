import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl

def plot_heatmap(df,labels, title=" ", save=""):
    plt.figure(figsize=(5, 5))
    min_ = df.min().min()
    max_ = df.max().max()
    ax=sns.heatmap(df.astype(float), cmap="coolwarm_r",vmin=-0.4,vmax=0.4,cbar=False)

    ax2 = ax.twinx()
    ax2 = sns.heatmap(df.astype(float), cmap="coolwarm_r", vmin=-0.4, vmax=0.4,cbar=False)#cbar_kws={'orientation': 'horizontal'}
    ax2.set_yticklabels(labels,fontdict=None, minor=False)
    ax2.tick_params(right=True)

    plt.title(title)
    plt.tight_layout()
    plt.savefig(save)
    plt.show()

if __name__ == '__main__':
    mpl.rc('font', family='Times New Roman')
    folder = "final_fig/Fig_3"
    df = pd.read_csv(f"{folder}/raw_corr_bnet.csv",index_col=0)
    df["group"] = df["Metabolites"]+"_"+df.index
    df["group"] = [i[:-2] for i in df["group"]]
    df_last = df.groupby(df["group"]).last()
    df_mean = df.groupby(df["group"]).mean()
    df_mean.index = ["k"+i.split("_k")[1] for i in df_last.index]
    df_mean.index = [i.split("__")[-1]+" (o)" for i in df_mean.index]

    plot_heatmap(df_mean,labels=df_last["Metabolites"],save=f"final_fig/Fig_3/Kim_He_Jacob_LONG_raw_without_cbar.png")
    c=0