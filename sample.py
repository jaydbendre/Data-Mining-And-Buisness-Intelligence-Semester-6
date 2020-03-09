import pandas as pd
import random

df = pd.read_csv(
    "Datasets/FinalMergedDataset/cleaned_dataset.csv",
    skiprows=lambda i: i > 0 and random.random() > 0.01)

with open("Datasets/FinalMergedDataset/sample_dataset.csv", "w") as csv_file:
    df.to_csv(path_or_buf=csv_file, index=False)
