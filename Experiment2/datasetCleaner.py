import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
import datetime as dt
from scipy.stats import chisquare, chi2_contingency

"""
Functions to update across the dataset
"""

"""
Update Departure Source in the dataset
"""


def update_source(value):
    if value["type"] == "D":
        return "Mumbai"
    else:
        return value["Source"]


"""
Update Arrival Destination in the dataset
"""


def update_destination(value):
    if value["type"] == "A":
        return "Mumbai"
    else:
        return value["Destination"]


"""
Convert String of date and time to timestamp
"""


def update_timestamp_init(value):
    timestamp = str(value["date"]) + " " + str(value["Time"])
    timestamp = pd.to_datetime(timestamp, format="%Y-%m-%d %H:%M:%S")
    return timestamp


def update_actual_time(value):
    # print(value["Status"])
    if type(value["Status"]) == type("String"):
        status = value["Status"].split(" ")
        if len(status) == 3 and status[1] != "to":
            time = value["date"] + " " + status[1] + " " + status[2]
            scheduled_time = pd.to_datetime(
                value["Time"], format="%Y-%m-%d %H:%M:%S")
            actual_time = pd.to_datetime(time, format="%Y-%m-%d %I:%M %p")

            threshold_date = pd.to_datetime(
                value["date"]+" "+"00:00:00", format="%Y-%m-%d %H:%M:%S")

            lb_threshold_date = pd.to_datetime(
                value["date"]+" "+"20:30:00", format="%Y-%m-%d %H:%M:%S")

            ub_threshold_date = pd.to_datetime(
                value["date"]+" "+"03:00:00", format="%Y-%m-%d %H:%M:%S")

            if actual_time <= ub_threshold_date and scheduled_time >= lb_threshold_date:
                actual_time = actual_time + dt.timedelta(days=1)
            elif scheduled_time <= ub_threshold_date and actual_time >= lb_threshold_date:
                actual_time = actual_time - dt.timedelta(days=1)
            timedelta = pd.Timedelta(actual_time - scheduled_time).seconds/3600
            return actual_time
        else:
            return np.nan
    else:
        return np.nan


def add_delay(value):
    time = pd.to_datetime(value["Time"], format="%Y-%m-%d %H:%M:%S")
    actual_time = pd.to_datetime(
        value["Actual_Time"], format="%Y-%m-%d %H:%M:%S")
    if pd.isnull(actual_time):
        return 0.0
    else:
        return pd.Timedelta(abs(time - actual_time)).seconds / 60


def update_status(value):
    if value != np.nan and type(value) == type("String"):
        value = value.split(" ")[0]
        return value
    else:
        return -9999


def dataCleaner():
    dataset = pd.read_csv("../Datasets/FinalMergedDataset/dataset.csv")
    df = pd.DataFrame(
        dataset[
            ["Time", "date", "Source", "Flight Name",
                "Status", "type", "Destination"]
        ]
    )

    # print(df["Status"])
    df["Source"] = df[["Source", "type"]].apply(update_source, 1)
    df["Destination"] = df[["Destination", "type"]].apply(
        update_destination, 1)
    df["Time"] = df[["date", "Time"]].apply(update_timestamp_init, 1)
    df["Actual_Time"] = df[["Time", "Status", "date"]].apply(
        update_actual_time, 1)
    # df = df.dropna()
    df["Status"] = df["Status"].apply(update_status, 1)
    map_dict = {
        "Landed": 0,
        "Departed": 1,
        "Unknown": 2,
        "Diverted": 3,
        "Canceled": 4,
        "Estimated": -1,
    }
    df["Status"] = df.Status.replace(map_dict)
    df["Status"] = df["Status"].astype(int)
    df["Delay"] = df[["Time", "Actual_Time"]].apply(add_delay, 1)
    # df = df.dropna()
    cleaned_df = pd.DataFrame(
        df[
            [
                "Source",
                "Destination",
                "Flight Name",
                "type",
                "Status",
                "Time",
                "Actual_Time",
                "Delay",
            ]
        ]
    )

    with open("../Datasets/FinalMergedDataset/cleaned_dataset.csv", "w") as f:
        cleaned_df.to_csv(path_or_buf=f, index=False)


dataCleaner()
