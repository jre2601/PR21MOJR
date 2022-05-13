import requests
import json

def get_api_key(filename):
    try:
        with open(filename, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)


parking_coords = [
    [14.517521, 46.039284, "Dolenjska cesta (Strelisce)"],
    [14.508285, 46.062497, "Bezigrad"],
    [14.514254, 46.087035, "BS4/ I"],
    [14.514251, 46.086728, "BS4/ II"],
    [14.518000, 46.074537, "Gosarjeva ulica"],
    [14.515989, 46.074583, "Gosarjeva ulica II."],
    [14.510116, 46.061856, "Gospodarsko razstavisce"],
    [14.503415, 46.050617, "PH Kongresni trg"],
    [14.504961, 46.056943, "Kozolec"],
    [14.522073, 46.070205, "Kranjceva ulica"],
    [14.509180, 46.063127, "Linhartova"],
    [14.516126, 46.056973, "Metelkova ulica"],
    [14.494343, 46.046584, "Mirje"],
    [14.501974, 46.046687, "NUK II."],
    [14.493818, 46.042360, "PH Kolezija"],
    [14.511568, 46.052130, "Petkovskovo nabrezje II."],
    [14.582565, 46.054942, "Pokopalisce Polje"],
    [14.529375, 46.051250, "Povsetova ulica"],
    [14.508596, 46.053622, "Senatorij Emona"],
    [14.507321, 46.088504, "Slovenceva ulica"],
    [14.500366, 46.056411, "Tivoli I."],
    [14.497231, 46.059912, "Tivoli II."],
    [14.495670, 46.046982, "Trg mladinskih delovnih brigad"],
    [14.488943, 46.068388, "Trg prekomorskih brigad"],
    [14.528873, 46.068968, "Zale I."],
    [14.528680, 46.067131, "Zale II."],
    [14.526062, 46.067969, "Zale III."],
    [14.526815, 46.069497, "Zale IV."],
    [14.531361, 46.074782, "Zale V."],
]

headers = {
    "Accept": "application/json",
    "Authorization": get_api_key("key.local")
}
radius = 50
for p in parking_coords:
    ll = "{:.3f}".format(p[1]) + "%2C" + "{:.3f}".format(p[0])
    name = p[-1]

    url = "https://api.foursquare.com/v3/places/search?ll="+ll+"&radius="+str(radius)
    response = requests.get(url, headers=headers)
    park_data = json.loads(response.text)

    print(name, ":")
    for poi in park_data["results"]:
        print("\t",poi["name"], "-", ", ".join(map(lambda c: c["name"], poi["categories"])), "; distance: ", poi["distance"], "m")
    print("----------------------------------")
