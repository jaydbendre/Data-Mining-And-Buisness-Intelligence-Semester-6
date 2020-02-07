from datasetCleaner import dataCleaner
from datasetMerger import dataMerger
import seaborn as sns
import pandas as pd
import numpy as np


def main():

    # dataMerger()
    # dataCleaner()

    data = pd.read_csv("Datasets/FinalMergedDataset/cleaned_dataset.csv")

    data = pd.DataFrame(data)

    print("1. Printing data within the dataset")
    print(data)
    print("\n\n")

    print("2. Printing starting rows within the dataset")
    print(data.head())
    print("\n\n")

    print("3. Printing ending rows within the dataset")
    print(data.tail())
    print("\n\n")

    print("4. Description of the dataset")
    print(data.describe())
    print("\n\n")

    print("5. Number of flights per flight company")
    print(data["Flight Name"].value_counts())
    print("\n\n")

    print("6. 5 point summary of delay")
    Q1, median, Q3 = np.nanpercentile(data["Delay"], [25, 50, 75])
    min, max = data["Delay"].min(), data["Delay"].max()
    print(
        "1. Minimum Delay = {} \n2. Maximum Delay = {} \n3. Q1 = {}\n4. Median = {}\n5. Q3 = {}".format(
            min, max, Q1, median, Q3
        )
    )
    print("\n\n")

    print("7. Mode of delay ")
    print(data["Delay"].mode())
    print("\n\n")

    print("8. Correlation between numerical attributes")
    correlation = data.corr(method="pearson")
    print(correlation)


main()
