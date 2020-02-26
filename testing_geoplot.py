import pandas as pd
import geopandas
import numpy as np
import json
from gcmap import GCMapper,Gradient
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize , LinearSegmentedColormap , PowerNorm
from geopy.geocoders import Nominatim
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
location_data["des_long"] = location_data["Source"].apply(des_long,1)

print(location_data.head())

airport_data = location_data.groupby(["source_lat","source_long","des_lat","des_long"]).size()
airport_data = airport_data.reset_index()
airport_data.columns = ("source_lat","source_long","des_lat","des_long","count")
grad = Gradient(((0, 0, 0, 0), (0.5, 204, 0, 153), (1, 255, 204, 230)))

gcm = GCMapper(cols=grad,height = 2000,width=4000)
gcm.set_data(airport_data["source_lat"],airport_data["source_long"],airport_data["des_lat"],airport_data["des_long"],airport_data["count"])

img = gcm.draw()
img.save("output.png")