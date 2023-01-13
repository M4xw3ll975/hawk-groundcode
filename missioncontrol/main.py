#pyQT5 mission control app for the plan with a map by mapboxGL
#import the necessary modules
import io
import sys
import PyQt5.QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
import ipyleaflet

from missioncontrol.token import MAP_TOKEN

#main function
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



#main window class
class MainWindow(QMainWindow) :
    #constructor
    def __init__(self) :
        #call the super class constructor
        super().__init__()
        #set the window title
        self.setWindowTitle("Mission Control")
        #set the window size
        self.setFixedSize(1500, 800)
        #set up the UI
        self.buttonUI()

    #UI function
    def buttonUI(self):
        buttonUp = QtWidgets.QPushButton(self.tr("Upload path"))
        buttonClear = QtWidgets.QPushButton(self.tr("Clear path"))
        buttonSend = QtWidgets.QPushButton(self.tr("SEND IT!"))
        buttonBreak = QtWidgets.QPushButton(self.tr("ABORT!"))

        buttonUp.setFixedSize(120, 50)
        buttonClear.setFixedSize(120, 50)
        buttonSend.setFixedSize(120, 50)
        buttonBreak.setFixedSize(120, 50)

        self.view = QtWebEngineWidgets.QWebEngineView()
        self.view.setContentsMargins(10, 10, 10, 10)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        lay = QtWidgets.QHBoxLayout(central_widget)

        button_container = QtWidgets.QWidget()
        vlay = QtWidgets.QVBoxLayout(button_container)
        vlay.setSpacing(20)
        vlay.addStretch()
        vlay.addWidget(buttonUp)
        vlay.addWidget(buttonClear)
        vlay.addWidget(buttonSend)
        vlay.addWidget(buttonBreak)
        vlay.addStretch()
        lay.addWidget(button_container)
        lay.addWidget(self.view, stretch=1)

        # map = folium.Map(
        #     location=[46.601179, 13.845101], 
        #     tiles="Stamen Terrain", 
        #     # tiles="https://api.mapbox.com/styles/v1/m4xw3ll/clb6asku6002414pkbmykld79/tiles/256/{z}/{x}/{y}@2x?access_token=" + MAP_TOKEN,
        #     # attr="Mapbox",
        #     zoom_start=15
        # )

        
        #define map with ipyleaflet
        map = ipyleaflet.Map(
        center=(46.601179, 13.845101),
        # tiles="Stamen Terrain",
        tiles="https://api.mapbox.com/styles/v1/m4xw3ll/clb6asku6002414pkbmykld79/tiles/256/{z}/{x}/{y}@2x?access_token=" + MAP_TOKEN,
        attr="Mapbox",
        zoom=15)

       
        #display the map without saving it to a file




        

        # data = io.BytesIO()
        #display the ipyleaflet map
        # map.save(data, close_file=False)
        # self.view.setHtml(data.getvalue().decode())

        # self.view.setHtml(data.getvalue().decode())




        
        





