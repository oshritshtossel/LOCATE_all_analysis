import seaborn as sns
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from statannot import add_stat_annotation
import numpy as np

if __name__ == '__main__':
    mpl.rc('font', family='Times New Roman')
    mpl.rcParams['axes.spines.right'] = False
    mpl.rcParams['axes.spines.left'] = False
    folder = "final_fig/Fig_1/exp_coef_data"
    WGS = True
    for name in ["FRANZOSA_IBD_2019","ERAWIJANTARI_GASTRIC_CANCER_2020","YACHIDA_CRC_2019","WANG_ESRD_2020","MARS_IBS_2020"]:
        df_to_plot = pd.read_csv(f"{folder}/{name}.csv", index_col=0)

        plt.figure(figsize=(3,5))  # Adjust the figure size as needed

        # Create a swarm plot
        ax = sns.swarmplot(data=df_to_plot, palette=["blueviolet", "mediumpurple"], zorder=0, alpha=0.75)

        # Create bar plots extending till the median
        medians = df_to_plot.median()
        x_coords = np.arange(len(medians))
        plt.bar(x_coords , medians, width=0.3, color=["blueviolet", "mediumpurple"], alpha=0.3)

        # Create box plots
        boxes = [df_to_plot["Real"], df_to_plot["Shuffled"]]
        ax = sns.boxplot(data=boxes, boxprops={'facecolor': 'None'})

        # Add statistical annotations
        test_results = add_stat_annotation(ax, data=pd.DataFrame(data=boxes, index=["A", "B"]).T,
                                           box_pairs=[("A", "B")],
                                           perform_stat_test=True,
                                           test="t-test_ind", text_format='star',
                                           loc='inside', verbose=2)

        plt.xticks(ticks=np.arange(2), labels=["Real", f"Shuffled"], fontsize=20, family='Times New Roman')
        if WGS:
            if name == "ERAWIJANTARI_GASTRIC_CANCER_2020":
                plt.title(name.replace("ERAWIJANTARI_GASTRIC_CANCER_2020", " "), fontsize=22,
                      family='Times New Roman',
                      fontweight="bold")
            elif name == "YACHIDA_CRC_2019":
                plt.title(name.replace("YACHIDA_CRC_2019", "YACHIDA"), fontsize=30,
                          family='Times New Roman',
                          fontweight="bold")
            elif name == "FRANZOSA_IBD_2019":
                plt.title(name.replace("FRANZOSA_IBD_2019", "FRANZOSA"), fontsize=30,
                          family='Times New Roman',
                          fontweight="bold")
            elif name == "WANG_ESRD_2020":
                plt.title(name.replace("WANG_ESRD_2020", "WANG"), fontsize=30,
                          family='Times New Roman',
                          fontweight="bold")
            elif name == "MARS_IBS_2020":
                plt.title(name.replace("MARS_IBS_2020", "MARS"), fontsize=30,
                          family='Times New Roman',
                          fontweight="bold")
        else:
            plt.title(name.replace("BGU", "Direct Plus"), fontsize=25, family='Times New Roman', fontweight="bold")
        if WGS:
            if name != "ERAWIJANTARI_GASTRIC_CANCER_2020":
                plt.setp(ax.get_yticklabels(), visible=False)
                plt.yticks([])
        else:
            if name != "He":
                plt.setp(ax.get_yticklabels(), visible=False)
                plt.yticks([])
        # for the most left one
        if WGS:
            if name == "ERAWIJANTARI_GASTRIC_CANCER_2020":
                plt.yticks(fontsize=15)
                # Add left border
                ax.spines['left'].set_visible(True)
                ax.spines['left'].set_linewidth(1.5)
        else:
            if name == "He":
                plt.ylabel("Expectation of coefficients", family='Times New Roman', fontdict={"fontsize": 20})
                plt.yticks(fontsize=15)
                # Add left border
                ax.spines['left'].set_visible(True)
                ax.spines['left'].set_linewidth(1.5)

        # for the most right one
        if WGS:
            if name == "YACHIDA_CRC_2019":
                # Add right border
                ax.spines['right'].set_visible(True)
                ax.spines['right'].set_linewidth(1.5)
        else:
            if name == "Poyet":
                # Add right border
                ax.spines['right'].set_visible(True)
                ax.spines['right'].set_linewidth(1.5)
        if WGS:
            plt.ylim((0.7, 1.1))
        else:
            plt.ylim((0.4, 1.1))
        plt.tight_layout()

        if WGS:
            plt.savefig(f"final_fig/revision/Fig_1/swarms_bars/WGS/{name}.png", dpi=300)
        else:
            plt.savefig(f"final_fig/revision/Fig_1/swarms_bars/{name}.png", dpi=300)
        plt.show()
