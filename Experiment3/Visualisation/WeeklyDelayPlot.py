import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import calendar


def get_day(value):
    value = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    return calendar.day_name[value.date().weekday()]


data = pd.read_csv("../../Datasets/FinalMergedDataset/cleaned_dataset.csv")

data = pd.DataFrame(
    data[
        [
            "Time",
            "Delay"
        ]
    ]
)

data["Day"] = data["Time"].apply(get_day, 1)

sns.catplot(y="Day", x="Delay", data=data)
plt.show()
