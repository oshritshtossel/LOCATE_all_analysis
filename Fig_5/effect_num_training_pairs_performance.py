import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
if __name__ == '__main__':
    ###############################################
    mpl.rc('font', family='Times New Roman')
    # generate diff dJacobfs
    #list_names=["Jacob","He"]#,"Poyet"
    list_names=["He"]#,"Poyet"#ERAWIJANTARI_GASTRIC_CANCER_2020 FRANZOSA_IBD_2019
    for data_name in list_names:
        plt.figure(figsize=(5,5))
        df = pd.read_csv(f"final_fig/Fig_4/number_samples/{data_name}.csv", index_col=0)# 16S
        #df = pd.read_csv(f"final_fig/Fig_4_sg/number_samples/{data_name}.csv", index_col=0)
        rep_contribution = df["REP-4"]-df["MICROBIOME"]
        met = df["METAB"] - df["MICROBIOME"]

        plt.plot(rep_contribution,label="Z LOCATE", marker='o',color="cornflowerblue")
        plt.title(data_name,fontweight="bold",fontdict={"fontsize":20})
        if data_name == "ERAWIJANTARI_GASTRIC_CANCER_2020":
            plt.title(data_name.replace("ERAWIJANTARI_GASTRIC_CANCER_2020", "ERAWIJANTARI"), fontsize=20,
                      family='Times New Roman',
                      fontweight="bold")
        elif data_name == "FRANZOSA_IBD_2019":
            plt.title(data_name.replace("FRANZOSA_IBD_2019", "FRANZOSA"), fontsize=20,
                      family='Times New Roman',
                      fontweight="bold")
        elif data_name == "WANG_ESRD_2020":
            plt.title(data_name.replace("WANG_ESRD_2020", "WANG"), fontsize=20,
                      family='Times New Roman',
                      fontweight="bold")
        plt.xlabel("Number of pairs",fontdict={"fontsize":20})

        plt.ylabel("AUC difference microbiome",fontdict={"fontsize":20})
        plt.axhline(y=0.0, color='hotpink',linewidth=4, linestyle='-',label="Mic.",zorder=0)
        plt.axhline(y=met[50], color='gold',linewidth=4, linestyle= '--',label="Met.",zorder=0)
        plt.yticks(fontsize=15)
        plt.xticks(fontsize=15)
        plt.ylim((-0.13,0.22))
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"final_fig/Fig_4_sg/number_samples/{data_name}_.png")
        plt.show()
    C=0
