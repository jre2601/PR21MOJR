# Analiza zasedenosti parkirnih mest v Ljubljani in okolici

Tekom analize podatkov bova skušala ugotoviti kdaj se pojavljajo konice zasedenosti na parkiriščih, jih skušala vnaprej napovedati, in izračuanti optimalno izbiro parkirišča glede na čas in željeno končno lokacijo.

# Podatki

Vsi podatki so zbrani iz spletne strani [Ljubljanska parkirišča in tržnice](https://www.lpt.si/parkirisca/informacije-za-parkiranje/prikaz-zasedenosti-parkirisc). Podatki se na spletni strani osvežijo vsakih 10 minut in ob času pisanja tega poročila sva zbrala dober mesec podatkov (~7 MB velika csv datoteka).

## Atributi

V podatkih samih pravzaprav ni veliko atributov, najpomembnejši so: `Parkirisce, Datum, Prosta mesta, Kapaciteta`. Obstajajo tudi enaki atributi, ki se beležijo le za naročnike, vendar pa le-ti ne bodo glavni poudarek naloge.

## Težave

Delež podatkov je pomankljiv oziroma celo napačen, namreč za določena parkirišča število prostih mest in kapaciteta nista beležena, pri določenih pa neprestano pise da so popolnoma zasedena, **čeprav v resnici niso**. Taka parkirišča so večinoma tipa P+R oziroma *Park and Ride*, ali so namenjena avtobusom (Bratislavska), ali pa so izven okolice Ljubljane (Tacen - parkirišče pod Šmarno goro). Ugibamo lahko, da so v ozadju morebitni birokratski razlogi, da za ta parkirišča ne beležijio / objavljajo števila prostih mest. Morda pa se jim to sploh ne splača, saj parkirisca P+R (načeloma) nikoli niso popolnoma zasedena.

Primer prikaza zasednih parkirišč, ki so v resnici prosta:

![Napačen prikaz podatkov](https://user-images.githubusercontent.com/59799831/161757323-94754b40-6d95-4099-a57a-a05342d2467f.png)

Pri nekaterih parkiriščih je celo število prostih mest **večje** od kapacitete. Primer je Žale V., kjer je na prikazu parkirilšč kapaciteta enaka 100, v opisu pa 288. Ta napaka je najverjetneje najhujša, saj jo je najtežje opaziti in lahko zelo "pokvari" analizo.

Tekom zbiranja podatkov se je zgodila še ena zanimivost, in sicer parkirišče "Center Stožice" je bilo izbrisano iz seznama. Očitno so med časom brisanja ugasnili njihove strežnike, kar je povzročilo zaustavitev skripte, česar nisva opazila približno 1 teden, in sva tako izgubila približno 1 teden podatkov.

Parkirišča s pomankljivimi podatki bodo **zavržena**, saj so neuporabna. To si lahko privoščimo, saj je ustreznih podatkov še vedno dovolj, da pridemo do smiselnih rezultatov.


# Analiza

## Priprava podatkov

### Grupiranje po imenih

Za tem ko so podatki prebrani iz datoteke, so parkirišča z enakim imenom grupirana v tabelo. Tako dobimo **2-dimenzionalno tabelo**, kjer posamezen element predstavlja eno parkirišče. Iz tabele se nato pobrišejo parkirišča z manjkajočimi polji, po potrebi pa jih lahko še omejimo do določenega datuma.

### Grupiranje po času

Parkirišča, ki imajo enak *timestamp* so grupirana v eno tabelo s časovnim razmakom ~1 dan. Tako dobimo tabelo, kjer so posamezni elementi bili zajeti v istem dnevu.


## Vizualizacija / ugotovitve

Naslednji graf prikazuje povprečno zasedenost parkirišč na dan 25.2.2022.

![image](https://user-images.githubusercontent.com/59799831/162043888-9c09f7ef-4a6f-400f-a9e0-cab33bbd7248.png)

Opazimo lahko da so si parkirišča med seboj dokaj različna. Poleg ure v dnevu in velikosti parkirišča je zelo pomembna tudi **lokacija** parkirišča, ni vseeno ali je parkirišče zraven trgovine, apartmajev ali objekta javne uprave. Poleg tega obstaja velika verjetnost, da imajo parkirišča, ki so blizu podobne vzorce. Vendar pa se vzorci parkirišč ne glede na to še vedno ponavljajo, in je napoved zasedenosti lahko dokaj natančna.

### Primer: Gosarjeva ulica

![image](https://user-images.githubusercontent.com/59799831/162046994-2a019556-fb49-4bfa-b8c0-6525844b26f5.png)

Gre za parkirišče, ki je v neposredni bližini fakultet (Ekonomska fakulteta, Pedagoška fakulteta ...) in predstavlja tipičen primer parkirišča zraven javne uprave, kjer vsak delovni dan zjutraj ljudje gredo v službe in parkirišče skoraj vedno zapolnijo do polne kapacitete. Stanje tega parkirišča morda ni zahtevno napovedati, lahko pa napovemo, da je parkirišče s takim vzorcem najverjetneje v bližini javne uprave ali industrijske cone.

### Primer: Center Stožice

![image](https://user-images.githubusercontent.com/59799831/162049539-d916111f-ab1f-4080-9dd7-605199184bf2.png)

Center Stožice pa predstavlja drugo skrajnost, kjer so parkirna mesta zasedena le na določene dni, po večini so to vikendi. Opazimo lahko tudi veliko zasedenost dne 8.3.2022 ob ~8 uri zvečer. Z veliko samozavestjo lahko ugibamo, da gre za nek dogodek. Po hitrem *googlanju* je res šlo za igro košarke: KK Cedevita Olimpija : Budučnost, EuroCup. Pomembna informacija, ki jo pridobimo je ta **kdaj** točno se parkirišča zapolnijo, predvidimo torej lahko kdaj moramo oditi, da ne bomo pozni.