import json
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from missioncontrol.token import MAP_TOKEN
from missioncontrol.toserial import *

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
        #set window icon
        self.setWindowIcon(QIcon('missioncontrol\logoNewTextIndustries.png'))
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
                    <script src="https://unpkg.com/@turf/turf@6/turf.min.js"></script>
                    <div id="map"></div>
                    <script>
                        
                    	mapboxgl.accessToken = "'''+MAP_TOKEN+'''";
                        const map = new mapboxgl.Map({
                            container: 'map',
                            // Choose from Mapbox's core styles, or make your own style with Mapbox Studio
                            //style: 'mapbox://styles/m4xw3ll/cl9y23u9m00jt14o2fipec794', //monochrome
                            style: 'mapbox://styles/m4xw3ll/cldoajl2q001301p5ifjjfyjx', //navigation
                            center: [13.845101, 46.601179],
                            zoom: 16
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

                        //point for the plane icon
                        let point = {
                            "type": "FeatureCollection",
                            "features": [{
                                "type": "Feature",
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": [13.845101, 46.601179]
                                }
                            }]
                        };

                        function displayPlane() {
                            //get the coordinates of the drawn line
                            var line = getLine();

                            //get the first point of the drawn line
                            var pointZero = line.features[0].geometry.coordinates[0];
                            
                            
                            map.addLayer({
                                "id": "plane",
                                "type": "symbol",
                                "source": {
                                    "type": "geojson",
                                    "data": pointZero,
                                },
                                "layout": {
                                    "icon-image": "habicht-small",
                                    "icon-size": 1,
                                    "icon-rotate": 0,
                                    "icon-rotation-alignment": "map",
                                    "icon-allow-overlap": true,
                                    "icon-ignore-placement": true,
                                    "icon-color": "#FFFFFF"
                                }
                            });

                            //set the layer to the top
                            map.moveLayer("plane");
                        }


                        //simulate the route
                        function simulateRoute() {
                            console.log("simulateRoute called");
                            //get the drawn line
                            var data = draw.getAll();

                            //get the points of the drawn line
                            var points = data.features[0].geometry.coordinates;

                            //calculate the distance between the points
                            let lineDistance = turf.lineDistance(data.features[0]);

                            let arc = [];

                            //number of steps to use in the arc and animation, more steps means
                            //a smoother arc and animation, but too many steps will result in a
                            //low frame rate
                            let steps = 500;

                            //draw an arc that connects the first point to the second point of the line, and so on
                            for (let i = 0; i < lineDistance; i += lineDistance / steps) {
                                let segment = turf.along(data.features[0], i);
                                arc.push(segment.geometry.coordinates);
                            }
                            console.log("befor arc output");
                            console.log(arc);
                            console.log("after arc output");

                            //update the route with calculated arc coordinates
                            points = arc;

                            //used to increment the value of the point measurement against the route
                            let counter = 0;

                            //set the plane icon to the first point of the route
                            point.features[0].geometry.coordinates = points[0];
                            console.log("befor points output");
                            console.log(points);
                            console.log("after points output");
                            animateRoute(points);
                            
                        }

                        //simulate the route
                        function animateRoute(arc) {
                            console.log("animateRoute called");
                            //set the point to the first point of the route
                            point.features[0].geometry.coordinates = arc[0];

                            //add plane icon to map
                            map.addLayer({
                                "id": "plane",
                                "type": "symbol",
                                "source": {
                                    "type": "geojson",
                                    "data": point
                                },
                                "layout": {
                                    "icon-image": "airport",
                                    "icon-size": 1.5,
                                    "icon-rotate": ["get", "bearing"],
                                    "icon-rotation-alignment": "map",
                                    "icon-allow-overlap": true,
                                    "icon-ignore-placement": true
                                }
                            });

                            let counter = 0;

                            //update the plane icon every 100ms
                            let interval = setInterval(function() {
                                if (counter >= arc.length) {
                                    clearInterval(interval);
                                    return;
                                } else {
                                    //update the plane icon coordinates
                                    point.features[0].geometry.coordinates = arc[counter];
                                    //update the plane icon
                                    console.log(point.features[0].geometry.coordinates);
                                    console.log(point)
                                    map.getSource("point").setData(point);
                                    //request the next frame of animation as long as the end has not been reached
                                    requestAnimationFrame(function() {
                                        //update the plane icon bearing so that it is in line with the next point
                                        point.features[0].properties.bearing = turf.bearing(
                                            turf.point(arc[counter - 1]),
                                            turf.point(arc[counter])
                                        );
                                        //update the plane icon
                                        map.getSource("point").setData(point);
                                    });

                                    counter = counter + 1;

                                }
                            }, 100);
                        }

                    </script>
                </body>
            </html>
        ''')
        #buttons
        # self.simulateButton = QPushButton("Simulate Route")
        # self.simulateButton.clicked.connect(self.on_simulateButton_clicked)
        self.button1 = QPushButton("Upload Route")
        self.button1.clicked.connect(self.on_button1_clicked)
        self.button2 = QPushButton("SEND IT!")
        self.button2.clicked.connect(self.on_button2_clicked)
        self.button3 = QPushButton("ABORT!")
        self.button3.clicked.connect(self.on_button3_clicked)

        #text output for the returned points withouth the abbility to edit it
        self.text = QTextEdit()
        self.text.setReadOnly(True)

        #set the textfield to transparent
        # self.text.setStyleSheet("background-color: rgba(0, 0, 0, 0);")

        #set the size of the buttons and the text output
        self.button1.setFixedSize(120, 50)
        self.button2.setFixedSize(120, 50)
        self.button3.setFixedSize(120, 50)
        # self.simulateButton.setFixedSize(120, 50)
        #set the width of the text output to 120
        # self.text.setMinimumWidth(120)
        #set the size of the text output to 120 x max height
        # self.text.setMaximumSize(120, 16777215)
        self.text.setFixedSize(120, 845)

        #set the margins of the map
        self.map_view.setContentsMargins(10, 10, 10, 10)

        #put the button is QVBox layout and then put the QVBox layout in the QHBox layout with the map
        buttonLayout = QVBoxLayout()
        # buttonLayout.addWidget(self.simulateButton)
        buttonLayout.addWidget(self.button1)
        buttonLayout.addWidget(self.button2)
        buttonLayout.addWidget(self.button3)
        buttonLayout.addWidget(self.text)
        buttonLayout.addStretch(1)
        mainLayout = QHBoxLayout()
        mainLayout.addLayout(buttonLayout)
        mainLayout.addWidget(self.map_view)

        #set the layout
        self.setLayout(mainLayout)

    #simulate the route
    def on_simulateButton_clicked(self):
        #call the simulateRoute function in the map and print the returned data in the python console without the on_markers_retrieved function
        self.map_view.page().runJavaScript("displayPlane()", self.printData)

    #print the returned data in the python console without the on_markers_retrieved function
    def printData(self, data):
        print(data)

    #get the points of the drawn line
    def on_button1_clicked(self):
        self.map_view.page().runJavaScript("getLine()", self.on_markers_retrieved)
        
    #generate a json object with the points of the drawn line and send it to the drone
    def on_markers_retrieved(self, markers_data):
        markers = markers_data
        #extract the points from the returned data
        markersExtracted = markers['features'][0]['geometry']['coordinates']
        #print the returned points in the text output
        self.text.setText(str(markersExtracted))
        #get content of the text output
        tmp = self.text.toPlainText()
        tmp2 = tmp + "\n"
        self.text.setText(tmp2 + "Uploading to drone...")
        #get content of the text output
        tmp = self.text.toPlainText()
        tmp2 = tmp + "\n"
        self.text.setText(tmp2 + "DONE!")

        #save the points in a json file
        with open("markers.json", "w") as f:
            json.dump(markers, f)
        
        #upload the points to the drone
        # self.upload_to_drone(markersExtracted)

    
    #upload the json to the drone via serial communication
    def upload_to_drone(self, markers):
        print("\033[92m" + "UPLOAD TO DRONE" + "\033[0m")
        print(markers)

        #surround the communication with a try catch block to catch errors
        try:
            #send the points to the drone via serial communication
            #listen to the serial port
            read_thread = threading.Thread(target=read_from_serial)
            #send the points to the serial port
            write_thread = threading.Thread(target=write_to_serial, args=(markers,))

            #start the threads
            read_thread.start()
            write_thread.start()

            #wait for the threads to finish
            read_thread.join()
            write_thread.join()

            #close the serial port
            close_serial()

        except Exception as e:
            print("\033[91m" + "ERROR: " + str(e) + "\033[0m")
            #close the serial port
            close_serial()


    #send a command to the drone to start the mission
    def on_button2_clicked(self):
        print("\033[92m" + "SEND IT!" + "\033[0m")
        self.text.setText(str("SEND IT!"))
        #get content of the text output
        tmp = self.text.toPlainText()
        tmp2 = tmp + "\n"
        self.text.setText(tmp2 + "Starting mission...")
        #get content of the text output
        tmp = self.text.toPlainText()
        tmp2 = tmp + "\n"
        self.text.setText(tmp2 + "Mission started!")

        # #surrond the communication with a try catch block to catch errors
        # try:
        #     #send the command to the drone to start the mission
        #     #listen to the serial port
        #     read_thread = threading.Thread(target=read_from_serial)
        #     #send the command "SEND_IT" to the serial port
        #     write_thread = threading.Thread(target=write_to_serial, args=("SEND_IT",))

        #     #start the threads
        #     read_thread.start()
        #     write_thread.start()

        #     #wait for the threads to finish
        #     read_thread.join()
        #     write_thread.join()

        #     #close the serial port
        #     close_serial() 
        
        # except Exception as e:
        #     print("\033[91m" + "ERROR: " + str(e) + "\033[0m")
        #     #close the serial port
        #     close_serial()

    
    #send a command to the drone to abort the mission
    def on_button3_clicked(self):
        print("\033[91m" + "ABORT!" + "\033[0m")
        self.text.setText(str("ABORT!"))
        #get content of the text output
        tmp = self.text.toPlainText()
        tmp2 = tmp + "\n"
        self.text.setText(tmp2 + "Initializing FTS...")
        #get content of the text output
        tmp = self.text.toPlainText()
        tmp2 = tmp + "\n"
        self.text.setText(tmp2 + "FTS initialized!")
        #get content of the text output
        tmp = self.text.toPlainText()
        tmp2 = tmp + "\n"
        self.text.setText(tmp2 + "Signal lost!")
        #get content of the text output
        tmp = self.text.toPlainText()
        tmp2 = tmp + "\n"
        self.text.setText(tmp2 + "Aircraft has been terminated!")

        # #surrond the communication with a try catch block to catch errors
        # try:
        #     #send the command to the drone to abort the mission
        #     #listen to the serial port
        #     read_thread = threading.Thread(target=read_from_serial)
        #     #send the command "ABORT" to the serial port
        #     write_thread = threading.Thread(target=write_to_serial, args=("ABORT",))

        #     #start the threads
        #     read_thread.start()
        #     write_thread.start()

        #     #wait for the threads to finish
        #     read_thread.join()
        #     write_thread.join()

        #     #close the serial port
        #     close_serial() 

        # except Exception as e:
        #     print("\033[91m" + "ERROR: " + str(e) + "\033[0m")
        #     #close the serial port
        #     close_serial()