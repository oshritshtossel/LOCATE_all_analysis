import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


def calculate_jaccard_index_between_2_groups(group_a, group_b):
    intersect_num = len(list(set(group_a.columns).intersection(set(group_b.columns))))
    union_num = len(list(set(group_a.columns).union(set(group_b.columns))))
    return intersect_num / union_num


def calculate_percent_of_common_bact(df, list_of_common, name=None):
    common = df[list_of_common]
    common = common.T
    common.index = [name.split(";")[-1] for name in common.index]
    common = common.groupby(common.index).mean()
    common.index = [i.split(".")[0] for i in common.index]
    common = common.groupby(common.index).mean()
    common = common.rename(index={'o__': 'Unclassified order'})
    common.index = [i.split("__")[-1]+" (o)" for i in common.index]
    common = common.T
    common[common.values > 1e-8] = 1.0
    percent = common.sum() / len(df.index)
    if name != None:
        percent.name = name
    return percent

def RR(org):
    A = org.split(";")
    final = ""
    for a,f in zip(A,("k__","p__","c__","o__")):
        if a != f:
            final+= f+a
        else:
            final+=a
        final += ";"

    return final[:-1]


if __name__ == '__main__':
    mpl.rc('font', family='Times New Roman')

    #################################
    # TAX 4 - RARE BACT 5
    ################################
    allergy = pd.read_csv("Data_after_process_jacard_index/Allergy/including_rare/otu_relative_mean_rare_bact_5_tax_4.csv",
                          index_col=0)

    ibd = pd.read_csv("Data_after_process_jacard_index/IBD/including_rare/otu_relative_mean_rare_bact_5_tax_4.csv", index_col=0)
    cirr = pd.read_csv("Data_after_process_jacard_index/Cirrhosis/including_rare/otu_relative_mean_rare_bact_5_tax_4.csv", index_col=0)

    male = pd.read_csv(
        "Data_after_process_jacard_index/Male_vs_female/including_rare/otu_relative_mean_rare_bact_5_tax_4.csv",
        index_col=0)
    gvhd = pd.read_csv("Data_after_process_jacard_index/gvhd/including_rare/otu_relative_mean_rare_bact_5_tax_4.csv", index_col=0)
    gdm = pd.read_csv("Data_after_process_jacard_index/GDM/including_rare/otu_relative_mean_rare_bact_5_tax_4.csv", index_col=0)
    allergy.columns = [i.replace("; ", ";") for i in allergy.columns]
    # delete duplicate bacterias
    allergy = ((allergy.T).groupby(allergy.columns).mean()).T
    ibd.columns = [i.replace("; ", ";") for i in ibd.columns]
    ibd = ((ibd.T).groupby(ibd.columns).mean()).T

    gvhd.columns = [i.replace("; ", ";") for i in gvhd.columns]
    gvhd = ((gvhd.T).groupby(gvhd.columns).mean()).T
    gdm.columns = [i.replace("; ", ";") for i in gdm.columns]
    gdm = ((gdm.T).groupby(gdm.columns).mean()).T
    # delete duplicate columns
    oy = pd.read_csv("Data_after_process_jacard_index/Elderly_vs_young/including_rare/otu_relative_mean_rare_bact_5_tax_4.csv",
                     index_col=0)
    par = pd.read_csv("Data_after_process_jacard_index/Parkinson/including_rare/otu_relative_mean_rare_bact_5_tax_4.csv", index_col=0)
    par.columns = [i.replace("; ", ";") for i in par.columns]
    par = ((par.T).groupby(par.columns).mean()).T
    sch = pd.read_csv("Data_after_process_jacard_index/Schizofrenia/including_rare/otu_relative_mean_rare_bact_5_tax_4.csv",
                      index_col=0)
    sch.columns = [i.replace("d_", "k_").replace("_A", "") for i in sch.columns]
    sch = ((sch.T).groupby(sch.columns).mean()).T
    bgu = pd.read_csv("Data_after_process_jacard_index/Ben_gurion/including_rare/otu_relative_mean_rare_bact_5_tax_4.csv", index_col=0)
    bgu = bgu.rename(columns=RR)
    bgu = ((bgu.T).groupby(bgu.columns).mean()).T
    j = calculate_jaccard_index_between_2_groups(male, ibd)
    list_of_common_bact = list(
        set(allergy.columns).intersection(set(ibd.columns)).intersection(set(cirr.columns)).intersection(
            set(male.columns)).intersection(
            (set(gvhd.columns)).intersection(set(gdm.columns))).intersection(set(oy.columns)).intersection(
            set(par.columns)).intersection(set(sch.columns)).intersection(set(bgu.columns)))



    #####################################################
    # calculate percent of common bact in each dataset
    ###################################################
    p_allergy = calculate_percent_of_common_bact(allergy, list(allergy.columns), "Allergy")
    p_ibd = calculate_percent_of_common_bact(ibd, list(ibd.columns), "IBD")
    p_cirr = calculate_percent_of_common_bact(cirr, list(cirr.columns), "Cirrhosis")

    p_male = calculate_percent_of_common_bact(male, list(male.columns), "MF")
    p_gvhd = calculate_percent_of_common_bact(gvhd, list(gvhd.columns), "GVHD")
    p_gdm = calculate_percent_of_common_bact(gdm, list(gdm.columns), "GDM")
    p_oy = calculate_percent_of_common_bact(oy, list(oy.columns), "Old vs young")
    p_par = calculate_percent_of_common_bact(par, list(par.columns), "Parkinson")
    p_sch = calculate_percent_of_common_bact(sch, list(sch.columns), "Schizofrenia")
    p_bgu = calculate_percent_of_common_bact(bgu, list(bgu.columns), "BGU")

    ######################
    # plot -common bacterias from 5 datasets
    ####################
    sum_all_datasets = p_ibd.add(p_cirr, fill_value=0.).add(p_male, fill_value=0.).add(p_gvhd, fill_value=0.).add(
        p_allergy, fill_value=0.).add(p_gdm, fill_value=0.).add(p_oy, fill_value=0.).add(p_par,
                                                                                         fill_value=0.).add(p_sch, fill_value=0.).add(p_bgu, fill_value=0.)
    sum_all_datasets.name = "SUM"
    all_series = pd.concat([p_allergy, p_gvhd, p_cirr, p_ibd, p_male, p_gdm, p_oy, p_par, p_sch,p_bgu,sum_all_datasets], axis=1)
    big_to_small = all_series.sort_values(["SUM"], ascending=False)
    del big_to_small["SUM"]

    big_to_small = big_to_small[:20]
    big_to_small.plot.barh(stacked=True, figsize=(7, 7),color=["darkred","red","orange","gold","yellow","greenyellow","limegreen","green","teal","royalblue","blue","darkblue","blueviolet","darkviolet","mediumorchid","orchid"])
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.legend(prop={'size': 12})
    plt.xlabel("Fraction",fontdict={"fontsize": 20})
    for rowNum, (_, row) in enumerate(big_to_small.iterrows()):
        xpos = 0
        for f, val in enumerate(row):
            if np.isnan(val):
                continue
            s_xpos = xpos
            e_xpos = xpos + val
            ps = (s_xpos + e_xpos) / 2
            plt.text(ps - (0.075 if f == 0 else 0.), rowNum - 0.1, str(round(val, 2)), color='black', fontsize=8)
            xpos += val

    plt.tight_layout()
    plt.savefig("core_micro_tax_4_.png")
    plt.show()
    x = 5
