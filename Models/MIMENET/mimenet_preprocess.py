import pandas as pd
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
if __name__ == '__main__':
    data_name = "WANG_ESRD_2020"
    if data_name == "BGU":
        bgu = pd.read_csv("Data/Ben_Gurion/tax_4_relative_mean.csv",index_col=0)
        bgu = bgu.rename(columns=RR)
        bgu.index = [f"{int(i[-3:])}_0" if "PBLN" in i else f"{int(i[-3:])}_{int(i[-6:-4])}" for i in bgu.index]
        bgu_me = pd.read_csv("Data/Ben_Gurion/metabolites_with_formula.csv",index_col=0).T
        bgu_tag = pd.read_csv("Data/Ben_Gurion/OSHRIT_li_binary_DIRECT_PLUS.csv",index_col=0)
        bgu_tag.index = [f"{int(i[-3:])}_0" if "PBLN" in i else f"{int(i[-3:])}_{int(i[-6:-4])}" for i in bgu_tag.index]
        bgu_tag = bgu_tag.squeeze()
        common = list(bgu.index.intersection(bgu_tag.index))
        bgu = bgu.loc[common]
        bgu_tag = bgu_tag.loc[common]
        bgu_me = bgu_me.loc[common]

        bgu = bgu.T
        bgu_me = bgu_me.T

        bgu.to_csv("mimenet_data/Ben_Gurion/micro.csv")
        bgu_me.to_csv("mimenet_data/Ben_Gurion/metab.csv")
        bgu_tag.to_csv("mimenet_data/Ben_Gurion/tag.csv")

    elif data_name == "Parkinson":
        otu = pd.read_csv("Data/Parkinson_linoy/otu_relative_mean_rare_bact_5_tax_4.csv", index_col=0)
        otu.columns = [i.replace("; ", ";") for i in otu.columns]
        otu.index = [int(i[2:]) for i in otu.index]
        otu = otu.T
        # otu.index = [i[:-2] for i in otu.index]
        otu = otu.groupby(otu.index).mean()
        otu = otu.T
        metab = pd.read_csv("Data/Parkinson/metab_with_formula.csv", index_col=0)
        del metab['Name']
        del metab["formula.1"]
        metab = metab.groupby(metab.index, observed=True).mean()
        metab = metab.T
        metab.index = [int(i) for i in metab.index]
        tag = pd.read_csv("Data/Parkinson_linoy/parkinson_or_control.csv", index_col=0)
        tag[tag.values == "P"] = 1.0
        tag[tag.values == "C"] = 0.0



        x=4

    elif data_name == "Schizofrenia":
        otu = pd.read_csv("Data/Schizofrenia/tax_4_relative_mean.csv", index_col=0)
        otu.columns = [i.replace("d_", "k_").replace("_A", "") for i in otu.columns]
        otu = otu.rename(columns={
            'k__Bacteria;p__Bacteroidota;c__Bacteroidia;o__Bacteroidales': 'k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bacteroidales'})
        otu = otu.rename(columns={
            'k__Bacteria;p__Bacteroidota;c__Bacteroidia;o__Bacteroidales': 'k__Bacteria;p__Bacteroidetes;c__Bacteroidia;o__Bacteroidales'})
        otu_cols = [i.replace("d_", "k_").replace("_A", "").replace("_C", "") for i in otu.columns]
        otu = otu.T
        otu.index = otu_cols
        # otu.index = [i[:-2] for i in otu.index]
        otu = otu.groupby(otu.index).mean().T

        metab = pd.read_csv("Data/schizo_metabolites_without_problematic_signs.csv", index_col=0)
        metab = metab[metab.columns[3:-3]]
        metab = metab.groupby(metab.index).mean()
        metab.index = set([i.replace(" ", "") for i in metab.index])
        metab = metab.T
        metab.index = [i.split(":")[1].split(".")[0].replace(" ", "") for i in metab.index]
        tag = pd.DataFrame(data=[i[0] for i in otu.index], index=otu.index, columns=["tag"])
        tag[tag["tag"] == "P"] = 1.0
        tag[tag["tag"] == "C"] = 0.0

        adj_np = np.ones(shape=(len(metab.columns), len(otu.columns)))
        adj = pd.DataFrame(data=adj_np, columns=list(otu.columns), index=list(metab.columns))

    elif data_name == "Poyet":
        otu = pd.read_csv("Data/Poyet_efrat/poyet_otu_log_subpca_zscore_row_tax4.csv", index_col=0)
        otu = otu.T
        otu.index = [i[:-2] for i in otu.index]
        otu = otu.groupby(otu.index).mean().T

        metab = pd.read_csv("Data/Poyet_efrat/poyet_metab_with_formula_.csv", index_col=0)
        metab.index = metab["formula"]
        del metab["Samples"]
        del metab["formula"]
        metab = metab.fillna(metab.mean().mean())
        metab = metab.groupby(metab.index, observed=True).mean()
        metab = metab.T
        metab["tag_ind"] = [i.split("-")[0] for i in metab.index]

        tag = pd.read_csv("Raw_Data/poyet_efrat/poyet_meta_data.csv", index_col=0)  # ["Weight (kg)"].dropna()
        tag = metab.join(tag, on=metab["tag_ind"])
        tag = tag["Weight (kg)"]
        del metab["tag_ind"]
        adj_np = np.ones(shape=(len(metab.columns), len(otu.columns)))
        adj = pd.DataFrame(data=adj_np, columns=list(otu.columns), index=list(metab.columns))


    elif data_name == "Kim":
        otu = pd.read_csv("Data/Kim_efrat/kim_otu_relative_mean_tax4.csv", index_col=0)
        otu = otu.T
        # otu.index = [i[:-2] for i in otu.index]
        otu = otu.groupby(otu.index).mean().T

        metab = pd.read_csv("Data/Kim_efrat/kim_formula_.csv", index_col=0)
        metab.index = metab["formula"]
        del metab["Biochemical"]
        del metab["Superpathway"]
        del metab["Subpathway"]
        del metab["Chem ID"]
        del metab["formula"]
        metab = metab.groupby(metab.index, observed=True).mean()
        metab = metab.T

        tag = pd.read_csv("Data/Kim_efrat/kim_meta_data.csv", index_col=0)
        tag = tag.T
        # make binary groups
        tag[tag["Group"] == "Control"] = 0.0
        tag[tag["Group"] != 0.0] = 1.0
        tag = tag["Group"]

        adj_np = np.ones(shape=(len(metab.columns), len(otu.columns)))
        adj = pd.DataFrame(data=adj_np, columns=list(otu.columns), index=list(metab.columns))

    elif data_name == "Jacob":
        otu = pd.read_csv("Data/Jacob_efrat/jacob_otu_relative_mean_tax4.csv", index_col=0)
        otu = otu.T
        # otu.index = [i[:-2] for i in otu.index]
        otu = otu.groupby(otu.index).mean().T

        metab_map = pd.read_csv("Data/Jacob_efrat/Jacob_formula_.csv", index_col=0)
        metab = pd.read_csv("Raw_Data/jacobs_efrat/Metabolites_normalized_POS.csv", index_col=0)
        common_m = list(set(metab_map.index).intersection(set(metab.index)))
        metab_map = metab_map.loc[common_m]
        metab = metab.loc[common_m]
        metab.index = metab_map["formula"]
        metab = metab.loc[metab.index.dropna()]
        metab = metab.groupby(metab.index, observed=True).mean()
        metab = metab.T

        tag = pd.read_csv("Data/Jacob_efrat/Pediatric_family_cohort_map.csv", index_col=0)
        # make binary groups
        tag[tag["IBD_Status"] == "Normal"] = 0.0
        tag[tag["IBD_Status"] != 0.0] = 1.0
        tag = tag["IBD_Status"]

        adj_np = np.ones(shape=(len(metab.columns), len(otu.columns)))
        adj = pd.DataFrame(data=adj_np, columns=list(otu.columns), index=list(metab.columns))

    elif data_name == "He":
        otu = pd.read_csv("Data/he_efrat/fixed_tax_4_relative_mean.csv", index_col=0)
        otu = otu.T
        # otu.index = [i[:-2] for i in otu.index]
        otu = otu.groupby(otu.index).mean().T

        metab = pd.read_csv("Data/he_efrat/he_metabolites_with_formula_T.csv", index_col=0)
        metab = metab.groupby(metab.index, observed=True).mean()
        metab = metab.T

        tag = pd.read_csv("Raw_Data/HE_INFANTS_MFGM_efrat/63189_mapping_file__small.csv", index_col=0)
        # make binary groups
        tag[tag["diet"] == "Breast milk"] = 0.0
        tag[tag["diet"] == "Standard infant formula"] = 1.0
        tag[tag["diet"] == "Experimental infant formula"] = 2.0

        tag = tag["diet"]
        tag.index = [i[6:].replace(".", "-") for i in tag.index]

    elif data_name == "ERAWIJANTARI_GASTRIC_CANCER_2020":
        otu = pd.read_csv("Data/ERAWIJANTARI_GASTRIC_CANCER_2020/tax4_relative_mean.csv", index_col=0)
        otu = otu.T
        # otu.index = [i[:-2] for i in otu.index]
        otu = otu.groupby(otu.index).mean().T

        metab = pd.read_csv("Data/ERAWIJANTARI_GASTRIC_CANCER_2020/metab.csv", index_col=0)
        metab = metab.groupby(metab.index, observed=True).mean()
        metab = metab.T

        tag = pd.read_csv("Raw_Data/ERAWIJANTARI_GASTRIC_CANCER_2020/metadata.tsv", index_col=0,sep="\t")
        # make binary groups
        tag["Study.Group"][tag["Study.Group"] == "Healthy"] = 0.0
        tag["Study.Group"][tag["Study.Group"] == "Gatrectonomy"] = 1.0

        tag.index = tag["Sample"]
        tag = tag["Study.Group"]

    elif data_name == "YACHIDA_CRC_2019":
        otu = pd.read_csv(f"Data/{data_name}/tax4_relative.csv", index_col=0)
        otu = otu.T
        # otu.index = [i[:-2] for i in otu.index]
        otu = otu.groupby(otu.index).mean().T

        metab = pd.read_csv(f"Data/{data_name}/metab.csv", index_col=0)
        metab = metab.groupby(metab.index, observed=True).mean()
        metab = metab.T

        tag = pd.read_csv(f"Raw_Data/{data_name}/metadata.tsv", index_col=0,sep="\t")
        # make binary groups
        tag["Study.Group"][tag["Study.Group"] == "Healthy"] = 0.0
        tag["Study.Group"][tag["Study.Group"] == "Gatrectonomy"] = 1.0

        tag.index = tag["Sample"]
        tag = tag["Study.Group"]

    elif data_name == "FRANZOSA_IBD_2019":
        otu = pd.read_csv(f"Data/{data_name}/tax4_relative_mean.csv", index_col=0)
        otu = otu.T
        # otu.index = [i[:-2] for i in otu.index]
        otu = otu.groupby(otu.index).mean().T

        metab = pd.read_csv(f"Data/{data_name}/metab.csv", index_col=0)
        metab = metab.groupby(metab.index, observed=True).mean()
        metab = metab.T

        tag = pd.read_csv(f"Raw_Data/{data_name}/metadata.tsv", index_col=0,sep="\t")
        # make binary groups
        tag["Study.Group"][tag["Study.Group"] == "Healthy"] = 0.0
        tag["Study.Group"][tag["Study.Group"] == "Gatrectonomy"] = 1.0

        tag.index = tag["Sample"]
        tag = tag["Study.Group"]

    elif data_name == "iHMP_IBDMDB_2019":
        otu = pd.read_csv(f"Data/{data_name}/tax4_relative_mean.csv", index_col=0)
        otu = otu.T
        # otu.index = [i[:-2] for i in otu.index]
        otu = otu.groupby(otu.index).mean().T

        metab = pd.read_csv(f"Data/{data_name}/metab.csv", index_col=0)
        metab = metab.groupby(metab.index, observed=True).mean()
        metab = metab.T

        tag = pd.read_csv(f"Raw_Data/{data_name}/metadata.tsv", index_col=0,sep="\t")
        # make binary groups
        tag["Study.Group"][tag["Study.Group"] == "nonIBD"] = 0.0
        tag["Study.Group"][tag["Study.Group"]!=0.0] = 1.0

        tag.index = tag["Sample"]
        tag = tag["Study.Group"]

    elif data_name == "WANG_ESRD_2020":
        otu = pd.read_csv(f"Data/{data_name}/tax4_relative_mean.csv", index_col=0)
        otu = otu.T
        # otu.index = [i[:-2] for i in otu.index]
        otu = otu.groupby(otu.index).mean().T

        metab = pd.read_csv(f"Data/{data_name}/metab.csv", index_col=0)
        metab = metab.groupby(metab.index, observed=True).mean()
        metab = metab.T

        tag = pd.read_csv(f"Raw_Data/{data_name}/metadata.tsv", index_col=0,sep="\t")
        # make binary groups
        tag["Study.Group"][tag["Study.Group"] == "nonIBD"] = 0.0
        tag["Study.Group"][tag["Study.Group"]!=0.0] = 1.0

        tag.index = tag["Sample"]
        tag = tag["Study.Group"]

    elif data_name == "MARS_IBS_2020":
        otu = pd.read_csv(f"Data/{data_name}/tax4_relative_mean.csv", index_col=0)
        otu = otu.T
        # otu.index = [i[:-2] for i in otu.index]
        otu = otu.groupby(otu.index).mean().T

        metab = pd.read_csv(f"Data/{data_name}/metab.csv", index_col=0)
        metab = metab.groupby(metab.index, observed=True).mean()
        metab = metab.T

        tag = pd.read_csv(f"Raw_Data/{data_name}/metadata.tsv", index_col=0,sep="\t")
        # make binary groups
        tag["Study.Group"][tag["Study.Group"] == "nonIBD"] = 0.0
        tag["Study.Group"][tag["Study.Group"]!=0.0] = 1.0

        tag.index = tag["Sample"]
        tag = tag["Study.Group"]


    otu = otu.T
    metab = metab
    otu.to_csv(f"mimenet_data/{data_name}/BGU_micro.csv")
    metab.to_csv(f"mimenet_data/{data_name}/BGU_metab.csv")
    tag.to_csv(f"mimenet_data/{data_name}/tag.csv")
