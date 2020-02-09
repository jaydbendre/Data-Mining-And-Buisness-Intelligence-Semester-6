"""
Main Purpose of this program is to merge all the dataset files into one dataset as dataset is available on a day basis and not a aggregate dataset
"""
import os
import pandas as pd

"""
Updates the string to time
"""


def update_time(value):
    time = pd.to_datetime(value, format="%I:%M %p").time()
    return time


def dataMerger():
    file_path = os.path.join(os.getcwd(), "Datasets")
    i = 0

    folder_name = ["Arrivals", "Departures"]
    arrival_path = file_path + "\\" + folder_name[0]
    departure_path = file_path + "\\" + folder_name[1]

    arrival_files = [
        file
        for file in os.listdir(arrival_path)
        if os.path.isfile(os.path.join(arrival_path, file))
    ]

    departure_files = [
        file
        for file in os.listdir(departure_path)
        if os.path.isfile(os.path.join(departure_path, file))
    ]

    file = pd.DataFrame()

    """
    Merges all the files and adds dates to the dataset
    """
    for arrival, departure in zip(arrival_files, departure_files):

        date = pd.to_datetime(arrival[12:-4], format="%d-%m-%Y").date()

        arrival_file = pd.DataFrame(
            pd.read_csv(arrival_path + "\\" + arrival, encoding="utf8")[
                ["Time", "Source", "Flight Name", "Status"]
            ]
        )
        departure_file = pd.DataFrame(
            pd.read_csv(departure_path + "\\" + departure, encoding="utf8")[
                ["Time", "Destination", "Flight Name", "Status"]
            ]
        )
        arrival_file["date"] = date
        arrival_file["type"] = "A"
        departure_file["date"] = date
        departure_file["type"] = "D"

        arrival_file["Time"] = arrival_file["Time"].apply(update_time, 1)
        departure_file["Time"] = departure_file["Time"].apply(update_time, 1)
        merged = arrival_file.append(departure_file, sort=False)
        file = file.append(merged, sort=False)
        file.sort_values(["date", "Time"], axis=0, inplace=True)
        # print(file)
        # file = file.append(file)

    with open(
        os.path.join(os.getcwd(), "Datasets\\FinalMergedDataset\\dataset.csv"), "w"
    ) as csv_file:
        file.to_csv(path_or_buf=csv_file, index=False)

    file = pd.DataFrame(
        pd.read_csv(
            os.path.join(os.getcwd(), "Datasets\\FinalMergedDataset\\dataset.csv")
        )
    )


dataMerger()
