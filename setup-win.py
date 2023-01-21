#this is the setup tool for mission control
#it is a pyqt5 application
#Author: Maximilian Birnbacher

import getpass
import threading
import time
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QProgressBar
from PyQt5.QtCore import Qt
import sys
import subprocess
import platform
import os

#views
#welcome dialog
class WelcomeDialog(QDialog):
    def __init__(self):
        super().__init__()

        #set a fixed size for the application
        self.setFixedSize(700, 500)
        #set the title of the application
        self.setWindowTitle("AETHER Mission Control Setup")

        # Create a label
        self.label = QLabel("Welcome to the setup of AETHER Mission Control")
        #create a text
        self.text = QLabel("This wizard will guide you through the process of setting up your AETHER Mission Control application")
        self.text2 = QLabel("This application is made by AETHER Aerospace Industries")
        self.text3 = QLabel("Please note that this application is still in development and may contain bugs")
        self.text4 = QLabel("Please note that you need a Mapbox token to use this application")

        # Create a button in the dialog
        self.button = QPushButton("Next")
        
        # Create a button in the dialog
        self.button2 = QPushButton("Cancel")

        # Create a vertical box layout and add the above created widgets
        layout = QVBoxLayout()
        layoutText = QVBoxLayout()
        layoutText.addWidget(self.label)
        layoutText.addWidget(self.text)
        layoutText.addWidget(self.text2)
        layoutText.addWidget(self.text3)
        layoutText.addWidget(self.text4)
        #remove the spacing between the text
        layoutText.setSpacing(0)
        layout.addLayout(layoutText)
        #align the text to the top
        layout.setAlignment(layoutText, Qt.AlignTop)

        #have the buttons as a bottom navigation bar
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.button)
        buttonLayout.addWidget(self.button2)
        layout.addLayout(buttonLayout)

        # #add a space between the text and the buttons so the windows size is not changed
        # layout.addSpacing(20)

        # Set the layout to the dialog
        self.setLayout(layout)

        # Add button signal
        self.button.clicked.connect(self.next)
        self.button2.clicked.connect(self.cancel)

    def next(self):
        #move to the next dialog
        self.accept()

    def cancel(self):
        #cancel the setup
        self.reject()

#check if git and python is installed
class CheckDialog(QDialog):
    def __init__(self):
        super().__init__()
        #set a fixed size for the application
        self.setFixedSize(700, 500)
        #set the title of the application
        self.setWindowTitle("AETHER Mission Control Setup - Please wait...")

        # Create a label
        self.label = QLabel("Checking if Git is installed")

        #output of the result of the checkGit function
        self.output = QLabel()

        #create a progress bar
        self.progress = QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setValue(0)

        # Create a button in the dialog
        self.button = QPushButton("Next")
        #disable the next button
        self.button.setEnabled(False)
        
        # Create a button in the dialog
        self.button2 = QPushButton("Cancel")

        # Create a vertical box layout and add the above created widgets
        layout = QVBoxLayout()
        layoutText = QVBoxLayout()
        layoutText.addWidget(self.label)
        layoutText.addWidget(self.progress)
        layoutText.addWidget(self.output)
        #remove the spacing between the text
        layoutText.setSpacing(0)
        layout.addLayout(layoutText)
        #align the text to the top
        layout.setAlignment(layoutText, Qt.AlignTop)

        #have the buttons at the bottom and horizontally aligned to each other
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.button)
        buttonLayout.addWidget(self.button2)
        layout.addLayout(buttonLayout)

        # Set the layout to the dialog
        self.setLayout(layout)

        # Add button signal
        self.button.clicked.connect(self.next)
        self.button2.clicked.connect(self.cancel)

    def next(self):
        #move to the next dialog
        self.accept()

    def cancel(self):
        #cancel the setup
        self.reject()

    #method to change the value of the progress bar
    def changeProgess(self, value):
        self.progress.setValue(value)

    #method to change the text of the output label
    def changeText(self, text):
        self.output.setText(text)

    #method to get the text of the output label
    def getText(self):
        return self.output.text()

    #method to change the text color of the output label
    def changeColor(self, color):
        self.output.setStyleSheet("color: " + color + "")

    #metod to change the text of the label
    def changeLabel(self, text):
        self.label.setText(text)
    
    #method to enable the next button
    def enableNext(self):
        self.button.setEnabled(True)

    

