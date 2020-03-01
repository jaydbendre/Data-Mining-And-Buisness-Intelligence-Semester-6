import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime
import calendar
def get_day(value):
    value = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    return calendar.day_name[value.date().weekday()]

df = pd.read_csv("Datasets/FinalMergedDataset/cleaned_dataset.csv")

data = pd.DataFrame(df[
    [
        "Flight Name",
        "Time",
        "Delay"
    ]
])
data["Day"] = data["Time"].apply(get_day, 1)

data = data.groupby(["Flight Name","Day"])["Delay"].mean().reset_index()
data = data.sort_values(by=["Day"])
print(data)

fig = px.line(data,x="Day",y="Delay",color="Flight Name")
fig.write_html("per_week_delay.html",auto_open=True)
fig.show()