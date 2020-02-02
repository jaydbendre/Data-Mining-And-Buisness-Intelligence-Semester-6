# import numpy as np
# import pandas as pd
# from sklearn.impute import SimpleImputer
# from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
# import datetime as dt

# df = pd.read_csv("AirplaneData26-01-2020.csv")
# file = pd.DataFrame({"Status": df["Status"]})
# file.replace(to_replace=, value=r"^Unknown", regex=True)
# print(file["Status"][48])
# # def update_status(value):
# #     current_time = pd.to_datetime(value["Time"], format="%I:%M %p")
# #     arrival_time_array = value["Status"].split(" ")
# #     value["Status"] = arrival_time_array[0].replace("Unknown",np.Nan)
# #     if len(arrival_time_array) > 1:
# #         arrival_time = pd.to_datetime(
# #             arrival_time_array[1] + " " + arrival_time_array[2], format="%I:%M %p"
# #         )
# #         pd.Timedelta(current_time - arrival_time).seconds


# # def clean_csv():
# #     df = pd.read_csv("AirplaneData26-01-2020.csv")
# #     df["Status"] = df[["Time", "Status"]].apply(update_status, 1)


# # def operations():
# #     df = pd.read_csv("AirplaneData26-01-2020.csv")
# #     ##head() prints first 5 tuples of the csv file in tabular form
# #     print("df.head()")
# #     print(df.head())
# #     print("\n\n")
# #     print("df.head(10)")
# #     print(df.head(10))
# #     print("\n\n")
# #     # tail() prints last 5 tuples of the csv files
# #     print("df.tail()")
# #     print(df.tail())
# #     print("\n\n")
# #     print("df.tail(10)")
# #     print(df.tail(10))
# #     # shape prints the number of rows and columns
# #     print("\n\n")
# #     print(df.shape)
# #     # size print rows * column
# #     print("\n\n")
# #     print(df.size)
# #     # columns print column headers in the dataset
# #     print("\n\n")
# #     print(df.columns)
# #     # to print specific columns
# #     print("\n\n")
# #     print(df["Status"])
# #     print(df["Status"][:10])


# # clean_csv()
# # # operations()


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


def insert_date(value):
    date = value.split(" ")
    if len(date) > 1 and date[1] != "to":
        return pd.to_datetime(date[1] + " " + date[2], format="%I:%M %p").time()
    else:
        return np.nan


data = pd.read_csv("Datasets/AirplaneData26-01-2020.csv")
data = pd.DataFrame(data[["Time", "Source", "Flight Name", "Status"]])
data["delay"] = data[["Time", "Status"]].apply(update_delay, 1)
data["Arrival"] = data["Status"].apply(insert_date, 1)
data["Status"] = data["Status"].apply(update_status, 1)
change_time = lambda x: pd.to_datetime(x, format="%I:%M %p").time()
data["Time"] = data["Time"].map(change_time)
print(data.head(500))
