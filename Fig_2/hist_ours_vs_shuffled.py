import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
if __name__ == '__main__':
    mpl.rc('font', family='Times New Roman')
    folder = "check_yoram_hypothesis_coef"
    for name in ["He"]:
        val_real = pd.read_csv(f"{folder}/for_hist_{name}.csv",index_col=0)
        val_shuffled = pd.read_csv(f"{folder}/for_hist_{name}_shuffled.csv",index_col=0)
        dict_metab_real = dict()
        dict_metab_real_std = dict()
        dict_metab_shuffled = dict()
        dict_metab_shuffled_std = dict()
        for metab in val_real.index:
            dict_metab_real[metab] = np.mean(eval(val_real.loc[metab][0]))
            dict_metab_real_std[metab] = np.std(eval(val_real.loc[metab][0]))
            dict_metab_shuffled[metab] = np.mean(eval(val_shuffled.loc[metab][0]))
            dict_metab_shuffled_std[metab] = np.std(eval(val_shuffled.loc[metab][0]))
        real = pd.Series(dict_metab_real)
        real_std = pd.Series(dict_metab_real_std)
        shuffled = pd.Series(dict_metab_shuffled)
        shuffled_std = pd.Series(dict_metab_shuffled_std)
        to_plot = pd.DataFrame(columns=["Real","Shuffled"])
        to_plot_stds = pd.DataFrame(columns=["Real","Shuffled"])
        to_plot["Real"] = real
        to_plot_stds["Real"] = real_std
        to_plot["Shuffled"] = shuffled
        to_plot_stds["Shuffled"] = shuffled_std
        to_plot_stds = to_plot_stds/10

        dict_metab = dict()
        for metab in val_real.index:
            dict_metab[[metab][0]] = sum([i > 0.5 for i in eval(val_real.loc[metab][0])])/(len(eval(val_real.loc[metab][0])))
        print((pd.Series(dict_metab)>0.5).sum())
        print(len(pd.Series(dict_metab).index))

        for metab in val_real.index:
            plt.figure(figsize=(5,5))
            plt.hist(eval(val_real.locv),bins=30,label="Real",alpha=0.75,color="blueviolet",edgecolor='black')#"black"
            plt.hist(eval(val_shuffled.loc[metab][0]),bins=30,label="Shuffled",alpha=0.5,color="mediumpurple",edgecolor='black')#"grey"
            plt.legend( prop={'size': 15})
            plt.title(metab,fontdict={"fontsize":25},fontweight="bold")
            plt.xlabel("Microbiome coefficient",fontdict={"fontsize":20})
            plt.ylabel("Frequency",fontdict={"fontsize":20})
            plt.xticks(fontsize=15)
            plt.yticks(fontsize=15)
            plt.axvline(x=np.mean(eval(val_real.loc[metab][0])), color='black',linewidth=3, linestyle= '-',zorder=1)
            plt.axvline(x=np.mean(eval(val_shuffled.loc[metab][0])), color='grey',linewidth=3, linestyle= '-',zorder=1)
            plt.tight_layout()

            plt.savefig(f"final_fig/Fig_1/hists/purple_new/{name}_{metab}.png")
            plt.show()
            plt.clf()
        x=5