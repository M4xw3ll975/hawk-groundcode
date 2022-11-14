// use strict

'use strict';

//html elements
const loadButton = document.getElementById('load');

//Mapbox map
//access token
// mapboxgl.accessToken = 'pk.eyJ1IjoibTR4dzNsbCIsImEiOiJjbDl4NzhsbGMwNzY3M3Fub3JhbnZldGhnIn0.9Y1af9ijoJiMuKxBe0CZyw';
mapboxgl.accessToken = MAPBOX_API_KEY;

//map
var map = new mapboxgl.Map({
    container: 'map',
    //Style URL
    style: 'mapbox://styles/m4xw3ll/cl9y23u9m00jt14o2fipec794', //custom style
    center: [13.845101, 46.601179],
    zoom: 10.7
});

//add zoom and rotation controls to the map.
map.addControl(new mapboxgl.NavigationControl());

//add draw control to the map to draw paths
const draw = new MapboxDraw({
    displayControlsDefault: false,
    controls: {
        line_string: true,
        trash: true,
        cancle: true
    },
    styles: [{
        "id": "gl-draw-line",
        "type": "line",
        "filter": ["all", ["==", "$type", "LineString"], ["!=", "mode", "static"]],
        "layout": {
            "line-cap": "round",
            "line-join": "round"
        },
        "paint": {
            "line-color": "#e14673",
            "line-dasharray": [0.2, 2],
            "line-width": 3,
            "line-opacity": 0.7
        }
    }, {
        "id": "gl-draw-polygon-and-line-vertex-halo-active",
        "type": "circle",
        "filter": ["all", ["==", "meta", "vertex"], ["==", "$type", "Point"], ["!=", "mode", "static"]],
        "paint": {
            "circle-radius": 6,
            "circle-color": "#e14673"
        }
    }, {
        "id": "gl-draw-polygon-and-line-vertex-active",
        "type": "circle",
        "filter": ["all", ["==", "meta", "vertex"], ["==", "$type", "Point"], ["!=", "mode", "static"]],
        "paint": {
            "circle-radius": 3,
            "circle-color": "#FFF",
        }
    }]
});

map.addControl(draw);

map.on('draw.create', updateArea);
map.on('draw.delete', updateArea);
map.on('draw.update', updateArea);

//store 2 styles in an array
const styles = ['mapbox://styles/m4xw3ll/cl9zp5f6j00ez14qtletemydp', 'mapbox://styles/m4xw3ll/cl9y23u9m00jt14o2fipec794'];

//add custom controls to the map to change the map style
class CustomControl {
    onAdd(map) {
        this._map = map;
        this._container = document.createElement('div');
        this._container.className = 'mapboxgl-ctrl mapboxgl-ctrl-group';
        //when the button is clicked, the map style is changed
        this._container.addEventListener('click', function () {
            
            //get the current style
            let currentStyle = map.getStyle();
            //get the current style name
            let currentStyleName = currentStyle.name;
            //when the button is clicked, the map style is changed
            //if the current style is the first style in the array, the next style is
            //the second style in the array
            if (currentStyleName === styles[0]) {
                map.setStyle(styles[1]);
            } else if(currentStyleName === styles[1]) {
                //if the current style is the second style in the array, the next style is
                //the first style in the array
                map.setStyle(styles[0]);
            }

            // if (map.getStyle().name == 'Monochrome Dark') {
            //     map.setStyle('mapbox://styles/m4xw3ll/cl9y23u9m00jt14o2fipec794');
            // } else {
            //     map.setStyle('mapbox://styles/m4xw3ll/cl9zp5f6j00ez14qtletemydp');
            // }
        });

        this._container.innerHTML = '<div class="tools-box">' +
        '<button>' +
        '<span class="mapbxgl-ctrl-icon layerIcon" aria-hidden="true" title="Description"><img src="../img/map_FILL0_wght400_GRAD0_opsz48.png"></span>' +
        '</button>' +
        '</div>';
        return this._container;
    }
    onRemove() {
        this
            ._container
            .parentNode
            .removeChild(this._container);
        this._map = undefined;
    }
}

map.addControl(new CustomControl());


//add dynamic custom marker to the map
//get the coordinates of the plane from the api
let planeCoordinates = [13.845101, 46.601179];

//define geojson for the marker
const geojson = {
    "type": "FeatureCollection",
    "features": [{
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": planeCoordinates
        }
    }]
};

//add the marker to the map
for (const feature of geojson.features) {
    const el = document.createElement('div');
    el.className = 'marker';
    new mapboxgl.Marker(el)
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
        "features": [{
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": planeCoordinates
            }
        }]
    };

    //add the marker to the map
    for (const feature of geojson.features) {
        const el = document.createElement('div');
        el.className = 'marker';
        new mapboxgl.Marker(el)
            .setLngLat(feature.geometry.coordinates)
            .addTo(map);
    }
}, 5000);

//generate a gpx file from the coordinates
function generateGPX(coordinates) {
    var gpx = '<?xml version="1.0" encoding="UTF-8"?>';
    gpx += '<gpx version="1.1" creator="AEHTER WCP" xmlns="http://www.topografix.com/GPX/1/1">' + '\n';
    gpx += '<metadata />' + '\n';
    //add the coordinates to the gpx file as waypoints
    for (var i = 0; i < coordinates.length; i++) {
        gpx += '<wpt lat="' + coordinates[i][1] + '" lon="' + coordinates[i][0] + '"><name>"'+ i +'"</name></wpt>' + '\n';
    }
    gpx += '</gpx>';
    return gpx;
}

//output the coordinates of the drawn path in the paragraph with id="waypoint-list" with only 6 decimal places
//if there are more than 10 waypoints, make the paragraph scrollable and set a max height of 200px
function outputWaypoints(coordinates) {
    var waypointList = document.getElementById('waypoint-list');
    waypointList.innerHTML = '';
    for (var i = 0; i < coordinates.length; i++) {
        waypointList.innerHTML += '<li>' + coordinates[i][0].toFixed(6) + ', ' + coordinates[i][1].toFixed(6) + '</li>';
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
    var blob = new Blob([gpx], {
        type: 'text/plain'
    });
    var url = URL.createObjectURL(blob);
    var link = document.createElement('a');
    link.href = url;
    link.download = 'path.gpx';
    link.click();

    // FIXME: CODE BELOW NOT WORKING! (send the gpx file to the server)
    // //save the gpx file internally on the server in the folder "gpx"
    // //get path of the gpx folder
    // var path = '../../gpx';
    // //get the name of the gpx file
    // var name = 'path.gpx';
    // //get the content of the gpx file
    // var content = gpx;
    // //save the gpx file
    // $.ajax({
    //     url: 'upload.php',
    //     type: 'POST',
    //     data: {
    //         path: path,
    //         name: name,
    //         content: content
    //     },
    //     success: function (data) {
    //         console.log(data);
    //     }
    // });
    
    //list the coordinates of the drawn path in the paragraph with id="waypoint-list"
    outputWaypoints(data.features[0].geometry.coordinates);
}
