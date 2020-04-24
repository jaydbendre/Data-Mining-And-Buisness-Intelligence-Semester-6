import pandas as pd

new_data = pd.DataFrame(pd.read_csv("Online Retail.csv"))

item_seq = dict()
# new_data = new_data[:600]
new_data["InvoiceNo"] = new_data["InvoiceNo"].astype("str")
def serialize_values(row):
    if row["InvoiceNo"] not in item_seq.keys():
        item_seq[row["InvoiceNo"]] = {}
        item_seq[row["InvoiceNo"]]["Description"]=list()
        item_seq[row["InvoiceNo"]]["Description"].append(row["Description"])
        
    else:
        item_seq[row["InvoiceNo"]]["Description"].append(row["Description"])

    return row

new_data = new_data.apply(serialize_values , 1)
print(item_seq)
import json
with open("values.json","w") as f:
    object_json = json.dumps([item_seq] , indent = 4)
    f.write(object_json)
