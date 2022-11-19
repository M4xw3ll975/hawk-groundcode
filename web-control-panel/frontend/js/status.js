// Buttonstatus.js
// This file is part of Web Control Panel
// Author: Maximilian Birnbacher

// functions to display the status of the plane

'use strict';

function ButtonStatus(htmlBtn, status) {
    if (status == 'OK') {
        //set background color to green
        htmlBtn.style.backgroundColor = '#4CAF50';
        htmlBtn.style.color = 'white';
    } else if (status == 'ERROR') {
        //set background color to red
        htmlBtn.style.backgroundColor = '#ff0000';
        htmlBtn.style.color = 'white';
    } else if (status == 'WARNING') {
        //set background color to orange
        htmlBtn.style.backgroundColor = '#ff9800';
        htmlBtn.style.color = 'white';
    } else if (status == 'DISABLED') {
        //set background color to dark grey and text color to light grey
        htmlBtn.style.backgroundColor = '#424242';
        htmlBtn.style.color = '#9E9E9E';
    }
}

//display engine throttle
function engineThrottle(throttle, htmlDiv, position) {
    //clear the div
    htmlDiv.innerHTML = '';
    // display engine thurst with a tui barchart
    // get the engine thurst from the api
    let engineThurst = throttle;
    let formatedEngineThurst = engineThurst / 4;
    // get div element
    const barchart = htmlDiv;
    // create a new tui barchart
    if (position == 'LEFT') {

        barchart.innerHTML = 'ENGINE ' + position + '&nbsp [';
    } else {
        barchart.innerHTML = 'ENGINE ' + position + ' [';
    }

    // display the engine thurst in the div with the id left-eng
    // run a for loop to animate the gauge
    for (let i = 0; i < 25; i++) {
        if (i < formatedEngineThurst) {
            //add color to the barchart
            if (i < 10) {
                //green for the first 10 bars
                barchart.innerHTML += '<span style="color: #00ff00;">|</span>';
            }
            if (i > 10 && i < 20) {
                //orange for the second 10 bars
                barchart.innerHTML += '<span style="color: #ff9900;">|</span>';
            }
            if (i > 20) {
                //red for the last 5 bars
                barchart.innerHTML += '<span style="color: #ff0000;">|</span>';
            }
        } else {
            barchart.innerHTML += '&nbsp';
        }
    }
    if (position == 'RIGHT') {
        //remove the last 2 characters from the string
        barchart.innerHTML = barchart.innerHTML.slice(0, -6);
    }
    barchart.innerHTML += '] ' + engineThurst + '% &nbsp &nbsp';
}