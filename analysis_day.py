import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

data = np.loadtxt(open("Parkirisca_do_04_04_2022.csv", "r"), dtype=str, delimiter=",", skiprows=1)

parking_names = np.unique(data[:, 0])
parking_dates = np.unique(data[:, 1])

entries_in_day = 144  # 3600 // 600 * 24 -> one entry every 10 mins
seconds_in_day = 3600 * 24
parkings = np.array(tuple(data[np.abs(data[:, 1].astype(int) - int(date)) <= seconds_in_day]
                          for date in parking_dates[::entries_in_day]))


def filter_to_date(parkings, end_date):
    timestamp = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())
    for i, parking in enumerate(parkings):
        after_date = parking[:, 1].astype(int) > timestamp
        parkings[i] = np.delete(parking, after_date, axis=0)


def plot_day_avgs(day, day_data):
    date = datetime.fromtimestamp(day)

    plt.barh(tuple(day_data.keys()), day_data.values())
    plt.xlabel("Povprecna zasedenost")
    plt.title(f"Dan: {date}")
    plt.show()


filter_to_date(parkings, "2022-03-15")

days_map = {}
for day in parkings:
    if len(day) == 0:
        continue
    parks_in_day = np.array(tuple(day[day[:, 0] == name] for name in parking_names))
    park_map = {}
    for park in filter(lambda park: len(park) != 0, parks_in_day):
        name = park[0][0]
        average = np.average(park[:, 3].astype(int) - park[:, 2].astype(int))
        if average <= 0:  # Empty or wrong data
            continue
        park_map[name] = average

    days_map[int(day[0][1])] = park_map


for day, data in days_map.items():
    plot_day_avgs(day, data)
