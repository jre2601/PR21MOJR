import './style.css';
import {
    Feature,
    Map,
    View,
} from 'ol';
import OSM from 'ol/source/OSM';
import VectorSource from 'ol/source/Vector';
import Point from 'ol/geom/Point';
import {
    fromLonLat,
    useGeographic
} from 'ol/proj';
import {
    Heatmap as HeatmapLayer,
    Tile as TileLayer,
} from 'ol/layer';

useGeographic();


// Loading the data
const parkingData = await fetch("data.json")
    .then(response => response.json())
    .then(json => {
        return json
    });
console.log(parkingData);

let startIndex = 0;
let endIndex = parkingData["Bezigrad"].percent_occupied.length;
let i = startIndex;

// Datepicker setup
$('input[name="daterange"]').daterangepicker({
    locale: {
        format: 'DD/MM/YYYY'
    },
    minDate: new Date(Math.min(...parkingData["Bezigrad"].timestamps) * 1000),
    maxDate: new Date(Math.max(...parkingData["Bezigrad"].timestamps) * 1000),
});

$('input[name="daterange"]').on('apply.daterangepicker', (ev, picker) => {
    let startTime = Math.floor(picker.startDate._d.getTime() / 1000);
    let endTime = Math.floor(picker.endDate._d.getTime() / 1000);

    startIndex = -1;
    endIndex = -1;
    for (let idx = 0; idx < parkingData["Bezigrad"].timestamps.length; idx++) {
        console.log(idx);
        if (startIndex == -1 && startTime <= parkingData["Bezigrad"].timestamps[idx]) {
            startIndex = idx;
        }
        if (endIndex == -1 && parkingData["Bezigrad"].timestamps[idx] >= endTime) {
            endIndex = idx;
            break;
        }
    }
    i = startIndex;
    // console.log(startIndex, endIndex);
});

const aSpeed = document.getElementById('speed');
let animationSpeed = 50;
let animationPlaying = false;
$("#stop").addClass("activeButton");


// Adding initial parking data
let data = new VectorSource();

data.addFeature(new Feature({
    name: "MAX",
    geometry: new Point(fromLonLat([0, 0, 0])),
    magnitude: 1,
}));

const parkingCoords = [
    [14.517521, 46.039284, "Dolenjska cesta (Strelisce)"],
    [14.508285, 46.062497, "Bezigrad"],
    [14.514254, 46.087035, "BS4/ I"],
    [14.514251, 46.086728, "BS4/ II"],
    [14.518000, 46.074537, "Gosarjeva ulica"],
    [14.515989, 46.074583, "Gosarjeva ulica II."],
    [14.510116, 46.061856, "Gospodarsko razstavisce"],
    // [14.513173, 46.088353, "Komanova ulica"],
    [14.503415, 46.050617, "PH Kongresni trg"],
    [14.504961, 46.056943, "Kozolec"],
    [14.522073, 46.070205, "Kranjceva ulica"],
    [14.509180, 46.063127, "Linhartova"],
    [14.516126, 46.056973, "Metelkova ulica"],
    [14.494343, 46.046584, "Mirje"],
    [14.501974, 46.046687, "NUK II."],
    //[14.499581, 46.026924, "P+R Barje"],
    //[14.463085, 46.036492, "P+R Dolgi most"],
    //[14.568027, 46.054279, "P+R Studenec"],
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
    // [14.515946, 46.078370, "Stembalova ulica"],
    [14.528873, 46.068968, "Zale I."],
    [14.528680, 46.067131, "Zale II."],
    [14.526062, 46.067969, "Zale III."],
    [14.526815, 46.069497, "Zale IV."],
    [14.531361, 46.074782, "Zale V."],
]
parkingCoords.forEach(parking => {
    data.addFeature(new Feature({
        name: parking[2],
        geometry: new Point(fromLonLat([parking[0], parking[1], 0])),
        magnitude: 0.0,
    }));
});

const vector = new HeatmapLayer({
    source: data,
    blur: 18,
    radius: 20,
    weight: (feature) => {
        const name = feature.get('name');
        const magnitude = feature.get('magnitude');
        return magnitude;
    },
});

const raster = new TileLayer({
    source: new OSM(),
});

const map = new Map({
    layers: [raster, vector],
    target: 'map',
    view: new View({
        center: [14.505751, 46.056946],
        zoom: 13,
    }),
});


// Animation logic
let renderParkings = () => {
    if (animationPlaying) {
        data.forEachFeature(feat => {
            let name = feat.getProperties().name;
            if (name !== "MAX") {
                let percent = parkingData[name].percent_occupied[i];
                if (!(i < endIndex)) {
                    animationPlaying = false;
                    $("#play").removeClass("activeButton");
                    $("#stop").addClass("activeButton");
                }
                feat.setProperties({
                    magnitude: percent
                });
            }
        });
        map.render();
        let time = new Date(parkingData["Bezigrad"].timestamps[i] * 1000);

        $("#currentTime").html(`
            <p>${time.toLocaleDateString()}</p>
            <p>${time.toLocaleTimeString()}</p>
        `);
        // <p>${time.toLocaleDateString("sl-SL", { weekday: 'long' })}</p>
        i++;
        // console.log(animationSpeed);
        setTimeout(renderParkings, animationSpeed);
    }
}


// UI handling
$("#play").click(() => {
    if (!animationPlaying) {
        animationPlaying = true;
        setTimeout(renderParkings, animationSpeed);
        $("#play").addClass("activeButton");
        $("#stop").removeClass("activeButton");
    }
});
$("#stop").click(() => {
    if (animationPlaying) {
        animationPlaying = false;
        $("#play").removeClass("activeButton");
        $("#stop").addClass("activeButton");
    }
});


const animationSpeedHandler = () => {
    animationSpeed = 500 - parseInt(aSpeed.value);
};
aSpeed.addEventListener('input', animationSpeedHandler);
aSpeed.addEventListener('speed', animationSpeedHandler);