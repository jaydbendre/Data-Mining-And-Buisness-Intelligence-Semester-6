import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import geoplotlib
<<<<<<< HEAD
from geoplotlib.utils import read_csv
from geopy.geocoders import Nominatim
=======
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time
>>>>>>> a7e05b65433c1cbf7bc726c06f33b1728782636a
data = pd.read_csv("Datasets/FinalMergedDataset/cleaned_dataset.csv")

data = pd.DataFrame(data)
geolocator = Nominatim()

<<<<<<< HEAD
geolocator = Nominatim(user_agent="localhost")

fun = lambda x : (geolocator.geocode(x).latitude,geolocator.geocode(x).longitude)
data["source_coords"] = data["Source"].apply(fun,1)
data["dest_coords"] = data["Destination"].apply(fun,1)

# data = read_csv('Datasets/FinalMergedDataset/cleaned_dataset.csv')
def des_src():
    geoplotlib.graph(data,
                    src_lat=data["source_coords"][0],
                    src_lon=data["source_coords"][1],
                    des_lat=data["dest_coords"][0],
                    des_lon=data["dest_coords"][1],
                    color='hot_r',
                    alpha=16,
                    linewidth=2)
    geoplotlib.show()
=======
geocode = RateLimiter(geolocator.geocode,min_delay_seconds=1)
data['s_loc'] = data["Source"].apply(geocode)
data['point'] = data['s_loc'].apply(lambda loc : tuple(loc.point) if loc else None)
data[["s_lat","s_lon","altitude"]] = pd.DataFrame(data["point"].tolist(),index=data.index)
>>>>>>> a7e05b65433c1cbf7bc726c06f33b1728782636a

# print(data)
print(data.head())
def visualize():
    graph_1 = sns.scatterplot(
        x=data.Time,
        y=data.Delay,
        hue=data.Delay,
        palette="ch:r=-.2,d=.3_r",
        sizes=(1, 8),
        hue_order=data.Delay,
    )
    plt.show()


<<<<<<< HEAD
# visualize()
des_src()
=======
def geographical_map():
    
    geoplotlib.graph(data,
                 src_lat='lat_departure',
                 src_lon='lon_departure',
                 dest_lat='lat_arrival',
                 dest_lon='lon_arrival',
                 color='hot_r',
                 alpha=16,
                 linewidth=2)
    geoplotlib.show()
# visualize()
>>>>>>> a7e05b65433c1cbf7bc726c06f33b1728782636a
