from statsmodels.tsa.statespace.sarimax import SARIMAXResults
from math import sqrt, cos, asin
import warnings

warnings.filterwarnings("ignore")


class Predictor:
    def __init__(self, models_path="models"):
        self.parkings = {
            "Dolenjska cesta (Strelisce)": (14.517521, 46.039284, 67),
            "Bezigrad": (14.508285, 46.062497, 64),
            "Gosarjeva ulica": (14.518000, 46.074537, 190),
            "Gosarjeva ulica II.": (14.515989, 46.074583, 115),
            "Gospodarsko razstavisce": (14.510116, 46.061856, 400),
            "PH Kongresni trg": (14.503415, 46.050617, 720),
            "Kozolec": (14.504961, 46.056943, 394),
            "Kranjceva ulica": (14.522073, 46.070205, 117),
            "Linhartova": (14.509180, 46.063127, 121),
            "Metelkova ulica": (14.516126, 46.056973, 89),
            "Mirje": (14.494343, 46.046584, 107),
            "NUK II.": (14.501974, 46.046687, 188),
            "PH Kolezija": (14.493818, 46.042360, 80),
            "Petkovskovo nabrezje II.": (14.511568, 46.052130, 85),
            "Pokopalisce Polje": (14.582565, 46.054942, 39),
            "Povsetova ulica": (14.529375, 46.051250, 81),
            "Senatorij Emona": (14.508596, 46.053622, 25),
            "Slovenceva ulica": (14.507321, 46.088504, 128),
            "Tivoli I.": (14.500366, 46.056411, 351),
            "Tivoli II.": (14.497231, 46.059912, 159),
            "Trg mladinskih delovnih brigad": (14.495670, 46.046982, 26),
            "Trg prekomorskih brigad": (14.488943, 46.068388, 61),
            "Zale I.": (14.528873, 46.068968, 125),
            "Zale IV.": (14.526815, 46.069497, 78),
            "Zale V.": (14.531361, 46.074782, 100),
        }

        self.models = {park_name: SARIMAXResults.load(
            models_path + "/" + park_name.replace("/", "_") + ".pkl") for park_name in self.parkings}

    def predict(self, date, loc):
        m = (-1, -1)
        prediction = None
        max_dist = 10000
        dist_weight = 3
        for park_name in self.parkings:
            curr_park = self.parkings[park_name]
            predicted = self.models[park_name].predict(start=date, end=date, dynamic=True, suppress_warnings=True)[0]
            dist_score = dist_weight * self.coordinate_distance(loc[1], loc[0], curr_park[1], curr_park[0]) / max_dist
            park_score = predicted / curr_park[-1]  # predicted_value / capacity
            if m == (-1, -1) or dist_score < m[0] and 0 < park_score < m[1]:
                m = (dist_score, park_score)
                prediction = park_name

        return prediction

    def coordinate_distance(self, lat1, lng1, lat2, lng2):
        p = 0.017453292519943295
        a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lng2 - lng1) * p)) / 2
        return 12742 * asin(sqrt(a)) * 1000  # meters


# p = Predictor()
# print(p.predict('2022-05-15', (14.515449867797852, 46.08612347752708)))