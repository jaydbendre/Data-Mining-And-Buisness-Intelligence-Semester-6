import pandas as pd
import geopandas
import numpy as np
import json
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import random 

# geolocator = Nominatim(user_agent="jaydbendre")
file = pd.read_csv("Datasets/FinalMergedDataset/cleaned_dataset.csv")

location_data = file[["Source","Destination"]]

# data = geopandas.tools.geocode(location_data.Source , provider="nominatim", user_agent="jaydbendre")
# print(data)

file = geopandas.read_file("Datasets/FinalMergedDataset/cleaned_dataset.csv")

unique_location = dict()
unique_set = set()

# for s in file.Source:
#     unique_set.add(s)

# for d in file.Destination:
#     unique_set.add(d)
# i=0
# for s in unique_set:
#     print("{}/{}".format(i,len(unique_set))) 
#     print(s)
#     location = geolocator.geocode(s)
#     print(location)
#     if location == None:
#         continue
#     unique_location[s] = {
#         "latitude" : location.latitude,
#         "longitude" : location.longitude
#     }
#     i+=1
    
# print(unique_location)

# with open("coords.json",'w') as json_file:
#     json.dump(unique_location,json_file)



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

# print(location_data.head())

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
# fig.show()

for i in range(len(airport_data)):
    fig.add_trace(
        go.Scattergeo(
            lon = [airport_data["source_long"][i],airport_data["des_long"][i]],
            lat = [airport_data["source_lat"][i],airport_data["des_lat"][i]],
            mode = "lines",
            line = dict(width =1,color = "rgb({},{},{})".format(random.randint(0,255),random.randint(0,255),random.randint(0,255))),
            # opacity = float(airport_data["count"][i])/float(airport_data["count"].max())
        )
    )    
    
fig.show()