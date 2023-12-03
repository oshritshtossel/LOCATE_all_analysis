import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
import numpy as np

def calculate_loglog_avg():
    bgu = pd.read_csv("final_fig/Fig_2/temp/log_BGU.csv",index_col=0)
    he = pd.read_csv("final_fig/Fig_2/temp/log_He.csv",index_col=0)
    jacob = pd.read_csv("final_fig/Fig_2/temp/log_Jacob.csv",index_col=0)
    kim = pd.read_csv("final_fig/Fig_2/temp/log_Kim.csv",index_col=0)
    poyet = pd.read_csv("final_fig/Fig_2/temp/log_Poyet.csv",index_col=0)
    all = pd.concat([bgu,he,jacob,kim,poyet])

def calculate_linear_avg():
    bgu = pd.read_csv("final_fig/Fig_2/temp/linear_BGU.csv",index_col=0)
    he = pd.read_csv("final_fig/Fig_2/temp/linear_He.csv",index_col=0)
    jacob = pd.read_csv("final_fig/Fig_2/temp/linear_Jacob.csv",index_col=0)
    kim = pd.read_csv("final_fig/Fig_2/temp/linear_Kim.csv",index_col=0)
    poyet = pd.read_csv("final_fig/Fig_2/temp/linear_Poyet.csv",index_col=0)
    all = pd.concat([bgu,he,jacob,kim,poyet])

if __name__ == '__main__':
    all = pd.read_csv("all_performances/all_metabolites_all_results.csv",index_col=0)
    calculate_loglog_avg()
    mpl.rc('font', family='Times New Roman')
    plt.figure(figsize=(6,4))
    height = [0.477,0.393,0.08, 0.118, 0.346, 0.08,0.1264]
    bars = ('LOCATE','Log\nnet\nwork','Linear\nnet\nwork', 'Sparse\nNED', 'Melo\nnnPan', 'Mime\nNet','m\nNODE')
    x_pos = np.arange(len(bars))
    yerr = [0.005,0.005,0.008,0.007,0.016,0.005,0.009]
    plt.bar(x_pos, height,  yerr=yerr, ecolor='black',capsize=10,color=["blue", "lightskyblue","lightsteelblue","orange","red","green","mediumpurple"])


    # Create names on the x-axis
    plt.xticks(x_pos, bars,fontsize=18)
    plt.yticks(fontsize=18)
    plt.ylabel("Average SCC",fontdict={"fontsize":20})
    plt.title(" ",fontsize=20)
    plt.tight_layout()

    plt.savefig("final_fig/revision/Fig_2/avg.png")

    # Show graph
    plt.show()


