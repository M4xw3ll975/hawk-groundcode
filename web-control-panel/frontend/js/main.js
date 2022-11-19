// Main.js
// Organisation: AEHTER AEROSPACE INDUSTRIES
// Author: Maximilian Birnbacher

'use strict';
mapboxgl.accessToken = MAPBOX_API_KEY;

//map
var map = new mapboxgl.Map({
    container: 'map',
    //Style URL
    style: 'mapbox://styles/m4xw3ll/clams6dxz003h14nx6tnwsm9i', //custom style
    center: [
        13.845101, 46.601179
    ],
    zoom: 10.7
});

//add zoom and rotation controls to the map overlapping the map
map.addControl(new mapboxgl.NavigationControl());

//add draw control to the map to draw paths
const draw = new MapboxDraw({
    displayControlsDefault: false,
    controls: {
        line_string: true,
        trash: true,
        cancle: true
    },
    styles: [
        {
            "id": "gl-draw-line",
            "type": "line",
            "filter": [
                "all",
                [
                    "==", "$type", "LineString"
                ],
                [
                    "!=", "mode", "static"
                ]
            ],
            "layout": {
                "line-cap": "round",
                "line-join": "round"
            },
            "paint": {
                "line-color": "#e14673",
                "line-dasharray": [
                    0.2, 2
                ],
                "line-width": 3,
                "line-opacity": 0.7
            }
        }, {
            "id": "gl-draw-polygon-and-line-vertex-halo-active",
            "type": "circle",
            "filter": [
                "all",
                [
                    "==", "meta", "vertex"
                ],
                [
                    "==", "$type", "Point"
                ],
                [
                    "!=", "mode", "static"
                ]
            ],
            "paint": {
                "circle-radius": 6,
                "circle-color": "#e14673"
            }
        }, {
            "id": "gl-draw-polygon-and-line-vertex-active",
            "type": "circle",
            "filter": [
                "all",
                [
                    "==", "meta", "vertex"
                ],
                [
                    "==", "$type", "Point"
                ],
                [
                    "!=", "mode", "static"
                ]
            ],
            "paint": {
                "circle-radius": 3,
                "circle-color": "#FFF"
            }
        }
    ]
});

map.addControl(draw);

map.on('draw.create', updateArea);
map.on('draw.delete', updateArea);
map.on('draw.update', updateArea);

//store 2 styles in an array
const styles = ['mapbox://styles/m4xw3ll/cl9zp5f6j00ez14qtletemydp', 'mapbox://styles/m4xw3ll/cl9y23u9m00jt14o2fipec794'];

// get the coordinates of the plane from the api
let planeCoordinates = [13.845101, 46.601179];

//define geojson for the marker
const geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": planeCoordinates
            }
        }
    ]
};

//add the marker to the map
for (const feature of geojson.features) {
    const el = document.createElement('div');
    el.className = 'marker';
    new mapboxgl
        .Marker(el)
        .setLngLat(feature.geometry.coordinates)
        .addTo(map);
}




