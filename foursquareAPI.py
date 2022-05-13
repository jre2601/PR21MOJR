import requests
import json


def get_api_key(filename):
    try:
        with open(filename, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)


park_locations = {
    "Dolenjska cesta (Strelisce)": (14.517521, 46.039284),
    "Bezigrad": (14.508285, 46.062497),
    "BS4/ I": (14.514254, 46.087035),
    "BS4/ II": (14.514251, 46.086728),
    "Gosarjeva ulica": (14.518000, 46.074537),
    "Gosarjeva ulica II.": (14.515989, 46.074583),
    "Gospodarsko razstavisce": (14.510116, 46.061856),
    "PH Kongresni trg": (14.503415, 46.050617),
    "Kozolec": (14.504961, 46.056943),
    "Kranjceva ulica": (14.522073, 46.070205),
    "Linhartova": (14.509180, 46.063127),
    "Metelkova ulica": (14.516126, 46.056973),
    "Mirje": (14.494343, 46.046584),
    "NUK II.": (14.501974, 46.046687),
    "PH Kolezija": (14.493818, 46.042360),
    "Petkovskovo nabrezje II.": (14.511568, 46.052130),
    "Pokopalisce Polje": (14.582565, 46.054942),
    "Povsetova ulica": (14.529375, 46.051250),
    "Senatorij Emona": (14.508596, 46.053622),
    "Slovenceva ulica": (14.507321, 46.088504),
    "Tivoli I.": (14.500366, 46.056411),
    "Tivoli II.": (14.497231, 46.059912),
    "Trg mladinskih delovnih brigad": (14.495670, 46.046982),
    "Trg prekomorskih brigad": (14.488943, 46.068388),
    "Zale I.": (14.528873, 46.068968),
    "Zale II.": (14.528680, 46.067131),
    "Zale III.": (14.526062, 46.067969),
    "Zale IV.": (14.526815, 46.069497),
    "Zale V.": (14.531361, 46.074782),
}

headers = {
    "Accept": "application/json",
    "Authorization": get_api_key("key.local")
}
# for p in parking_data:
#     ll = "{:.3f}".format(p[1]) + "%2C" + "{:.3f}".format(p[0])
#     name = p[-1]

#     url = "https://api.foursquare.com/v3/places/search?ll="+ll+"&radius="+str(radius)
#     response = requests.get(url, headers=headers)
#     park_data = json.loads(response.text)

#     print(name, ":")
#     for poi in park_data["results"]:
#         print("\t", poi["name"], "-", ", ".join(map(lambda c: c["name"],
#               poi["categories"])), "; distance: ", poi["distance"], "m")
#     print("----------------------------------")


def get_poi(park_name, radius=50):
    location = park_locations[park_name]
    ll = "{:.3f}".format(location[1]) + "%2C" + "{:.3f}".format(location[0])

    url = "https://api.foursquare.com/v3/places/search?ll="+ll+"&radius="+str(radius)
    response = requests.get(url, headers=headers)
    park_data = json.loads(response.text)

    return [", ".join(map(lambda c: c["name"], poi["categories"])) for poi in park_data["results"]]


print(get_poi("Petkovskovo nabrezje II."))