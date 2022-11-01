// use strict

'use strict';

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