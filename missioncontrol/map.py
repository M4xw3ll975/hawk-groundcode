import json
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from missioncontrol.token import MAP_TOKEN

def main() :
    #create the app
    app = QApplication(sys.argv)
    #set style
    # Force the style to be the same on all OSs:
    app.setStyle("Fusion")
    # Now use a palette to switch to dark colors:
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(2, 36, 49))
    palette.setColor(QPalette.WindowText, Qt.white)
    app.setPalette(palette)

    #create the main window
    window = MainWindow()
    #show the window
    window.show()
    #execute the app
    sys.exit(app.exec_())

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        #set the window title
        self.setWindowTitle("Mission Control")
        #set the window size to resizeable
        self.resize(1500, 800)

        #set up the UI
        self.map_view = QWebEngineView()
        self.map_view.setHtml('''
            <!DOCTYPE html>
            <html>
                <head>
                    <meta charset="utf-8">
                    <title>Add a default marker to a web map</title>
                    <meta name="viewport" content="initial-scale=1,maximum-scale=1,user-scalable=no">
                    <link href="https://api.mapbox.com/mapbox-gl-js/v2.12.0/mapbox-gl.css" rel="stylesheet">
                    <script src="https://api.mapbox.com/mapbox-gl-js/v2.12.0/mapbox-gl.js"></script>
                    <link rel="stylesheet" href="https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-draw/v1.2.2/mapbox-gl-draw.css" type="text/css">
                    <script src="https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-draw/v1.2.2/mapbox-gl-draw.js"></script>
                    <style>
                    body { margin: 0; padding: 0; }
                    #map { position: absolute; top: 0; bottom: 0; width: 100%; }
                    </style>
                </head>
                <body>
                    <div id="map"></div>

                <script>
                	mapboxgl.accessToken = "'''+MAP_TOKEN+'''";
                    const map = new mapboxgl.Map({
                        container: 'map',
                        // Choose from Mapbox's core styles, or make your own style with Mapbox Studio
                        style: 'mapbox://styles/m4xw3ll/clb6asku6002414pkbmykld79',
                        center: [13.845101, 46.601179],
                        zoom: 15
                    });

                    //define the draw variable
                    var draw = new MapboxDraw({
                        displayControlsDefault: true
                    });

                    //add ability to draw lines
                    map.addControl(draw);

                    //return the points of the drawn line
                    function getLine() {
                        //get the drawn line
                        var data = draw.getAll();
                        return data;
                    }

                </script>
                </body>
            </html>
        ''')
        self.button1 = QPushButton("Upload Route")
        self.button1.clicked.connect(self.on_button1_clicked)
        self.button2 = QPushButton("SEND IT!")
        self.button2.clicked.connect(self.on_button2_clicked)
        self.button3 = QPushButton("ABORT!")
        self.button3.clicked.connect(self.on_button3_clicked)

        #text output for the returned points withouth the abbility to edit it
        self.text = QTextEdit()
        self.text.setReadOnly(True)

        self.button1.setFixedSize(120, 50)
        self.button2.setFixedSize(120, 50)
        self.button3.setFixedSize(120, 50)
        self.text.setFixedSize(120, 500)

        self.map_view.setContentsMargins(10, 10, 10, 10)

        #put the button is QVBox layout and then put the QVBox layout in the QHBox layout with the map
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.button1)
        buttonLayout.addWidget(self.button2)
        buttonLayout.addWidget(self.button3)
        buttonLayout.addWidget(self.text)
        buttonLayout.addStretch(1)

        mainLayout = QHBoxLayout()
        mainLayout.addLayout(buttonLayout)
        mainLayout.addWidget(self.map_view)

        self.setLayout(mainLayout)

    def on_button1_clicked(self):
        self.map_view.page().runJavaScript("getLine()", self.on_markers_retrieved)
        

    def on_markers_retrieved(self, markers_data):
        markers = markers_data
        #extract the points from the returned data
        markersExtracted = markers['features'][0]['geometry']['coordinates']
        #print the returned points in the text output
        self.text.setText(str(markersExtracted))

        #save the points in a json file
        with open("markers.json", "w") as f:
            json.dump(markers, f)
        
        #upload the points to the drone
        self.upload_to_drone(markersExtracted)
        
    def upload_to_drone(self, markers):
        print("UPLOAD TO DRONE")
        print(markers)
        #TODO: send the points to the drone via serial communication

    def on_button2_clicked(self):
        print("SEND IT!")
        #TODO: send the command to the drone to start the mission
        
    def on_button3_clicked(self):
        print("ABORT!")
        #TODO: send the command to the drone to abort the mission