//update the marker position every 5 seconds
setInterval(function () {
    //get the coordinates of the plane from the api
    let planeCoordinates = [13.845101, 46.601179];

    //define geojson for the marker
    const geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": planeCoordinates
                }
            }
        ]
    };

    //add the marker to the map
    for (const feature of geojson.features) {
        const el = document.createElement('div');
        el.className = 'marker';
        new mapboxgl
            .Marker(el)
            .setLngLat(feature.geometry.coordinates)
            .addTo(map);
    }

    // display engine thurst with a tui barchart
    // get the engine thurst from the api
    let engineThurstLeft = 89;
    let engineThurstRight = 75;
    engineThrottle(engineThurstLeft, document.getElementById('left-eng'), 'LEFT');
    engineThrottle(engineThurstRight, document.getElementById('right-eng'), 'RIGHT');
    
    //update button status
    //get button DOM element
    let left_eng_pwr = document.getElementById('left-eng-pwr');
    let right_eng_pwr = document.getElementById('right-eng-pwr');
    let left_eng_error = document.getElementById('left-eng-error');
    let right_eng_error = document.getElementById('right-eng-error');
    let left_eng_fire = document.getElementById('left-eng-fire');
    let right_eng_fire = document.getElementById('right-eng-fire');
    let left_eng_speed = document.getElementById('left-eng-speed');
    let right_eng_speed = document.getElementById('right-eng-speed');
    let left_eng_temp = document.getElementById('left-eng-temp');
    let right_eng_temp = document.getElementById('right-eng-temp');
    let left_eng_battery = document.getElementById('left-eng-battery');
    let right_eng_battery = document.getElementById('right-eng-battery');
    let left_eng_amp = document.getElementById('left-eng-amp');
    let right_eng_amp = document.getElementById('right-eng-amp');
    let left_eng_volt = document.getElementById('left-eng-volt');
    let right_eng_volt = document.getElementById('right-eng-volt');

    //set button status with Buttonstatus.js
    ButtonStatus(left_eng_pwr, 'OK');
    ButtonStatus(right_eng_pwr, 'OK');
    ButtonStatus(left_eng_error, 'DISABLED');
    ButtonStatus(right_eng_error, 'ERROR');
    ButtonStatus(left_eng_fire, 'DISABLED');
    ButtonStatus(right_eng_fire, 'ERROR');
    ButtonStatus(left_eng_speed, 'OK');
    ButtonStatus(right_eng_speed, 'OK');
    ButtonStatus(left_eng_temp, 'OK');
    ButtonStatus(right_eng_temp, 'WARNING');
    ButtonStatus(left_eng_battery, 'OK');
    ButtonStatus(right_eng_battery, 'OK');
    ButtonStatus(left_eng_amp, 'OK');
    ButtonStatus(right_eng_amp, 'ERROR');
    ButtonStatus(left_eng_volt, 'OK');
    ButtonStatus(right_eng_volt, 'OK');

}, 5000);

//generate a gpx file from the coordinates
function generateGPX(coordinates) {
    var gpx = '<?xml version="1.0" encoding="UTF-8"?>';
    gpx += '<gpx version="1.1" creator="AEHTER WCP" xmlns="http://www.topografix.com/GPX/1' +
            '/1">\n';
    gpx += '<metadata />\n';
    //add the coordinates to the gpx file as waypoints
    for (var i = 0; i < coordinates.length; i++) {
        gpx += '<wpt lat="' + coordinates[i][1] + '" lon="' + coordinates[i][0] +
                '"><name>"' + i + '"</name></wpt>\n';
    }
    gpx += '</gpx>';
    return gpx;
}

// output the coordinates of the drawn path in the paragraph with
// id="waypoint-list" with only 6 decimal places if there are more than 10
// waypoints, make the paragraph scrollable and set a max height of 200px
function outputWaypoints(coordinates) {
    var waypointList = document.getElementById('waypoint-list');
    waypointList.innerHTML = '';
    for (var i = 0; i < coordinates.length; i++) {
        waypointList.innerHTML += '<li>' + coordinates[i][0].toFixed(6) + ', ' + coordinates[i][1].toFixed(
            6
        ) + '</li>';
    }
    if (coordinates.length > 10) {
        waypointList.style.maxHeight = '200px';
        waypointList.style.overflowY = 'scroll';
        //no points for the list style
        waypointList.style.listStyleType = 'none';
    } else {
        waypointList.style.listStyleType = 'none';
    }
}

//get the coordinates of the drawn path
function updateArea(e) {
    var data = draw.getAll();

    //generate a gpx file from the coordinates and save it to the server
    var gpx = generateGPX(data.features[0].geometry.coordinates);
    var blob = new Blob([gpx], {type: 'text/plain'});
    var url = URL.createObjectURL(blob);
    var link = document.createElement('a');
    link.href = url;
    link.download = 'path.gpx';
    link.click();

    // FIXME: CODE BELOW NOT WORKING! (send the gpx file to the server) save the gpx
    // file internally on the server in the folder "gpx" get path of the gpx folder
    // var path = '../../gpx'; get the name of the gpx file var name = 'path.gpx';
    // get the content of the gpx file var content = gpx; save the gpx file $.ajax({
    // url: 'upload.php',     type: 'POST',     data: {         path: path,
    // name: name,         content: content     },     success: function (data) {
    // console.log(data);     } }); list the coordinates of the drawn path in the
    // paragraph with id="waypoint-list"
    outputWaypoints(data.features[0].geometry.coordinates);
}
