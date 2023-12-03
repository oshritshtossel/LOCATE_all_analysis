import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from scipy.stats import entropy, spearmanr
import matplotlib as mpl
import numpy as np

def RR(org):
    A = org.split(";")
    final = ""
    for a, f in zip(A, ("k__", "p__", "c__", "o__")):
        if a != f:
            final += f + a
        else:
            final += a
        final += ";"

    return final[:-1]

def pad(l, size, padding):
    return l + [padding] * abs((len(l)-size))

def Average(lst):
    return sum(lst) / len(lst)


def load_data(name, folder):
    if name == "BGU":
        coef_matrix = pd.read_csv(f"{folder}/BGU.csv", index_col=0)
        micro = pd.read_csv("Data/Ben_Gurion/tax_4_relative_mean.csv", index_col=0)
        micro = micro.rename(columns=RR).dropna()

    elif name == "He":
        coef_matrix = pd.read_csv(f"{folder}/He.csv", index_col=0)
        micro = pd.read_csv("Data/he_efrat/fixed_tax_4_relative_mean.csv", index_col=0)

    elif name == "Kim":
        coef_matrix = pd.read_csv(f"{folder}/BGU.csv", index_col=0)
        micro = pd.read_csv("Data/Kim_efrat/kim_otu_relative_mean_tax4.csv", index_col=0)
        micro = micro.T
        micro = micro.groupby(micro.index).mean().T
        common = list(micro.columns.intersection(coef_matrix.columns))
        micro = micro[common]
        coef_matrix = coef_matrix[common]

    elif name == "Jacob":
        coef_matrix = pd.read_csv(f"{folder}/Jacob.csv", index_col=0)
        micro = pd.read_csv("Data/Jacob_efrat/jacob_otu_relative_mean_tax4.csv", index_col=0)

    return micro, coef_matrix


def calculate_vals_and_exps(coef_matrix, plot_=False):
    dict_of_exp = dict()
    dict_of_entropy = dict()
    list_df_freq = list()
    for metab in coef_matrix.iterrows():
        temp = metab[1].sort_values(ascending=False)[:10]
        relative = micro[temp.index]
        list_of_freq = list()
        for sample in relative.iterrows():
            most_freq = list(sample[1].index)[sample[1].argmax()]
            list_of_freq.append(most_freq)
        df_of_freq = pd.DataFrame.from_dict(Counter(list_of_freq), orient='index').reset_index()
        df_of_freq["freq"] = df_of_freq[0] / len(micro.index)
        df_of_freq["coef"] = [i for i in (coef_matrix.loc[metab[0]].T)[list(df_of_freq.index)].values]
        list_df_freq.append(df_of_freq)
    all = pd.concat(list_df_freq)
    fig, ax = plt.subplots(figsize=(4, 4))
    min1 = all["coef"].min()
    max1 = all["coef"].max()
    min2 = all["freq"].min()
    max2 = all["freq"].max()

    lims = [
        np.min([np.log(min1+0.00001), np.log(min2+0.00001)]),  # min of both axes
        np.max([np.log(max1+0.00001), np.log(max2+0.00001)]),  # max of both axes
    ]
    plt.figure(figsize=(5, 5))
    scc = spearmanr(np.log(all["freq"]+0.00001),np.log(all["coef"]+0.00001))[0]
    ax.scatter(np.log(all["coef"]+0.00001),np.log(all["freq"]+0.00001),label=f"SCC:{round(scc,3)}",color="blueviolet")
    ax.tick_params(axis='both', which='major', labelsize=15)
    ax.set_xlabel("log(coefficient)",fontdict={"fontsize":20})
    ax.set_ylabel("log(fraction in population)",fontdict={"fontsize":20})
    # ax.set_xscale("log")
    # ax.set_yscale("log")
    ax.legend(prop={'size': 12})
    ax.set_title(" ",fontdict={"fontsize":25})
    fig.tight_layout()
    fig.savefig("final_fig/Fig_1/coef_freq_scatter.png")
    plt.show()


    return df_of_entropy



if __name__ == '__main__':
    mpl.rc('font', family='Times New Roman')
    plot_ = False
    folder= "draft_fig/shannon"
    real_folder = "check_yoram_hypothesis_coef"
    shuffled_folder = "check_yoram_hypothesis_coef_shuffled"
    for name in ["He"]:  # "BGU","Jacob","Parkinson","He"
        micro, coef_matrix = load_data(name, real_folder)
        shuffled_micro, shuffled_coef_matrix = load_data(name, shuffled_folder)
        # df_for_hist = pd.DataFrame(index=coef_matrix.index,columns=["Bacteria","Relative coef"])
        df_of_entropy= calculate_vals_and_exps(coef_matrix,plot_=True)

        df_of_shuffeled = calculate_vals_and_exps(shuffled_coef_matrix,plot_=False)
        plt.hist(df_of_entropy.values, bins=30, label="Real", alpha=0.5, edgecolor='black',color="blue")#darkorchid
        plt.hist(df_of_shuffeled.values, bins=30, label="Shuffled", alpha=0.5, edgecolor='black',color="grey")
        plt.xlabel("Shannon entropy",fontdict={"fontsize":15})
        plt.ylabel("Frequency",fontdict={"fontsize":15})
        plt.title(name,fontdict={"fontsize":20})
        plt.legend()
        plt.savefig(f"{folder}/hist_of_shannon/{name}.png")
        plt.show()



    x = 3
