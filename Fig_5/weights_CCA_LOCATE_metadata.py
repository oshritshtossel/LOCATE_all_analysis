import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
if __name__ == '__main__':
    mpl.rc('font', family='Times New Roman')
    name ="BGU"#"BGU"#"Jacob"#"Kim""He"#"Poyet"
    df = pd.read_csv(f"met_contribution/for_meta_plot/{name}_MERGE_1.csv",index_col=0)#.T[["Age","Diet","Pet allergy","Relationship status","Sex","Country Birth","BMI","Height","Weight","Seasonal Pollen allergy","Travel abroad last year"
#]].T
    #df = df.rename(index={'BGU': 'Direct Plus'})
    # list_colors=["darkred","red","tomato","coral","sandybrown","orange","gold","yellow","greenyellow","limegreen","green","teal","dodgerblue","royalblue","blue","darkblue","blueviolet","darkviolet","mediumorchid","orchid"]
    # list_colors = ["blue","cornflowerblue","dodgerblue","teal","green","limegreen","greenyellow"]
    #list_colors= ["orchid","mediumorchid","darkviolet","blueviolet","darkblue","blue","dodgerblue","royalblue","cornflowerblue","lightskyblue","lightsteelblue","darkcyan","forestgreen","teal","seagreen","green","springgreen","lime","limegreen","greenyellow","y","yellow"]#poyet
    #list_colors.reverse()
    # POYET
    #list_colors = ["cornflowerblue","midnightblue","mediumblue","blue","royalblue","steelblue","dodgerblue","deepskyblue","skyblue","lightskyblue","lightblue","powderblue","c","seagreen","mediumseagreen","darkgreen","g","forestgreen","limegreen","lime","springgreen","lawngreen","palegreen","olivedrab","greenyellow","yellowgreen"]
    list_colors = ["cornflowerblue","midnightblue","mediumblue","blue","seagreen","mediumseagreen","darkgreen","g"]
    single = ["cornflowerblue","seagreen"]
    df.plot.barh(stacked=True,color=list_colors,legend=False,figsize=(5,5))
    #df.plot.barh(stacked=True,color=single,legend=False,figsize=(5,5))
    plt.xlabel("Absolute weight (CCA)",fontdict={"fontsize": 15})
    plt.title(name.replace("ERAWIJANTARI_GASTRIC_CANCER_2020", "ERAWIJANTARI"),fontdict={"fontsize": 20},fontweight="bold")
    #plt.title(name.replace("FRANZOSA_IBD_2019", "FRANZOSA"),fontdict={"fontsize": 20},fontweight="bold")
    #plt.title(name.replace("WANG_ESRD_2020", "WANG"), fontdict={"fontsize": 20}, fontweight="bold")
    #plt.title(name, fontdict={"fontsize": 20}, fontweight="bold")
    #plt.title("Direct Plus",fontdict={"fontsize": 20},fontweight="bold")
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.tight_layout()
    #plt.savefig(f"met_contribution/for_meta_plot/{name}_MERGE.png")
    plt.savefig(f"final_fig/Fig_4/meta/{name}_MERGE1.png")
    plt.show()