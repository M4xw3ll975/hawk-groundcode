from flask import Flask, request, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)

class Waypoint:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

class Mission:
    def __init__(self):
        self.mission_waypoints = []

    def add_waypoint(self, waypoint):
        self.mission_waypoints.append(waypoint)
    
    def calculate_center(self):
        lat_sum = 0
        lon_sum = 0
        for waypoint in self.mission_waypoints:
            lat_sum += float(waypoint.lat)
            lon_sum += float(waypoint.lon)
        return Waypoint(lat_sum/len(self.mission_waypoints), lon_sum/len(self.mission_waypoints))
    
    def insert_waypoints(self, file):
        with open(file, 'r') as f:
            data = f.read()
        soup = BeautifulSoup(data, 'xml')
        waypoints = soup.find_all('wpt')
        for waypoint in waypoints:
            self.add_waypoint(Waypoint(waypoint['lat'], waypoint['lon']))

    def waypoints_string(self):
        string = ""
        for waypoint in self.mission_waypoints:
            waypoint_number = str(self.mission_waypoints.index(waypoint) + 1)
            string += waypoint_number + ":" + waypoint.lat + ',' + waypoint.lon + ";"
        return string


hawk = Mission()
hawk.insert_waypoints("redlining.gpx") 
app.jinja_env.globals.update(waypoint_list=hawk.mission_waypoints)
app.jinja_env.globals.update(waypoint_center=hawk.calculate_center())


@app.route('/')
def index():
    return render_template('index.html')
