// use strict

'use strict';


//html elements
const loadButton = document.getElementById('load');

//Mapbox map
//access token
mapboxgl.accessToken = 'pk.eyJ1IjoibTR4dzNsbCIsImEiOiJjbDl4NzhsbGMwNzY3M3Fub3JhbnZldGhnIn0.9Y1af9ijoJiMuKxBe0CZyw';

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
    }
});

map.addControl(draw);

map.on('draw.create', updateArea);
map.on('draw.delete', updateArea);
map.on('draw.update', updateArea);

//generate a gpx file from the coordinates
function generateGPX(coordinates) {
    var gpx = '<?xml version="1.0" encoding="UTF-8"?>';
    gpx += '<gpx version="1.1" creator="Mapbox GL Draw" xmlns="http://www.topografix.com/GPX/1/1">' + '\n';
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

    //save the gpx file internally on the server in the folder "gpx"
    

    //list the coordinates of the drawn path in the paragraph with id="waypoint-list"
    outputWaypoints(data.features[0].geometry.coordinates);
    
}
