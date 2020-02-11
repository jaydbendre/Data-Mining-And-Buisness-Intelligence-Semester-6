import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import geoplotlib
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time
data = pd.read_csv("Datasets/FinalMergedDataset/cleaned_dataset.csv")

data = pd.DataFrame(data)
geolocator = Nominatim()

geocode = RateLimiter(geolocator.geocode,min_delay_seconds=1)
data['s_loc'] = data["Source"].apply(geocode)
data['point'] = data['s_loc'].apply(lambda loc : tuple(loc.point) if loc else None)
data[["s_lat","s_lon","altitude"]] = pd.DataFrame(data["point"].tolist(),index=data.index)

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
