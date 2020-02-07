from datasetCleaner import dataCleaner
from datasetMerger import dataMerger
import seaborn as sns
import pandas as pd
import numpy as np
from scipy.stats import chisquare, chi2_contingency


def main():

    dataMerger()
    dataCleaner()

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

    print("8. Median of delay ")
    print(data["Delay"].median())
    print("\n\n")

    print("9. Mean of delay ")
    print(data["Delay"].mean())
    print("\n\n")

    print("10. Correlation between numerical attributes")
    correlation = data.corr(method="pearson")
    print(correlation)
    print("\n\n")

    print("11. Generating a frequency table for Status and Flight Name")
    table = pd.crosstab(data["Flight Name"], data["Status"])
    print(table)
    print("\n\n")

    print("12. Chi Squared test on the data from the above table")
    chi, p, df1, expected = chi2_contingency(table)
    print("Chi-Squared Value = {0:3f} \n p value = {1:3f} ".format(chi, p))
    print("\n\n")

    print("13. Grouping Data by Flight Name ")
    flight_data = data.groupby(["Flight Name"])
    print(flight_data.describe())
    print("\n\n")

    print("14. Description of delay of the grouped data")
    print(flight_data["Delay"].describe())
    print("\n\n")

    print("15. Standard Deviation of Delay of grouped data")
    print(flight_data["Delay"].std().reset_index())
    print("\n\n")

    print("16. Finding median by aggregating data")
    print(flight_data["Delay"].aggregate(np.median).reset_index())
    print("\n\n")

    print("17. Finding mean by aggregating data")
    print(flight_data["Delay"].aggregate(np.mean).reset_index())
    print("\n\n")

    print("18. Printing total null values of the data ")
    print(data.isnull().sum())
    print("\n\n")


main()
