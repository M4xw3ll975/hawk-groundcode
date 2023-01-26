<div align="center">
    <hr>
    <h1>AAI HAWK</h1>
    <p>Groundcode<p>
    <hr>
</div>

# VERSION #

0.2.2



# FEATURES #
- PyQT5 App running on Windows, Linux and Mac
- Map to draw the flight path
- Flight path can be uploaded to the ground station via serial connection
- Start and stop the current flight



# REQUIREMENTS #
You need the following to use this software:
1. A mapbox token to use the map. You can get one for free [here](https://www.mapbox.com/).
2. Python 3.9.1 or higher
3. Pip version 20.2.3 or higher
4. A compatible ground station with the latest firmware
5. A PC/Laptop with a USB port running Windows, Linux or Mac
6. A internet connection to use the map



# INSTALLATION #
## Windows:
1. Download the latest version of the [setup-win.py](setup-win.py) file and run it
```bash	
python setup-win.py
```

## Linux/Mac:
1. Install the requirements with pip:
```bash
pip install -r requirements.txt
```
2. Add the file `token.py` to the [missioncontrol](missioncontrol) folder with the following content:
```python
MAP_TOKEN = 'YOUR_MAPBOX_TOKEN'
```



# USAGE #
## Start up: ##
1. Connect the ground station to the computer via USB
2. Start the ground station
```bash
python mission-control.py
```
3. Add a flight path to the map by using the menu bar on the right side of the map
4. Upload the flight path to the ground station
5. Start the flight

## Guide: ##

When starting the application, you will see a map, a map navigation bar, and 3 buttons. The map navigation bar allows you to zoom in and out of the map, and move around the map. The buttons are as follows:

1. The first button is the 'Upload Route' button. This buttonallows you to add a mission to the map. You can add a mission by using the drawingfunctionality on the map, and then clicking on the 'Upload Route' button. The uploadwill take place in the background, there is no user interaction needed.
2. The second button is the 'SEND IT!' button. This button allowsyou to start the mission. You can start the mission by clicking on the 'SEND IT!'button. The Plane will use the last uploaded mission.
3. The third button is the 'ABORT!' button. This button allowsyou to abort the mission. You can abort the mission by clicking on the 'ABORT!' button.The Plane will stop the mission and return to the home position or use the build in FTS

To draw on the map, you can use the following tools that are onthe right side of the map:
1. Line plotter - to draw lines on the map
2. Polygon plotter - to draw areas on the map
3. Marker - to place single points on the map
4. Eraser - to remove points from the map
5. Combine - to combine multiple points into a single point
6. Uncombine - to split a single point into multiple points

For more information, please take a look at the readme file thatis included in the installation folder or at our documentation.

#### Have fun using AETHER Mission Control! ####

---

# DOCUMENTATION #
The documentation can be found [here](Documentation).

# LICENSE #
This project is licensed under the GNU GENERAL PUBLIC License - see the [LICENSE](LICENSE) file for details