#input dialog for the mapbox token
class InputDialog(QDialog):
    def __init__(self):
        super().__init__()
        #set a fixed size for the application
        self.setFixedSize(700, 500)
        #set the title of the application
        self.setWindowTitle("AETHER Mission Control Setup")

        # Create a label
        self.label = QLabel("Enter your Mapbox token:")

        # Create a line edit
        self.line_edit = QLineEdit()

        # Create a button in the dialog
        self.button = QPushButton("Next")
        
        # Create a button in the dialog
        self.button2 = QPushButton("Cancel")

        # Create a vertical box layout and add the above created widgets
        layout = QVBoxLayout()
        layoutText = QVBoxLayout()
        layoutText.addWidget(self.label)
        layoutText.addWidget(self.line_edit)
        #remove the spacing between the text
        layoutText.setSpacing(0)
        layout.addLayout(layoutText)
        #align the text to the top
        layout.setAlignment(layoutText, Qt.AlignTop)

        #have the buttons at the bottom and horizontally aligned to each other
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.button)
        buttonLayout.addWidget(self.button2)
        layout.addLayout(buttonLayout)

        # Set the layout to the dialog
        self.setLayout(layout)

        # Add button signal
        self.button.clicked.connect(self.next)
        self.button2.clicked.connect(self.cancel)

    def next(self):
        #get the text from the line edit
        self.text = self.line_edit.text()
        #move to the next dialog
        self.accept()

    def cancel(self):
        #cancel the setup
        self.reject()

#Start up information dialog
class FinishDialog(QDialog):
    def __init__(self):
        super().__init__()
        #set a fixed size for the application
        self.setFixedSize(700, 500)
        #set the title of the application
        self.setWindowTitle("AETHER Mission Control Setup")

        # Create a label
        self.label = QLabel("Thanks for installing AETHER Mission Control!")
        # Create a label
        self.label2 = QLabel("This guide will help you use the application.")
        self.label3 = QLabel("When starting the application, you will see a map, a map navigation bar, and 3 buttons. The map navigation bar allows you to zoom in and out of the map, and move around the map. The buttons are as follows:")
        self.label4 = QLabel("1. The first button is the 'Upload Route' button. This button allows you to add a mission to the map. You can add a mission by using the drawing functionality on the map, and then clicking on the 'Upload Route' button. The upload will take place in the background, there is no user interaction needed.")
        self.label5 = QLabel("2. The second button is the 'SEND IT!' button. This button allows you to start the mission. You can start the mission by clicking on the 'SEND IT!' button. The Plane will use the last uploaded mission.")
        self.label6 = QLabel("3. The third button is the 'ABORT!' button. This button allows you to abort the mission. You can abort the mission by clicking on the 'ABORT!' button. The Plane will stop the mission and return to the home position or use the build in FTS.")
        self.label7 = QLabel("To draw on the map, you can use the following tools that are on the right side of the map:")
        self.label8 = QLabel("1. Line plotter - to draw lines on the map")
        self.label9 = QLabel("2. Polygon plotter - to draw areas on the map")
        self.label10 = QLabel("3. Marker - to place single points on the map")
        self.label11 = QLabel("4. Eraser - to remove points from the map")
        self.label12 = QLabel("5. Combine - to combine multiple points into a single point")
        self.label13 = QLabel("6. Uncombine - to split a single point into multiple points")
        self.label14 = QLabel("For more information, please take a look at the readme file that is included in the installation folder or at our documentation.")
        self.label15 = QLabel("Have fun using AETHER Mission Control!")

        # Create a button in the dialog
        self.button = QPushButton("Launch Mission Control")
        
        # Create a button in the dialog
        self.button2 = QPushButton("Cancel")

        # Create a vertical box layout and add the above created widgets
        layout = QVBoxLayout()
        layoutText = QVBoxLayout()
        layoutText.addWidget(self.label)
        layoutText.addWidget(self.label2)
        layoutText.addWidget(self.label3)
        layoutText.addWidget(self.label4)
        layoutText.addWidget(self.label5)
        layoutText.addWidget(self.label6)
        layoutText.addWidget(self.label7)
        layoutText.addWidget(self.label8)
        layoutText.addWidget(self.label9)
        layoutText.addWidget(self.label10)
        layoutText.addWidget(self.label11)
        layoutText.addWidget(self.label12)
        layoutText.addWidget(self.label13)
        layoutText.addWidget(self.label14)
        layoutText.addWidget(self.label15)

        #wrap the text
        self.label.setWordWrap(True)
        self.label2.setWordWrap(True)
        self.label3.setWordWrap(True)
        self.label4.setWordWrap(True)
        self.label5.setWordWrap(True)
        self.label6.setWordWrap(True)
        self.label7.setWordWrap(True)
        self.label8.setWordWrap(True)
        self.label9.setWordWrap(True)
        self.label10.setWordWrap(True)
        self.label11.setWordWrap(True)
        self.label12.setWordWrap(True)
        self.label13.setWordWrap(True)
        self.label14.setWordWrap(True)
        self.label15.setWordWrap(True)

        #remove the spacing between the text
        layoutText.setSpacing(0)
        layout.addLayout(layoutText)
        #align the text to the top
        layout.setAlignment(layoutText, Qt.AlignTop)

        #have the buttons at the bottom and horizontally aligned to each other
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.button)
        buttonLayout.addWidget(self.button2)
        layout.addLayout(buttonLayout)

        # Set the layout to the dialog
        self.setLayout(layout)

        # Add button signal
        self.button.clicked.connect(self.next)
        self.button2.clicked.connect(self.cancel)

    def next(self):
        #move to the next dialog
        self.accept()

    def cancel(self):
        #cancel the setup
        self.reject()

