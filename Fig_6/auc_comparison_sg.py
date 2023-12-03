import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
if __name__ == '__main__':
    ###############################################
    mpl.rc('font', family='Times New Roman')
    label_size = 16
    plt.rcParams['ytick.labelsize'] = 20
    mpl.rcParams['xtick.labelsize'] = label_size

    all = pd.read_csv("final_fig/revision/Fig_4_wgs/org_auc.csv")
    dfp = all.pivot(index='class1', columns='class2', values='val')
    cols = ["Mic. iMic","Mic., meta iMic","Mic. , Met. iMic","Met. LR","Log-log LR","Z LOCATE LR","Z LOCATE, meta LR"]
    dfp=dfp[cols]
    yerr = all.pivot(index='class1', columns='class2', values='se')
    dfp.plot(kind='bar', yerr=yerr,color=["hotpink","mediumvioletred","goldenrod","gold","lightskyblue","cornflowerblue","darkblue"],figsize=(8,5),capsize=2,rot=0)
    plt.ylabel("Average AUC",fontdict={"fontsize":20})
    plt.ylim([0.5, 1.1])
    plt.xlabel("")
    plt.legend(bbox_to_anchor=(0.48,0.5),fontsize=14)#,ncol=2
    plt.tight_layout()
    plt.savefig("final_fig/revision/Fig_4_wgs/auc_std_new.png")
    plt.show()
    plt.close()

