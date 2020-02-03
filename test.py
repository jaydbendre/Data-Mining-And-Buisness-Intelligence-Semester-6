import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
import datetime as dt
from scipy.stats import chisquare, chi2_contingency


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

    status = value["Status"].split(" ")
    if status[0] == "Landed" and value["delay"] == 0:
        return "On-Time"
    elif status[0] == "Landed" and value["delay"] > 0:
        return "Delayed"
    elif status[0] == "Canceled":
        return "Canceled"
    else:
        return "Diverted"


def insert_date(value):
    date = value.split(" ")
    if len(date) > 1 and date[1] != "to":
        return pd.to_datetime(date[1] + " " + date[2], format="%I:%M %p").time()
    else:
        return np.nan


#No Invalid Bytes
data = pd.read_csv("Datasets/Arrivals/AirplaneData26-01-2020.csv", encoding = 'utf8')

# DataFrame is like a subset of the dataset so redudant columns have been removed
data = pd.DataFrame(data[["Time", "Source", "Flight Name", "Status"]])
data["delay"] = data[["Time", "Status"]].apply(update_delay, 1)
data["Arrival"] = data["Status"].apply(insert_date, 1)
data["Status"] = data[["Status", "delay"]].apply(update_status, 1)
change_time = lambda x: pd.to_datetime(x, format="%I:%M %p").time()
data["Time"] = data["Time"].map(change_time)


print("Dataset for airplane traffic in Mumbai")
print(data.head(500))
print("\n\n")
# DATASET READY FOR OPERATIONS
print("Description of the dataset")
print(data.describe())
print("\n\n")
print("Shape of the dataset")
print(data.shape)
print("\n\n")
print("Number of data points : ")
print(data.size)
print("\n\n")
print("Number of null Values column wise ")
print(data.isnull().sum())
print("\n\n")
print("Number of flights per Airline Agency")
print(data["Flight Name"].value_counts())
print("\n\n")
print("5 Point summary of the data on the basis of delay time of the flights")
Q1, median, Q3 = np.nanpercentile(data["delay"], [25, 50, 75])
min, max = data["delay"].min(), data["delay"].max()
print(
    "Min : {} \nMax : {}\nQ1 : {}\nQ3 : {}\nMedian : {}".format(
        min, max, Q1, Q3, median
    )
)
print("\n\n")
print("Finding correlation between Status and delay")
relation = data.corr(method="pearson")
print(relation)
print("\n\n")
print("Frequency Table for category and type")
table = pd.crosstab(data["Flight Name"], data["Status"])
print(table)
print("\n\n")
print("Chi Squared test to find out whether flight name and flight status are related")
chi, p, df1, expected = chi2_contingency(table)
print("Chi Square value = {0:0.3f}\np value = {1:0.3f}".format(chi, p))
print("\n\n")
print("Grouped data by Flight Name")
grouped_data = data.groupby(["Flight Name"])
print("Grouped Data")
print(grouped_data.describe())
print("\n\n")
print("Description of the grouped data delay")
print(grouped_data["delay"].describe())
print("\n\n")
print("Mean delay offered by per flight company")
print(grouped_data["delay"].mean().sort_values(ascending=False))
