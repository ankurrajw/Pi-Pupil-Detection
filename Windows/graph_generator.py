import matplotlib.pyplot as plt
import pandas as pd
import os
import glob


folder_path = r'PATH_FOLDER'

def graph_generation(path):
    """Generate graph for experimentation
    1. loss mean
    2. sigma
    """

    path_mean = glob.glob(path + r'\*loss_mean_*.csv')
    path_sigma = glob.glob(path + r'\*loss_sigma_*.csv')

    if len(path_sigma) > 1 or len(path_mean) > 1:
        print('more than one files for threshold calculation')
        return

    mean_data = pd.read_csv(path_mean[0], index_col=0)
    sigma_data = pd.read_csv(path_sigma[0], index_col=0)
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(20, 20))

    ax[0].set_xlabel("threshold")
    ax[0].set_ylabel("loss mean")
    ax[0].set_title("mean distribution of loss")
    ax[0].grid()
    ax[1].set_xlabel("threshold")
    ax[1].set_ylabel("STD or sigma loss")
    ax[1].set_title("sigma distribution of loss")
    ax[1].grid()
    for label in mean_data.index:
        ax[0].plot(mean_data.columns, mean_data.loc[label], label=label, linewidth=2)
        ax[1].plot(sigma_data.columns, sigma_data.loc[label], label=label, linewidth=2)
    ax[0].legend(title="kernel size", loc='center left', bbox_to_anchor=(1, 0.5))
    ax[1].legend(title="kernel size", loc='center left', bbox_to_anchor=(1, 0.5))

    fig.suptitle(f'File name - {os.path.basename(path_mean[0])} & {os.path.basename(path_sigma[0])}', fontsize=16)
    plt.savefig(path + '/graph_loss_mean_sigma.png', bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    graph_generation(folder_path)
