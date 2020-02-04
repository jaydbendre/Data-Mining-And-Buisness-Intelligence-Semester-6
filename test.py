import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
import datetime as dt
from scipy.stats import chisquare, chi2_contingency


def update_source(value):
    if value["type"] == "D":
        return "Mumbai"
    else:
        return value["Source"]


def update_destination(value):
    if value["type"] == "A":
        return "Mumbai"
    else:
        return value["Destination"]


def update_timestamp_init(value):
    timestamp = str(value["date"]) + " " + str(value["Time"])
    timestamp = pd.to_datetime(timestamp, format="%Y-%m-%d %H:%M:%S")
    return timestamp


def update_actual_time(value):
    status = value["Status"].split(" ")
    if len(status) == 3 and status[1] != "to":
        time = value["date"] + " " + status[1] + " " + status[2]
        timestamp = pd.to_datetime(time, format="%Y-%m-%d %I:%M %p")
        timedelta = timestamp - pd.to_datetime(
            value["date"], format="%Y-%m-%d %H:%M:%S"
        )
        if timedelta > dt.timedelta(hours=12):
            value["date"] = pd.to_datetime(
                value["date"], format="%Y-%m-%d"
            ) - dt.timedelta(days=1)
            value["date"] = value["date"].date()
            time = str(value["date"]) + " " + status[1] + " " + status[2]
            timestamp = pd.to_datetime(time, format="%Y-%m-%d %I:%M %p")
            timedelta = timestamp - pd.to_datetime(
                value["date"], format="%Y-%m-%d %H:%M:%S"
            )
        return timestamp
    else:
        return np.nan


def add_delay(value):
    if value["Actual_Time"] or value["Time"]:
        time = pd.to_datetime(value["Time"], format="%Y-%m-%d %H:%M:%S")
        actual_time = pd.to_datetime(value["Actual_Time"], format="%Y-%m-%d %H:%M:%S")
        return pd.Timedelta(abs(time - actual_time)).seconds / 60
    else:
        return np.nan


dataset = pd.read_csv("Datasets/FinalMergedDataset/dataset.csv")
df = pd.DataFrame(
    dataset[["Time", "date", "Source", "Flight Name", "Status", "type", "Destination"]]
)

df["Source"] = df[["Source", "type"]].apply(update_source, 1)
df["Destination"] = df[["Destination", "type"]].apply(update_destination, 1)
df["Time"] = df[["date", "Time"]].apply(update_timestamp_init, 1)
df["Actual_Time"] = df[["Time", "Status", "date"]].apply(update_actual_time, 1)
df = df.dropna()
df["Delay"] = df[["Time", "Actual_Time"]].apply(add_delay, 1)

cleaned_df = pd.DataFrame(df[["Source","Destination","type","Time","Actual_Time","Delay"]])
print(cleaned_df)
