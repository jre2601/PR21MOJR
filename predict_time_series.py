import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from scipy.stats import pearsonr
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd

data = np.loadtxt(open("Parkirisca_do_10_05_2022.csv", "r"), dtype=[("ime", "U35"), ("datum", "i8"), ("prosta_mesta", "i8"), (
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


train_data = filter_to_date(parkings, "2022-05-05")
test_data = filter_date_range(parkings, "2022-05-06", "2022-05-11")

for train_park_data, test_park_data in zip(train_data, test_data):
    if train_park_data.size == 0 or test_park_data.size == 0:
        continue
    timestamps_train = pd.to_datetime(list(map(lambda park: park[1], train_park_data)), unit="s")
    train = pd.DataFrame(train_park_data["kapaciteta"] - train_park_data["prosta_mesta"], columns=["Zasedenost"])
    train.index = timestamps_train

    timestamps_test = pd.to_datetime(list(map(lambda park: park[1], test_park_data)), unit="s")
    test = pd.DataFrame(test_park_data["kapaciteta"] - test_park_data["prosta_mesta"], columns=["Zasedenost"])
    test.index = timestamps_test

    plt.plot(train, color="black", label='Training')
    plt.plot(test, color="red", label='Test')

    name = train_park_data["ime"][0]
    plt.gcf().autofmt_xdate()
    plt.xlabel("Datum")
    plt.ylabel("Stevilo zasedenih mest")
    plt.title(f"Parkirisce: {name}")

    y = train["Zasedenost"]

    # ARIMA Predictor
    ARIMAmodel = ARIMA(y, order=(1, 0, 0))
    ARIMAmodel = ARIMAmodel.fit()
    y_pred = ARIMAmodel.get_forecast(len(test.index))
    y_pred_df = y_pred.conf_int(alpha=0.05)
    y_pred_df["Predictions"] = ARIMAmodel.predict(start=y_pred_df.index[0], end=y_pred_df.index[-1])
    y_pred_df.index = test.index
    plt.plot(y_pred_df["Predictions"], color='Blue', label='ARIMA Predictions')
    arima_rmse = np.sqrt(mean_squared_error(test["Zasedenost"].values, y_pred_df["Predictions"]))
    print("ARIMA RMSE: ", arima_rmse)

    plt.legend()
    plt.show()

# print("----------------------------------------------------------------------------------------------------")
# print(sorted(((v, k) for k, v in RMSE.items())))
# params = ((1, 0, 0), (0, 1, 0), (1, 1, 0), (0, 1, 1), (0, 2, 1), (0, 2, 2), (1, 1, 2))
# RMSE = {}
# for p, d, q in params:
#     ARMA_RMSE_sum = 0
#     ARIMA_RMSE_sum = 0
#     SARIMA_RMSE_sum = 0
#     for train_park_data, test_park_data in zip(train_data[:2], test_data):
#         if train_park_data.size == 0 or test_park_data.size == 0:
#             continue
#         timestamps_train = pd.to_datetime(list(map(lambda park: park[1], train_park_data)), unit="s")
#         train = pd.DataFrame(train_park_data["kapaciteta"] - train_park_data["prosta_mesta"], columns=["Zasedenost"])
#         train.index = timestamps_train

#         timestamps_test = pd.to_datetime(list(map(lambda park: park[1], test_park_data)), unit="s")
#         test = pd.DataFrame(test_park_data["kapaciteta"] - test_park_data["prosta_mesta"], columns=["Zasedenost"])
#         test.index = timestamps_test

#         # plt.plot(train, color="black", label='Training')
#         # plt.plot(test, color="red", label='Test')

#         # name = train_park_data["ime"][0]
#         # plt.gcf().autofmt_xdate()
#         # plt.xlabel("Datum")
#         # plt.ylabel("Stevilo zasedenih mest")
#         # plt.title(f"Parkirisce: {name}")

#         y = train["Zasedenost"]

#         # ARMA Predictor
#         ARMAmodel = SARIMAX(y, order=(p, d, q))
#         ARMAmodel = ARMAmodel.fit()
#         y_pred = ARMAmodel.get_forecast(len(test.index))
#         y_pred_df = y_pred.conf_int(alpha=0.05)
#         y_pred_df["Predictions"] = ARMAmodel.predict(start=y_pred_df.index[0], end=y_pred_df.index[-1])
#         y_pred_df.index = test.index
#         # plt.plot(y_pred_df["Predictions"], color='green', label='ARMA Predictions')
#         arma_rmse = np.sqrt(mean_squared_error(test["Zasedenost"].values, y_pred_df["Predictions"]))
#         # print("ARMA RMSE: ", arma_rmse)
#         ARMA_RMSE_sum += arma_rmse

#         # ARIMA Predictor
#         ARIMAmodel = ARIMA(y, order=(p, d, q))
#         ARIMAmodel = ARIMAmodel.fit()
#         y_pred = ARIMAmodel.get_forecast(len(test.index))
#         y_pred_df = y_pred.conf_int(alpha=0.05)
#         y_pred_df["Predictions"] = ARIMAmodel.predict(start=y_pred_df.index[0], end=y_pred_df.index[-1])
#         y_pred_df.index = test.index
#         # plt.plot(y_pred_df["Predictions"], color='Yellow', label='ARIMA Predictions')
#         # plt.legend()
#         arima_rmse = np.sqrt(mean_squared_error(test["Zasedenost"].values, y_pred_df["Predictions"]))
#         # print("ARIMA RMSE: ", arima_rmse)
#         ARIMA_RMSE_sum += arima_rmse

#         # Seasonal Auto-Regressive Integrated Moving Average with eXogenous factors
#         SARIMAXmodel = SARIMAX(y, order=(p, d, q), seasonal_order=(2, 2, 2, 12))
#         SARIMAXmodel = SARIMAXmodel.fit()
#         y_pred = SARIMAXmodel.get_forecast(len(test.index))
#         y_pred_df = y_pred.conf_int(alpha=0.05)
#         y_pred_df["Predictions"] = SARIMAXmodel.predict(start=y_pred_df.index[0], end=y_pred_df.index[-1])
#         y_pred_df.index = test.index
#         # plt.plot(y_pred_df["Predictions"], color='Blue', label='SARIMA Predictions')
#         sarima_rmse = np.sqrt(mean_squared_error(test["Zasedenost"].values, y_pred_df["Predictions"]))
#         # print("SARIMA RMSE: ", sarima_rmse)
#         SARIMA_RMSE_sum += sarima_rmse

#         # plt.legend()
#         # plt.show()

#     RMSE["ARMA_RMSE(" + str(p) + ", " + str(d) + ", " + str(q) + ")"] = ARMA_RMSE_sum
#     RMSE["ARIMA_RMSE(" + str(p) + ", " + str(d) + ", " + str(q) + ")"] = ARIMA_RMSE_sum
#     RMSE["SARIMA_RMSE(" + str(p) + ", " + str(d) + ", " + str(q) + ")"] = SARIMA_RMSE_sum

# print("----------------------------------------------------------------------------------------------------")
# print(sorted(((v, k) for k, v in RMSE.items())))
