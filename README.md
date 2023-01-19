<div align="center">
    <hr>
    <h1>AAE HAWK</h1>
    <p>Groundcode<p>
    <hr>
</div>

# VERSION #

0.2.0

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

1. Install the requirements with pip:
```bash
pip install -r requirements.txt
```
2. Add the file `token.py` to the [missioncontrol](missioncontrol) folder with the following content:
```python
MAP_TOKEN = 'YOUR_MAPBOX_TOKEN'
```

# USAGE #
1. Connect the ground station to the computer via USB
2. Start the ground station
```bash
python mission-control.py
```
3. Add a flight path to the map by using the menu bar on the right side of the map
4. Upload the flight path to the ground station
5. Start the flight

# LICENSE #
This project is licensed under the GNU GENERAL PUBLIC License - see the [LICENSE](LICENSE) file for details

