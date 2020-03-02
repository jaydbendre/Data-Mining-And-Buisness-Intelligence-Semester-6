import plotly.graph_objects as go
import numpy as np
import pandas as pd

df = pd.read_csv("../../Datasets/FinalMergedDataset/cleaned_dataset.csv")

data = pd.DataFrame(df[
    [
        "Delay",
        "type"
    ]
])

y0 = data[data["type"] == "A"]
y1 = data[data["type"] == "D"]

y0 = y0[y0["Delay"] <= 400]
y1 = y1[y1["Delay"] <= 400]

fig = go.Figure()
fig.add_trace(go.Box(y=y0["Delay"]))
fig.add_trace(go.Box(y=y1["Delay"]))

fig.write_html("Output/box.html", auto_open=True)

fig.show()
