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
    // style: 'mapbox://styles/examples/cjgiiz9ck002j2ss5zur1vjji',
    style: 'mapbox://styles/m4xw3ll/cl9y23u9m00jt14o2fipec794', //custom style
    center: [-87.661557, 41.893748],
    zoom: 10.7
});

//add zoom and rotation controls to the map.
map.addControl(new mapboxgl.NavigationControl());



//when load button is clicked open a promt file input dialog that allows the user to select a gpx file
loadButton.onclick = function() {
    let fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.gpx';
    fileInput.onchange = function() {
        //get the file
        let file = fileInput.files[0];

        //create a file reader
        let reader = new FileReader();

        //when the file is loaded
        reader.onload = function() {
            //get the file contents
            let fileContents = reader.result;

            //parse the gpx file
            let gpx = toGeoJSON.gpx(new DOMParser().parseFromString(fileContents, 'text/xml'));

            //add the gpx file to the map
            map.addSource('gpx', {
                type: 'geojson',
                data: gpx
            });

            //add the gpx file to the map as a layer
            map.addLayer({
                id: 'gpx',
                type: 'line',
                source: 'gpx',
                paint: {
                    'line-color': '#ff0000',
                    'line-width': 3
                }
            });
        };

        //read the file
        reader.readAsText(file);
    };
    fileInput.click();
    
};
