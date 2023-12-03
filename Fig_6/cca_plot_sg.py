import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
if __name__ == '__main__':
    ###############################################
    mpl.rc('font', family='Times New Roman')
    label_size = 15
    plt.rcParams['ytick.labelsize'] = 15
    mpl.rcParams['xtick.labelsize'] = label_size
    all = pd.read_csv("final_fig/Fig_4_sg/cca_std.csv")
    dfp = all.pivot(index='class1', columns='class2', values='val')
    cols = ["Mic","Met","LOCATE"]
    dfp=dfp[cols]
    yerr = all.pivot(index='class1', columns='class2', values='se')
    dfp.plot(kind='bar', yerr=yerr,color=["hotpink","gold","cornflowerblue"],figsize=(8,5),capsize=2,rot=0,legend=False)
    plt.ylabel("Average SCC",fontdict={"fontsize":15})
    plt.xlabel("")

    plt.tight_layout()
    plt.savefig("final_fig/Fig_4_sg/cca_std.png")
    plt.show()
    plt.close()

