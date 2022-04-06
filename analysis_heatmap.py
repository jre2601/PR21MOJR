import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import seaborn as sns

# TODO Heatmap visualization on an actual map

data = np.loadtxt(open("Parkirisca_do_04_04_2022.csv", "r"), dtype=str, delimiter=",", skiprows=1)
parking_names = np.unique(data[:, 0])

all_parkings = np.array(tuple(data[data[:, 0] == name] for name in parking_names))

# Filter out empty data
empty_parkings = np.fromiter((not np.any(parking[:, 2].astype(int)) for parking in all_parkings), dtype=bool)
parkings = np.delete(all_parkings, empty_parkings, axis=0)


def filter_to_date(parkings, end_date):
    timestamp = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())
    for i, parking in enumerate(parkings):
        after_date = parking[:, 1].astype(int) > timestamp
        parkings[i] = np.delete(parking, after_date, axis=0)
    return parkings


parkings = filter_to_date(parkings, "2022-03-15")
print(parkings)

park_map = {}
for parking in parkings:
    if len(parking) == 0:
        continue
    park_map[parking[0][0]] = tuple((int(p2[3]) - int(p2[2])) - (int(p1[3]) - int(p1[2])) for p1, p2 in zip(parking, parking[1:]))

# ax = sns.heatmap((park_map.keys(), park_map.values()), linewidth=0.5)
# plt.show()

def plot_parking_change(parking, park_map):
    name = parking[0][0]
    data = park_map[name]

    # X: date, Y: change in occupied places
    plt.plot(tuple(map(datetime.fromtimestamp, parking[:-1, 1].astype(int))), data)
    plt.gcf().autofmt_xdate()  # format the dates
    plt.xlabel("Datum")
    plt.ylabel("Sprememba zasedenih mest")
    plt.title(f"Parkirisce: {name}")
    plt.show()


for parking in parkings:
    if parking.size == 0:
        continue
    plot_parking_change(parking, park_map)
