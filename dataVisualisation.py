import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
data = pd.read_csv("Datasets/FinalMergedDataset/cleaned_dataset.csv")

data = pd.DataFrame(data)


def visualize():
    graph_1 = sns.scatterplot(
        x=data.Time,
        y=data.Delay,
        hue=data.Delay,
        palette="ch:r=-.2,d=.3_r",
        sizes=(1, 8),
        hue_order=data.Delay,
    )
    plt.show()


visualize()
