from bs4 import BeautifulSoup
import requests
import csv
import os
from datetime import datetime
from time import sleep, mktime


def map_to_ascii(s):
    mp = {"š": "s", "č": "c", "ž": "z", "Š": "S", "Č": "C", "Ž": "Z"}
    return "".join(map(lambda c: mp.get(c, c), s))


csv_file = open("Parkirisca.csv", "a")
csv_writer = csv.writer(csv_file)
format_ = ["Parkirisce", "Datum", "Prosta mesta", "Kapaciteta",
           "Na voljo (narocniki)", "Oddana (narocniki)", "Prosta (narocniki)", "Cakalna vrsta (narocniki)"]
csv_writer.writerow(format_)
print("Format zapisa: ", format_)

LINK = "https://www.lpt.si/parkirisca/informacije-za-parkiranje/prikaz-zasedenosti-parkirisc"

try:
    while True:
        source = requests.get(LINK).text
        soup = BeautifulSoup(source, "lxml")

        parkirisca = soup.find_all("a", class_="text-green underline hover:font-bold")
        mesta = soup.find_all("p", class_="w-1/3")
        narocniki = soup.find_all("p", class_="w-1/4")

        mesta = [m.get_text() for (i, m) in enumerate(mesta) if i % 3 == 1 or i % 3 == 2]

        nar = zip(narocniki[4::4], narocniki[5::4], narocniki[6::4], narocniki[7::4])

        for (parkirisce, mesta, n) in zip(parkirisca, zip(mesta[2::2], mesta[3::2]), nar):
            ime = map_to_ascii(parkirisce.get_text())
            datum = int(datetime.now().timestamp())  # UNIX UTC timestamp
            prosta_mesta = 0 if mesta[0] == "/" else int(mesta[0])
            kapaciteta = 0 if mesta[1] == "/" else int(mesta[1])
            nx = [n[i].get_text() for i in range(4)]  # narocniki

            out = [ime, datum, prosta_mesta, kapaciteta, *nx]
            csv_writer.writerow(out)
            print(out)

        csv_file.flush()
        sleep(600)  # 10 min
except BaseException:
    csv_file.close()
