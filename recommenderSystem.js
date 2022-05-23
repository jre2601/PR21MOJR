import './style.css';
import {
    Feature,
    Map,
    View,
} from 'ol';
import OSM from 'ol/source/OSM';
import VectorSource from 'ol/source/Vector';
import Overlay from 'ol/Overlay';
import Point from 'ol/geom/Point';
import {
    fromLonLat,
    useGeographic
} from 'ol/proj';
import {
    Heatmap as HeatmapLayer,
    Tile as TileLayer,
    Vector as VectorLayer
} from 'ol/layer';
import {Icon, Style} from 'ol/style';

useGeographic();



// All parkings as features
let iconFeatures = [];

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

const iconStyle = new Style({
    image: new Icon({
        anchor: [0.5, 1],
        anchorXUnits: 'fraction',
        anchorYUnits: 'fraction',
        src: 'location.svg',
        scale: [0.07, 0.07],
    })
});

parkingCoords.forEach(parking => {
    let feature = new Feature({
        name: parking[2],
        geometry: new Point([parking[0], parking[1]]),
        /*population: 4000,
        rainfall: 500,*/
    });
    feature.setStyle(iconStyle);
    iconFeatures.push(feature);
});

const raster = new TileLayer({
    source: new OSM(),
});

  
const vectorLayer = new VectorLayer({
    source: new VectorSource({
        features: iconFeatures,
    })
});


const map = new Map({
    layers: [raster, vectorLayer],
    target: 'map',
    view: new View({
        center: [14.505751, 46.056946],
        zoom: 13,
    }),
});

map.on('singleclick', function (e) {
    console.log(e.coordinate);
    Swal.fire({
        title: '<h1>Priporočilni sistem</h1><br>',
        html:
            `
            <div class="recommenderModal">
                Koordinate cilja: <b>${e.coordinate[0].toFixed(4)}</b> - <b>${e.coordinate[1].toFixed(4)}</b><br>
                Datum prihoda: <input style="top: 0px;" type="text" name="daterange" value="" /><br>
            </div>
          `,
        showCloseButton: true,
        showCancelButton: true,
        focusConfirm: false,
        showLoaderOnConfirm: true,
        confirmButtonText:
          '<i class="fa fa-thumbs-up"></i> Potrdi',
        cancelButtonText:
          '<i class="fa fa-thumbs-down"></i> Prekliči',
    }).then((result) => {
        if (result.isConfirmed) {

            let postResult = {};
            console.log($('input[name="daterange"]').val());
           
            $.ajax({
                url: 'getRecommendation',
                dataType: 'json',
                type: 'post',
                contentType: 'application/json',
                data: JSON.stringify( {
                    x: e.coordinate[0],
                    y: e.coordinate[1],
                    date: $('input[name="daterange"]').val(),
                } ),
                processData: false,
                success: function( data, textStatus, jQxhr ){
                    console.log(data);
                    postResult = data;
                    iconFeatures.forEach(f => { f.setStyle(iconStyle); });
                    iconFeatures.forEach(f => {
                        if (f.getProperties().name == postResult) {
                            f.setStyle(new Style({
                             image: new Icon({
                                 anchor: [0.5, 1],
                                 anchorXUnits: 'fraction',
                                 anchorYUnits: 'fraction',
                                 src: 'location_recommended.svg',
                                 scale: [0.12, 0.12],
                             })
                         }));
                        }
                     });
                },
                error: function( jqXhr, textStatus, errorThrown ){
                    console.log( errorThrown );
                }
            }).then(() => {
                
                Swal.fire({
                    title: '<h1>Priporočeno parkirišče:</h1><br>',
                    html:
                        `
                        <h2>${postResult}</h2>
                        <div class="recommenderModal">
                        </div>
                      `,
                    showCloseButton: true,
                    showCancelButton: false,
                    focusConfirm: true,
                    confirmButtonText:
                      '<i class="fa fa-thumbs-up"></i> Izhod',
                })
            });
        }
    });
    
    // Datepicker setup
    $('input[name="daterange"]').daterangepicker({
        "singleDatePicker": true,
        locale: {
            format: 'DD/MM/YYYY'
        },
    });
   
});


// Change mouse cursor when over marker
/*map.on('pointermove', function (e) {
  const pixel = map.getEventPixel(e.originalEvent);
  const hit = map.hasFeatureAtPixel(pixel);
  map.getTarget().style.cursor = hit ? 'pointer' : '';
});*/

// Close the popup when the map is moved
map.on('movestart', function () {
  // $(element).popover('dispose');
  // Close overlay
});

// Clear recommendation
$("#clearRec").click(() => {
    iconFeatures.forEach(f => {
        f.setStyle(iconStyle);
    });
});

