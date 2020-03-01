import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import random 

file = pd.read_csv("Datasets/FinalMergedDataset/cleaned_dataset.csv")

location_data = file[["Source","Destination"]]

unique_location = dict()
unique_set = set()

with open("coords.json","r") as json_file:
    unique_location = json.load(json_file)
    
def source_lat(data):
    if data in unique_location.keys():
        return unique_location[data]["latitude"]
    else:
        return np.nan

def source_long(data):
    if data in unique_location.keys():
        return unique_location[data]["longitude"]
    else:
        return np.nan

def des_lat(data):
    if data in unique_location.keys():
        return unique_location[data]["latitude"]
    else:
        return np.nan

def des_long(data):
    if data in unique_location.keys():
        return unique_location[data]["longitude"]
    else:
        return np.nan

location_data["source_lat"] = location_data["Source"].apply(source_lat,1)
location_data["source_long"] = location_data["Source"].apply(source_long,1)
location_data["des_lat"] = location_data["Destination"].apply(des_lat,1)
location_data["des_long"] = location_data["Destination"].apply(des_long,1)

airport_data = location_data.groupby(["Source","Destination","source_lat","source_long","des_lat","des_long"]).size()
airport_data = airport_data.reset_index()
airport_data.columns = ("Source","Destination","source_lat","source_long","des_lat","des_long","count")
print(airport_data.head())
fig=go.Figure()
print(airport_data["source_long"])
fig.add_trace(go.Scattergeo(
    lon = airport_data["source_long"],
    lat = airport_data["source_lat"],
    hoverinfo = "text",
    text= airport_data["Source"],
    mode = "markers",
    marker = dict(
        size=10,
        color="rgb(255,0,0)",
        line = dict(
            width=3,
            color = "rgba(68,68,68,0)"
        )
    )
))
fig.add_trace(go.Scattergeo(
    lon = airport_data["des_long"],
    lat = airport_data["des_lat"],
    hoverinfo = "text",
    text= airport_data["Destination"],
    mode = "markers",
    marker = dict(
        size=10,
        color="rgb(52,55,235)",
        line = dict(
            width=3,
            color = "rgba(68,68,68,0)"
        )
    )
))

for i in range(len(airport_data)):
    fig.add_trace(
        go.Scattergeo(
            lon = [airport_data["source_long"][i],airport_data["des_long"][i]],
            lat = [airport_data["source_lat"][i],airport_data["des_lat"][i]],
            mode = "lines",
            line = dict(width =1,color = "rgb({},{},{})".format(random.randint(0,255),random.randint(0,255),random.randint(0,255))),
        )
    )    
    
fig.write_html("test.html",auto_open=True)
# fig.show()