def checkRequirements(CheckDialog):
    #check if git is installed
    def checkGit():
        # Check the current operating system
        if platform.system() == "Windows":
            try:
                # Try running the 'git' command
                subprocess.run(['git', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return True
            except subprocess.CalledProcessError:
                # 'git' command returned a non-zero exit code, indicating that Git is not installed
                return False
        else:
            # You can add other platforms check as well
            return False

    #check if the python version is 3.6 or higher
    def checkPython():
        #check if the python version is 3.6 or higher
        if sys.version_info[0] >= 3 and sys.version_info[1] >= 6:
            return True
        else:
            return False
    
    #check if the folder \hawk-groundcode exists in c:\Users\%username%\ and if it does not exist, create it
    def checkFolder():
        #get the current user
        user = getpass.getuser()
        #check if the folder exists
        if os.path.isdir("C:\\Users\\" + user + "\\hawk-groundcode"):
            return True
        else:
            #create the folder
            os.mkdir("C:\\Users\\" + user + "\\hawk-groundcode")
            return False
        
    #clone the repository
    def clone():
        #get the current user
        user = getpass.getuser()
        #change the directory to the folder hawk-groundcode
        os.chdir("C:\\Users\\" + user + "\\hawk-groundcode")
        #if the clone is successful return true
        try:
            #clone the repository
            os.system("git clone https://github.com/AetherAerospace/hawk-groundcode.git .")
            #return true when the cloning is done
            return True
        except:
            #return false if the cloning is not successful
            return False

    #create a virtual environment in the folder hawk-groundcode
    def createVirtualEnv():
        #get the current user
        user = getpass.getuser()
        #change the directory to the folder hawk-groundcode
        os.chdir("C:\\Users\\" + user + "\\hawk-groundcode")
        #create the virtual environment
        os.system("python -m venv env")
        #activate the virtual environment with the command env\Scripts\activate
        os.system("env\Scripts\activate")
        #install the requirements
        os.system("pip install -r requirements.txt")
        #return true if the requirements are installed
        return True

    #check if git is installed by calling the checkGit function and increase the progress bar value to 25 if it is installed
    if checkGit() == True:
        #delay of 1 second
        time.sleep(1)
        #set the progress bar value to 25
        CheckDialog.changeProgess(25)
        #change the color of the text to green
        CheckDialog.changeColor("green")
        CheckDialog.changeText("Git is installed")
        #now check if python is installed
        CheckDialog.changeLabel("Checking if Python is installed")

        #check if python is installed by calling the checkPython function and set the progress bar value to 30 if it is installed
        if checkPython() == True:
            #delay of 1 second
            time.sleep(1)
            CheckDialog.changeProgess(30)
            #change the color of the text to green
            CheckDialog.changeColor("green")
            #append the text with a new line and the text that python is installed
            CheckDialog.changeText(CheckDialog.getText() + "\nPython is installed")
            #now check if the folder mission-control exists
            CheckDialog.changeLabel("Checking if the folder hawk-groundcode exists")
            
            #check if the folder mission-control exists by calling the checkFolder function and set the progress bar value to 54 if it is installed
            if checkFolder() == True:
                #delay of 1 second
                time.sleep(1)
                CheckDialog.changeProgess(54)
                #change the color of the text to green
                CheckDialog.changeColor("green")
                #append the text with a new line and the text that the folder mission-control exists
                CheckDialog.changeText(CheckDialog.getText() + "\nFolder hawk-groundcode exists")
                #now clone the repository
                CheckDialog.changeLabel("Cloning the repository")

                #clone the repository by calling the clone function and set the progress bar value to 90 if it is installed
                if clone() == True:
                    #delay of 1 second
                    time.sleep(1)
                    CheckDialog.changeProgess(90)
                    #change the color of the text to green
                    CheckDialog.changeColor("green")
                    #append the text with a new line and the text that the repository has been cloned
                    CheckDialog.changeText(CheckDialog.getText() + "\nRepository has been cloned")
                    #now create a virtual environment
                    CheckDialog.changeLabel("Creating a virtual environment")

                    #create a virtual environment by calling the createVirtualEnv function and set the progress bar value to 100 if it is installed
                    if createVirtualEnv() == True:
                        #delay of 1 second
                        time.sleep(1)
                        CheckDialog.changeProgess(100)
                        #change the color of the text to green
                        CheckDialog.changeColor("green")
                        #append the text with a new line and the text that the virtual environment has been created
                        CheckDialog.changeText(CheckDialog.getText() + "\nVirtual environment has been created")
                        #enable the next button
                        CheckDialog.enableNext()
                        #change the label to Installation complete
                        CheckDialog.changeLabel("Installation complete")
                    
            #if the folder mission-control does not exist write that the folder has been created
            else:
                #change the color of the text to red
                CheckDialog.changeColor("green")
                #append the text with a new line and the text that the folder mission-control has been created
                CheckDialog.changeText(CheckDialog.getText() + "\nFolder hawk-groundcode has been created")
                
                #clone the repository by calling the clone function and set the progress bar value to 90 if it is installed
                if clone() == True:
                    #delay of 1 second
                    time.sleep(1)
                    CheckDialog.changeProgess(90)
                    #change the color of the text to green
                    CheckDialog.changeColor("green")
                    #append the text with a new line and the text that the repository has been cloned
                    CheckDialog.changeText(CheckDialog.getText() + "\nRepository has been cloned")
                    #now create a virtual environment
                    CheckDialog.changeLabel("Creating a virtual environment")

                    #create a virtual environment by calling the createVirtualEnv function and set the progress bar value to 100 if it is installed
                    if createVirtualEnv() == True:
                        #delay of 1 second
                        time.sleep(1)
                        CheckDialog.changeProgess(100)
                        #change the color of the text to green
                        CheckDialog.changeColor("green")
                        #append the text with a new line and the text that the virtual environment has been created
                        CheckDialog.changeText(CheckDialog.getText() + "\nVirtual environment has been created")
                        #enable the next button
                        CheckDialog.enableNext()
                        #change the label to Installation complete
                        CheckDialog.changeLabel("Installation complete")

        #if python is not installed change the text of the output label
        else:
            #change the color of the text to red
            CheckDialog.changeColor("red")
            #set the text of the output label
            CheckDialog.changeText("Python is not installed")

    #else set the progress bar value to 0 and change the text of the output label
    else:
        #change the color of the text to red
        CheckDialog.changeColor("red")
        #set the text of the output label
        CheckDialog.changeText("Git is not installed")

#main function
def main():
    # Create an instance of QApplication
    app = QApplication(sys.argv)

    # Create an instance of your application's dialog
    dialog = WelcomeDialog()
    # Show the dialog
    dialog.show()

    # Execute the dialog event loop
    if dialog.exec_():
        # Create an instance of your application's dialog
        dialog = CheckDialog()
        # Show the dialog
        dialog.show()

        #check if requirements are installed
        checkRequirements(dialog)

        # Execute the dialog event loop
        if dialog.exec_():
            # Create an instance of your application's dialog
            dialog = InputDialog()
            # Show the dialog
            dialog.show()

            # Execute the dialog event loop
            if dialog.exec_():
                #get the current user
                user = getpass.getuser()
                #get the text from the line edit
                text = dialog.text
                #append the text with a prefix and a suffix
                text = "MAP_TOKEN = '" + text + "'"
                filePath = "C:\\Users\\" + user + "\\hawk-groundcode\\missioncontrol\\token.py"
                #create a file and write the text into hawk-groundcode\missioncontrol and name it token.py
                f = open(filePath, "w")
                f.write(text)
                f.close()
                
                #execute the dialog event loop
                dialog = FinishDialog()
                dialog.show()
                if dialog.exec_():
                    #start the mission-control.py file
                    os.system("python C:\\Users\\" + user + "\\hawk-groundcode\\mission-control.py")
                    #close the application
                    sys.exit()
            else:
                #close the application
                sys.exit()
        else:
            #close the application
            sys.exit()
    else:
        #close the application
        sys.exit()



if __name__ == "__main__":
    main()