import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
import datetime as dt


def update_delay(value):
    current_time = pd.to_datetime(value["Time"], format="%I:%M %p")
    status = value["Status"].split(" ")
    if len(status) > 1:
        if status[1] != "to":
            arrival_time = pd.to_datetime(
                status[1] + " " + status[2], format="%I:%M %p"
            )
            return pd.Timedelta(abs(current_time - arrival_time)).seconds / 60
    else:
        return 0


def update_status(value):
    """
    0 : Landed
    1 : Canceled
    2 : Diverted
    """

    status = value.split(" ")
    if status[0] == "Landed":
        return 0
    elif status[0] == "Canceled":
        return 1
    else:
        return 2


data = pd.read_csv("AirplaneData26-01-2020.csv")
data["delay"] = data[["Time", "Status"]].apply(update_delay, 1)
data["Status"] = data["Status"].apply(update_status, 1)
print(data.head(100))
