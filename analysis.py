import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
# import json

data = np.loadtxt(open("Parkirisca_do_10_05_2022.csv", "r"), dtype=str, delimiter=",", skiprows=1)
parking_names = np.unique(data[:, 0])
all_parkings = np.array(tuple(data[data[:, 0] == name] for name in parking_names))
# all_parkings_json = dict()

print(all_parkings.shape)
print(all_parkings)
# Filter out empty data
empty_parkings = np.fromiter((not np.any(parking[:, 2].astype(int)) for parking in all_parkings), dtype=bool)
# print("Number of empty parkings: ", sum(1 for _ in filter(lambda x: x == True, empty_parkings)))

parkings = np.delete(all_parkings, empty_parkings, axis=0)


def filter_to_date(parkings, end_date):
    timestamp = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())
    for i, parking in enumerate(parkings):
        after_date = parking[:, 1].astype(int) > timestamp
        parkings[i] = np.delete(parking, after_date, axis=0)


def plot_parking(parking):
    name = parking[0][0]
    capacity = int(parking[parking[:, 3].astype(int) != 0][0][3])
    min_x, max_x = np.min(parking[:, 1].astype(int)), np.max(parking[:, 1].astype(int))
   
    # all_parkings_json[name] = {
    #     "timestamps": list(parking[:, 1]),
    #     "percent_occupied": list((parking[:, 3].astype(int) - parking[:, 2].astype(int)) / parking[:, 3].astype(int)),
    # }

    # X: date, Y: capacity - n_free_spots = n_occupied
    plt.plot(tuple(map(datetime.fromtimestamp, parking[:, 1].astype(int))), parking[:, 3].astype(
        int) - parking[:, 2].astype(int))
    plt.plot(tuple(map(datetime.fromtimestamp, (min_x, max_x))), (capacity, capacity), "k--")
    plt.gcf().autofmt_xdate()  # format the dates
    plt.xlabel("Datum")
    plt.ylabel("Stevilo zasedenih mest")
    plt.title(f"Parkirisce: {name}")
    plt.show()

filter_to_date(parkings, "2022-05-11")

for parking in parkings:
    if parking.size == 0:
        continue
    plot_parking(parking)
    
# with open('js.json', 'w') as f:
#     json.dump(all_parkings_json, f)
