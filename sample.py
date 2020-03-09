import pandas as pd
import random


def delay_status(value):
    if value > 15:
        return "Delayed"
    else:
        return "On time"


df = pd.DataFrame(pd.read_csv(
    "Datasets/FinalMergedDataset/cleaned_dataset.csv",
    skiprows=lambda i: i > 0 and random.random() > 0.02)
)

df["Delay_Status"] = df["Delay"].apply(delay_status, 1)

with open("Datasets/FinalMergedDataset/sample_dataset.csv", "w") as csv_file:
    df.to_csv(path_or_buf=csv_file, index=False)
