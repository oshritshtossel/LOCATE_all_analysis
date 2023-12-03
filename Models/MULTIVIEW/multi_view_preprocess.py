import pandas as pd
def RR(org):
    A = org.split(";")
    final = ""
    for a, f in zip(A, ("k__", "p__", "c__", "o__","f__","g__","s__")):
        if a != f:
            final += f + a
        else:
            final += a
        final += ";"

    return final[:-1]

def prepare_data_sets(data_name):
    if data_name == "BGU":
        otu = pd.read_csv("Data/Ben_Gurion/BGU_relative_otu_tax_7.csv", index_col=0)
        otu = otu.rename(columns=RR)
        otu.index = [f"{int(i[-3:])}_0" if "PBLN" in i else f"{int(i[-3:])}_{int(i[-6:-4])}" for i in otu.index]
        otu = otu.T
        # otu.index = [i[:-2] for i in otu.index]
        otu = otu.groupby(otu.index).mean()
        otu = otu.T
        metab = pd.read_csv("Data/Ben_Gurion/metabolites_with_formula.csv", index_col=0).T
        #tag = pd.read_csv("Data//Ben_Gurion/dsc_tag_raw.csv",index_col=0)
        #tag = pd.read_csv("Data//Ben_Gurion/ssc_tag_raw.csv",index_col=0)
        tag = pd.read_csv("Data//Ben_Gurion/vat_tag_raw.csv",index_col=0)
        #tag = pd.read_csv("Data//Ben_Gurion/OSHRIT_li_binary_DIRECT_PLUS.csv", index_col=0)
        #tag = pd.read_csv("Data//Ben_Gurion/dsc_tag_raw.csv", index_col=0)
        #tag = pd.read_csv("Data//Ben_Gurion/vat_tag_raw.csv", index_col=0)
        #tag = pd.read_csv("Data//Ben_Gurion/ssc_tag_raw.csv", index_col=0)
        tag.index = [f"{int(i[-3:])}_0" if "PBLN" in i else f"{int(i[-3:])}_{int(i[-6:-4])}" for i in tag.index]
        tag["time"] = [i.split("_")[1] for i in tag.index]
        tag = tag[tag["time"]=="18"]
        del tag["time"]
        p=0


    elif data_name == "Poyet":
        otu = pd.read_csv("Data/Poyet_efrat/poyet_otu_relative_mean_tax7.csv", index_col=0)
        otu = otu.T
        otu.index = [i[:-2] for i in otu.index]
        otu = otu.groupby(otu.index).mean().T
    ################# all #################3
        # metab = pd.read_csv("Data/Poyet_efrat/poyet_metab_with_formula_.csv", index_col=0)
        # metab.index = metab["formula"]
        # del metab["Samples"]
        # del metab["formula"]
        # metab = metab.fillna(metab.mean().mean())
        # metab = metab.groupby(metab.index, observed=True).mean()
        # metab = metab.T
        ####################################
        #classified
        metab = pd.read_csv("Data/Poyet_efrat/metab_classified.csv",index_col=0)
        metab = metab.fillna(metab.median())
        ############################
        metab["tag_ind"] = [i.split("-")[0] for i in metab.index]

        tag = pd.read_csv("Raw_Data/poyet_efrat/poyet_meta_data.csv", index_col=0)  # ["Weight (kg)"].dropna()
        tag = metab.join(tag, on=metab["tag_ind"])
        tag = tag["Age"]#["Age"]
        # tag[tag.values=="Male"]=1.0
        # tag[tag.values=="Female"]=0.0
        del metab["tag_ind"]

    #
    elif data_name == "ERAWIJANTARI_GASTRIC_CANCER_2020":
        #otu = pd.read_csv("Data/ERAWIJANTARI_GASTRIC_CANCER_2020/tax4_log_subpca_zscore_row.csv", index_col=0)# tax 4
        otu = pd.read_csv("Data/ERAWIJANTARI_GASTRIC_CANCER_2020/tax7_relative_mean.csv", index_col=0)# tax 7
        otu = otu.T
        otu.index = [i[:-2] for i in otu.index]
        otu = otu.groupby(otu.index).mean().T

        metab = pd.read_csv("Data/ERAWIJANTARI_GASTRIC_CANCER_2020/metab.csv", index_col=0)

        metab = metab.fillna(metab.mean().mean())
        metab = metab.groupby(metab.index, observed=True).mean()
        #metab = metab.T

        tag = pd.read_csv("Raw_Data/ERAWIJANTARI_GASTRIC_CANCER_2020/metadata.tsv", index_col=0,
                          sep="\t")  # ["Weight (kg)"].dropna()

        tag["Study.Group"][tag["Study.Group"] == "Healthy"] = 0.0
        tag["Study.Group"][tag["Study.Group"] == "Gastrectomy"] = 1.0

        tag.index = tag["Sample"]
        tag = tag["Study.Group"]

    elif data_name == "YACHIDA_CRC_2019":
        otu = pd.read_csv("Data/YACHIDA_CRC_2019/tax7_relative.csv", index_col=0)# tax 4
        #otu = pd.read_csv("Data/YACHIDA_CRC_2019/tax7_log_subpca_zscore_row.csv", index_col=0)# tax 7
        otu = otu.T
        otu.index = [i[:-2] for i in otu.index]
        otu = otu.groupby(otu.index).mean().T

        metab = pd.read_csv("Data/YACHIDA_CRC_2019/metab.csv", index_col=0)

        metab = metab.fillna(metab.mean().mean())
        metab = metab.groupby(metab.index, observed=True).mean()
        #metab = metab.T

        tag = pd.read_csv("Raw_Data/YACHIDA_CRC_2019/metadata.tsv", index_col=0,
                          sep="\t")  # ["Weight (kg)"].dropna()

        tag["Study.Group"][tag["Study.Group"] == "Healthy"] = 0.0
        tag["Study.Group"][tag["Study.Group"]!=0.0] = 1.0

        tag.index = tag["Sample"]
        tag = tag["Study.Group"]

    #
    elif data_name == "FRANZOSA_IBD_2019":
        #otu = pd.read_csv("Data/FRANZOSA_IBD_2019/tax4_log_subpca_zscore_row.csv", index_col=0)# tax 4
        otu = pd.read_csv("Data/FRANZOSA_IBD_2019/tax7_relative_mean.csv", index_col=0)# tax 7
        otu = otu.T
        otu.index = [i[:-2] for i in otu.index]
        otu = otu.groupby(otu.index).mean().T

        #metab = pd.read_csv("Data/FRANZOSA_IBD_2019/metab.csv", index_col=0)
        metab = pd.read_csv("Data/FRANZOSA_IBD_2019/metab_classified.csv", index_col=0)

        metab = metab.fillna(metab.mean().mean())
        metab = metab.groupby(metab.index, observed=True).mean()
        #metab = metab.T

        tag = pd.read_csv("Raw_Data/FRANZOSA_IBD_2019/metadata.tsv", index_col=0,
                          sep="\t")  # ["Weight (kg)"].dropna()

        tag["Study.Group"][tag["Study.Group"] == "Control"] = 0.0
        tag["Study.Group"][tag["Study.Group"]!=0.0] = 1.0

        tag.index = tag["Sample"]
        tag = tag["Study.Group"]

    #
    elif data_name == "MARS_IBS_2020":
        otu = pd.read_csv("Data/MARS_IBS_2020/tax7_relative_mean.csv", index_col=0)# tax 4
        #otu = pd.read_csv("Data/MARS_IBS_2020/tax7_log_subpca.csv", index_col=0)# tax 7
        otu = otu.T
        otu.index = [i[:-2] for i in otu.index]
        otu = otu.groupby(otu.index).mean().T

        metab = pd.read_csv("Data/MARS_IBS_2020/metab.csv", index_col=0)

        metab = metab.fillna(metab.mean().mean())
        metab = metab.groupby(metab.index, observed=True).mean()
        #metab = metab.T

        tag = pd.read_csv("Raw_Data/MARS_IBS_2020/metadata.tsv", index_col=0,
                          sep="\t")  # ["Weight (kg)"].dropna()

        tag["Study.Group"][tag["Study.Group"] == "H"] = 0.0
        tag["Study.Group"][tag["Study.Group"]!=0.0] = 1.0

        tag.index = tag["Sample"]
        tag = tag["Study.Group"]

    #
    elif data_name == "WANG_ESRD_2020":
        #otu = pd.read_csv("Data/WANG_ESRD_2020/tax4_log_subpca_zscore_row.csv", index_col=0)# tax 4
        otu = pd.read_csv("Data/WANG_ESRD_2020/tax7_relative_mean.csv", index_col=0)# tax 7
        otu = otu.T
        otu.index = [i[:-2] for i in otu.index]
        otu = otu.groupby(otu.index).mean().T

        #metab = pd.read_csv("Data/WANG_ESRD_2020/metab.csv", index_col=0)
        metab = pd.read_csv("Data/WANG_ESRD_2020/metab_classified.csv", index_col=0)

        metab = metab.fillna(metab.mean().mean())
        metab = metab.groupby(metab.index, observed=True).mean()
        #metab = metab.T

        tag = pd.read_csv("Raw_Data/WANG_ESRD_2020/metadata.tsv", index_col=0,
                          sep="\t")  # ["Weight (kg)"].dropna()

        tag["Study.Group"][tag["Study.Group"] == "Control"] = 0.0
        tag["Study.Group"][tag["Study.Group"]!=0.0] = 1.0

        tag.index = tag["Sample"]
        tag = tag["Study.Group"]

    elif data_name == "Jacob":
        otu = pd.read_csv("Data/Jacob_efrat/jacob_otu_relative_mean_tax7.csv", index_col=0)
        otu = otu.T
        otu = otu.groupby(otu.index).mean().T

        metab = pd.read_csv("Data/Jacob_efrat/metab_classified.csv",index_col=0)

        tag = pd.read_csv("Data/Jacob_efrat/Pediatric_family_cohort_map.csv", index_col=0)
        # make binary groups
        tag[tag["IBD_Status"] == "Normal"] = 0.0
        tag[tag["IBD_Status"] != 0.0] = 1.0
        tag = tag["IBD_Status"]


    #
    elif data_name == "He":
        #otu = pd.read_csv("Data/he_efrat/he_tax4_subpca_zscore_row.csv", index_col=0)# tax 4
        otu = pd.read_csv("Data/he_efrat/he_tax7_relative_mean.csv", index_col=0)# tax 7
        otu = otu.T
        # otu.index = [i[:-2] for i in otu.index]
        otu = otu.groupby(otu.index).mean().T
        otu.index = [i[6:].replace(".", "-") for i in otu.index]

        metab = pd.read_csv("Data/he_efrat/he_metabolites_with_formula_T.csv", index_col=0)
        metab = metab.groupby(metab.index, observed=True).mean()
        metab = metab.T

        tag = pd.read_csv("Raw_Data/HE_INFANTS_MFGM_efrat/63189_mapping_file__small.csv", index_col=0)
        # make binary groups
        tag[tag["diet"] == "Breast milk"] = 0.0
        tag[tag["diet"] == "Standard infant formula"] = 0.0
        tag[tag["diet"] == "Experimental infant formula"] = 1.0

        tag = tag["diet"]
        tag.index = [i[6:].replace(".", "-") for i in tag.index]



    # take common values
    common  = list(otu.index.intersection(metab.index).intersection(tag.index))
    otu = otu.loc[common]
    metab = metab.loc[common]
    tag = tag.loc[common]


    return otu, metab, tag
if __name__ == '__main__':
    NAME = "BGU"
    o,m,t = prepare_data_sets(NAME)
    #t = t.groupby(t.index).first() # FOR YACHIDA
    o.to_csv(f"multiview/{NAME}/VAT18/otu.csv")
    m.to_csv(f"multiview/{NAME}/VAT18/metab.csv")
    t.to_csv(f"multiview/{NAME}/VAT18/tag.csv")
    #t.to_csv(f"multiview/{NAME}/dsc0.csv")

    c=0