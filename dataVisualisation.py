import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import geoplotlib
from geoplotlib.utils import read_csv
from geopy.geocoders import Nominatim
data = pd.read_csv("Datasets/FinalMergedDataset/cleaned_dataset.csv")

data = pd.DataFrame(data)

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


# visualize()
des_src()