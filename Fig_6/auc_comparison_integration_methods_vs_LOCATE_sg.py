import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
if __name__ == '__main__':
    ###############################################
    mpl.rc('font', family='Times New Roman')
    label_size = 20
    plt.rcParams['ytick.labelsize'] = 20
    mpl.rcParams['xtick.labelsize'] = label_size
    all = pd.read_csv("final_fig/revision/Fig_4_wgs/auc_locate_new.csv")
    dfp = all.pivot(index='class1', columns='class2', values='val')
    cols = ["LOCATE","Multiview","IntegratedLearner-mic.","IntegratedLearner-met.","IntegratedLearner-stacked","IntegratedLearner-concatenated"]
    dfp=dfp[cols]
    yerr = all.pivot(index='class1', columns='class2', values='se')
    dfp.plot(kind='bar', yerr=yerr,color=["cornflowerblue","orange","indianred","coral",'red',"maroon"],figsize=(20,5),capsize=2,rot=0)
    plt.ylabel("Average AUC",fontdict={"fontsize":20})
    plt.ylim([0.5, 1.1])
    plt.xlabel("")
    plt.legend(fontsize=20,ncol=3)
    plt.tight_layout()
    plt.savefig("final_fig/revision/Fig_4_wgs/auc_std_NEW1.png")
    plt.show()
    plt.close()