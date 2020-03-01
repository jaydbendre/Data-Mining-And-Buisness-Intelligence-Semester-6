import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import calendar

sns.set(style="whitegrid")

def week(value):
    value = datetime.datetime.strptime(value,"%Y-%m-%d %H:%M:%S")
    # return calendar.day_name[value.date().weekday()]
    return value.date().weekday()

data = pd.read_csv("Datasets/FinalMergedDataset/cleaned_dataset.csv")
data = pd.DataFrame(data[["Time","Delay"]])
data["day"] = data["Time"].apply(week,1)
data = pd.DataFrame(data[["Delay","day"]])
print(data.head())

# rs = np.random.RandomState(365)
# values = rs.randn(365, 4).cumsum(axis=0)
# dates = pd.date_range("1 1 2016", periods=365, freq="D")
# data = pd.DataFrame(values, dates, columns=["A", "B", "C", "D"])
# data = data.rolling(7).mean()

sns.lineplot(x="day",y="Delay",data = data ,palette="tab10", linewidth=2.5)
plt.show()