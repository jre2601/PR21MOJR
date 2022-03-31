# Analiza zasedenosti parkirnih mest v Ljubljani in okolici

Seminarska naloga za predmet Podatkovno rudarjenje na Fakuteti za računalništvo in informatiko v študijskem letu 2021/2022.

## Ekipa

- Matija Ojo
- Jan Renar

## Problem

Izbrala sva si problem zasedenosti parkirišč v Ljubljani. Tekom analize podatkov bova skušala ugotoviti kdaj se pojavljajo konice zasedenosti na parkiriščih, jih skušala vnaprej napovedati, in izračuanti optimalno izbiro parkirišča glede na čas in željeno končno lokacijo.


## Vir podatkov

Podatke o trenutni zasedenosti parkirisc bova pridobivala iz spletne strani [Ljubljanska parkirišča in tržnice](https://www.lpt.si/parkirisca/informacije-za-parkiranje/prikaz-zasedenosti-parkirisc) in jih *parsala* s pomocjo knjiznice [Beautiful Soup 4](https://beautiful-soup-4.readthedocs.io/en/latest/).

## Oblika podatkov

Parkirisca.csv:

- Parkirisce - ime parkirišča; string
- Datum - čas ob vnosu (timestamp); string
- Prosta mesta - število prostih mest; numeric
- Kapaciteta - število vseh mest; numeric
- Na voljo (narocniki) - kapaciteta mest za naročnike; numeric
- Oddana (narocniki) - število mest, ki jih naročniki uporabljajo; numeric
- Prosta (narocniki) - število prostih mest za naročnike; numeric
- Cakalna vrsta (narocniki) - število ljudi, ki čaka za nakup naročnine; numeric
