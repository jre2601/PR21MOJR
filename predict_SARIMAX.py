import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from scipy.stats import pearsonr
from statsmodels.tsa.statespace.sarimax import SARIMAX
import pandas as pd


# parkings_data = np.fromregex('podatki/ml-latest-small/movies.csv', r'(\d+),"?(.+)"?,(.+)', dtype=[("movieId",'i8'), ("title", 'U100'), ("genres", 'U100')], encoding="utf-8")
data = np.loadtxt(open("Parkirisca_do_04_04_2022.csv", "r"), dtype=[("ime", "U35"), ("datum", "i8"), ("prosta_mesta", "i8"), (
    "kapaciteta", "i8"), ("na_voljo(narocniki)", "U10"), ("oddana(narocniki)", "U10"), ("cakalna_vrsta(narocniki)", "U10")], delimiter=",", skiprows=1)

parking_names = np.unique(data["ime"])
all_parkings = np.array(tuple(data[data["ime"] == name] for name in parking_names))

# print(all_parkings.shape)
# print(all_parkings)

# Filter out empty data
empty_parkings = np.fromiter((not np.any(parking["prosta_mesta"]) for parking in all_parkings), dtype=bool)
parkings = np.delete(all_parkings, empty_parkings, axis=0)

# print(parkings)


def filter_to_date(parkings, end_date):
    out = parkings.copy()
    timestamp = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())
    for i, parking in enumerate(out):
        after_date = parking["datum"] > timestamp
        out[i] = np.delete(parking, after_date, axis=0)
    return out


def filter_date_range(parkings, start_date, end_date):
    out = parkings.copy()
    timestamp_start = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
    timestamp_end = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())
    for i, parking in enumerate(out):
        illegal_dates = (parking["datum"] < timestamp_start) | (parking["datum"] > timestamp_end)
        out[i] = np.delete(parking, illegal_dates, axis=0)
    return out


def plot_parking(parking):
    name = parking[0]["ime"]
    capacity = int(parking[parking["kapaciteta"] != 0][0]["kapaciteta"])
    min_x, max_x = np.min(parking["datum"]), np.max(parking["datum"])

    # X: date, Y: capacity - n_free_spots = n_occupied
    plt.plot(tuple(map(datetime.fromtimestamp, parking["datum"])), parking["kapaciteta"] - parking["prosta_mesta"])
    plt.plot(tuple(map(datetime.fromtimestamp, (min_x, max_x))), (capacity, capacity), "k--")
    plt.gcf().autofmt_xdate()  # format the dates
    plt.xlabel("Datum")
    plt.ylabel("Stevilo zasedenih mest")
    plt.title(f"Parkirisce: {name}")
    plt.show()


def plot_fit_residual(x, y, yp):
    # Model
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 4))
    axes[0].plot(x.ravel(), y.ravel(), "k.",  label="Podatki")
    axes[0].plot(x.ravel(), yp.ravel(), "g-", label="Model h(x)")
    axes[0].set_xlabel("x")
    axes[0].set_ylabel("y")
    axes[0].legend(loc=4)

    # Ostanki
    r = pearsonr(y.ravel(), y.ravel()-yp.ravel())[0]
    axes[1].plot(y.ravel(), y.ravel()-yp.ravel(), "k.", label="Ostanek")
    axes[1].set_xlabel("y")
    axes[1].set_ylabel("y-h(x)")
    axes[1].set_title("Graf ostankov, R=%.3f" % r)
    axes[1].legend(loc=4)
    plt.show()


# FIXME: Data/format is wrong?
# Seasonal Auto-Regressive Integrated Moving Average with eXogenous factors
train = filter_to_date(parkings, "2022-03-15")
test = filter_date_range(parkings, "2022-03-23", "2022-04-04")
for train_park_data, test_park_data in zip(train, test):
    timestamps_train = pd.to_datetime(list(map(lambda park: park[1], train_park_data)), unit="s")
    timestamps_test = pd.to_datetime(list(map(lambda park: park[1], test_park_data)), unit="s")
    train_park = train_park_data["kapaciteta"] - train_park_data["prosta_mesta"]
    train_data = pd.DataFrame(train_park)
    train_data.index = timestamps_train
    test_park = test_park_data["kapaciteta"] - test_park_data["prosta_mesta"]
    test_data = pd.DataFrame(test_park)
    test_data.index = timestamps_test

    SARIMAXmodel = SARIMAX(train_data, order=(5, 4, 2), seasonal_order=(2, 2, 2, 12))
    SARIMAXmodel = SARIMAXmodel.fit()

    y_pred = SARIMAXmodel.get_forecast(len(test_data.index))
    y_pred_df = y_pred.conf_int(alpha=0.05)
    y_pred_df["Predictions"] = SARIMAXmodel.predict(start=y_pred_df.index[0], end=y_pred_df.index[-1])
    y_pred_df.index = test_data.index
    y_pred_out = y_pred_df["Predictions"]
    plt.plot(train_data, color="Blue", label="Train")
    plt.plot(test_data, color="Black", label="Test")
    plt.plot(y_pred_out, color='Red', label='SARIMA Predictions')
    plt.legend()
    plt.show()
