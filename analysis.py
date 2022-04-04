import matplotlib.pyplot as plt
import numpy as np
import csv
from datetime import datetime

file = open('Parkirisca_do_04_04_2022.csv')
csv_dict = csv.DictReader(file)
data = np.array([line for line in csv_dict])
file.close()

mesta = np.unique(tuple(d["Parkirisce"] for d in data)) 

for mesto in mesta:
    mesto_data = np.array([(datetime.fromtimestamp(int(row["Datum"])), int(row["Prosta mesta"]))
                        for row in data if row["Parkirisce"] == mesto])

    plt.plot(mesto_data[:, 0], mesto_data[:, 1])
    plt.gcf().autofmt_xdate()  # format the dates
    plt.xlabel("Datum")
    plt.ylabel("Zasedena mesta")
    plt.title(f"Zasedenost: {mesto}")
    plt.show()

