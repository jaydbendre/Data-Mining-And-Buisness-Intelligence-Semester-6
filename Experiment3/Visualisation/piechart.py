import plotly.express as px
import pandas as pd

df = pd.read_csv("../../Datasets/FinalMergedDataset/cleaned_dataset.csv")

dataframe = pd.DataFrame(df[["Flight Name"]])
dataframe = dataframe.groupby(dataframe["Flight Name"]).size().reset_index()
dataframe.columns = ("Flight Name", "Count")
print(dataframe)

fig = px.pie(dataframe, values=dataframe["Count"], names=dataframe['Flight Name'],
             color_discrete_sequence=px.colors.sequential.RdBu)
fig.write_html("Output/pie.html", auto_open=True)
fig.show()
