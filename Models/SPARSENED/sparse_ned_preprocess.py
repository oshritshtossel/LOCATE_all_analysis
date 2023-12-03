import pandas as pd
import numpy as np
def log_normalization(as_data_frame, eps_for_zeros):
    as_data_frame += eps_for_zeros
    as_data_frame = np.log10(as_data_frame)
    return as_data_frame


def prepare_jacob():
    metab_map = pd.read_csv("Data/Jacob_efrat/Jacob_formula_.csv", index_col=0)
    metab = pd.read_csv("Raw_Data/jacobs_efrat/Metabolites_normalized_POS.csv", index_col=0)
    common_m = list(set(metab_map.index).intersection(set(metab.index)))
    metab_map = metab_map.loc[common_m]
    metab = metab.loc[common_m]
    metab.index = metab_map["formula"]
    metab = metab.loc[metab.index.dropna()]
    return metab

def prepare_kim():
    metab = pd.read_csv("Data/Kim_efrat/kim_formula_.csv", index_col=0)
    metab.index = metab["formula"]
    del metab["Biochemical"]
    del metab["Superpathway"]
    del metab["Subpathway"]
    del metab["Chem ID"]
    del metab["formula"]
    return metab

def prepare_parkinson():
    metab = pd.read_csv("Data/Parkinson/metab_with_formula.csv", index_col=0)
    del metab['Name']
    del metab["formula.1"]
    return metab



if __name__ == '__main__':
    he = pd.read_csv("Data/he_efrat/he_metabolites_with_formula_T.csv",index_col=0)
    jacob = prepare_jacob()
    kim = prepare_kim()
    bgu = pd.read_csv("Data/Ben_Gurion/metabolites_with_formula.csv", index_col=0)
    parkinson = prepare_parkinson()
    x=5