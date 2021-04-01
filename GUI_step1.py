# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 13:52:53 2018

@author: joseph.brunet
"""




import os
import os.path
import time

import sys


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton, QAction, QStatusBar, QFormLayout, QLabel, QLineEdit, 
    QVBoxLayout, QHBoxLayout, QSpacerItem, QMessageBox, QFrame, QSizePolicy, QInputDialog, QGroupBox, QRadioButton, 
    QFileDialog, QProgressBar, QDesktopWidget)
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QFont, QDoubleValidator, QPixmap, QPalette, QColor, QCursor

import serial.tools.list_ports
from serial import SerialException

import Arduino    #Program created to connect / read... with the arduino microcontrol

import Pump_seringe    #Program to control the pump

import MotorPI    #Program to control the axial motor 






##############################################################################################################
##############################################################################################################
##############################################################################################################


def read():
    """This method is used to take the information given by the arduino in atributes of the class
    String code => "(secu,ori,load,pressure)"
    """
    try:
        char = Arduino.read_ino()
    except:
        print("Problem with arduino's sent values !")
    if char[0] == "(" and char[-1] == ")":   #Check the letter before value (to not take into account the partial value)
        data = char[1:-1].split(",")   #[secu,ori,load,pressure]
        data[0] = int(data[0])
        data[1] = int(data[1])
        data[2] = float(data[2])
        data[3] = float(data[3])
    else:
        raise Exception("Incorrect value")
    return data



##############################################################################################################
##############################################################################################################
##############################################################################################################



class IniWindow(QMainWindow):    #QDefinition of the graphical interface (GI) class

    switch_window = QtCore.pyqtSignal(str)
    
    
    def __init__(self):   #Initiation: It's in there that we create all the widgets needed in our window
        
        
        QMainWindow.__init__(self)
 
        #self.setMinimumSize(QSize(1000, 500))    
        self.setWindowTitle("Initialisation")     # set window title
        self.setMinimumSize(400, 200);
        self.setStyleSheet("background-color: gray;")   #Background color
        
        centralWidget = QWidget()    # Create a central Widgets (It's a big widget that contains all others and the we will assign to the window)
        centralLayout = QHBoxLayout()    # Create a Layout for the central Widget
        
        
        #Put window in center
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())


#######################################################
        #Create all labels
#######################################################
       
        #Create label
        self.label = QLabel()
        self.label.setText("Waiting")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial",20,QFont.Bold))
        
#######################################################
        #Set the Timer 
#######################################################
        
        

        
        self.timer_ini = QtCore.QTimer()    #Set the timer
        self.timer_ini.timeout.connect(self.update_ini)   #Each time the timer clock, this method is called




        QMessageBox.about(self, "Directory:", "Choose your directory folder")
        self.path = str(QFileDialog.getExistingDirectory(self, "Select your main directory")) #Choose a path
        
        
        self.progress = QProgressBar(self)
        self.progress.setGeometry(200, 80, 250, 20)


        self.ini_start = False
        self.btn = QPushButton("Start initialisation",self)
        self.btn.clicked.connect(self.Ini_process)
        
        self.btn2 = QPushButton("Pass the initialisation",self)
        self.btn2.clicked.connect(self.Pass)
        
        
        
#######################################################
        #Def menubar
#######################################################
        
        menuBar = self.menuBar()   #Creation of the menubar


#############
        #Def port definition
        fileMenu = menuBar.addMenu('&File')

        changeFileAction = QAction('&Change working directory', self)        
        changeFileAction.setStatusTip('Change working directory')
        changeFileAction.triggered.connect(self.ChangeDir)    #Call the fonction when this action is selected
        fileMenu.addAction(changeFileAction)    #Put the new action in the item
        


#############
        #Def port definition
        portMenu = menuBar.addMenu('&Serial Ports')

        ShowPortAction = QAction('&Show Serial Ports', self)        
        ShowPortAction.setStatusTip('Show Serial Ports')
        ShowPortAction.triggered.connect(self.ShowPortCall)    #Call the fonction when this action is selected
        portMenu.addAction(ShowPortAction)    #Put the new action in the item

        chooseMenu = portMenu.addMenu('&Choose Serial Port')
        # Create new action (for menubar)
        InoPortAction = QAction('&Arduino', self)        
        InoPortAction.setStatusTip('Define the serial port of the arduino')
        InoPortAction.triggered.connect(self.InoPortCall)    #Call the fonction when this action is selected
        chooseMenu.addAction(InoPortAction)    #Put the new action in the item
        
        
        MotorPortAction = QAction('&PI Motor', self)        
        MotorPortAction.setStatusTip('Define the serial port of the Motor')
        MotorPortAction.triggered.connect(self.MotorPortCall)    #Call the fonction when this action is selected
        chooseMenu.addAction(MotorPortAction)    #Put the new action in the item
        
        
        PumpPortAction = QAction('&Watson-Marlow Pump', self)        
        PumpPortAction.setStatusTip('Define the serial ports of the PI motor')
        PumpPortAction.triggered.connect(self.PumpPortCall)    #Call the fonction when this action is selected
        chooseMenu.addAction(PumpPortAction)    #Put the new action in the item
        
        
#######################################################
        # Creation of the different composent of the window (Layout !!)
#######################################################
        
        
        final_layout = QVBoxLayout()
        final_layout.addWidget(self.label)
        
        final_layout.addSpacing (20)
        final_layout.addStretch(1)
        final_layout.addWidget(self.btn2)
        
        final_layout.addSpacing (20)
        final_layout.addStretch(1)
        final_layout.addWidget(self.btn)
        
        final_layout.addSpacing (20)
        final_layout.addStretch(1)
        final_layout.addWidget(self.progress)
        final_layout.addSpacing (20)
        final_layout.addStretch() 



        centralLayout.addLayout(final_layout)    #Add the layout to the central widget
        # Set the Layout
        centralWidget.setLayout(centralLayout)

        # Set the Widget
        self.setCentralWidget(centralWidget)     
        
        
        self.show



#######################################################
        # Def functions
#######################################################

    def ChangeDir(self):
        """Function to change directory"""
        
        
        self.path = str(QFileDialog.getExistingDirectory(self, "Select Directory")) #Choose a path
        print(self.path)
        
    def Pass(self):
        """Function to change directory"""
        
        #######################################################
        ## CONNECTION WITH ARDUINO/PUMP/MOTOR
        
        try:
            Arduino.findport()
        except:
            print("arduino findport problem")
        try:
            Pump_seringe.findport()
        except:
            print("pump findport problem")
        try:
            MotorPI.findport()
        except:
            print("motor findport problem")
        
        
        msg = ""
        try:
            Arduino.connect()
        except:
            print("Can't connect to arduino")
        if Arduino.isconnected():
            msg += "Arduino: Connected\n"
        else:
            msg += "Arduino: Not connected\n"
            
        try:
            Pump_seringe.connect()
        except:
            print("Can't connect to pump")
        if Pump_seringe.isconnected():
            msg += "Pump: Connected\n"
        else:
            msg += "Pump: Not connected\n"
        
        try:
            MotorPI.connect()
            MotorPI.ref()
        except:
            print("Can't connect to motor")
        if MotorPI.isconnected():
            msg += "Motor: Connected\n"
        else:
            msg += "Motor: Not connected\n"
            
        
        
        msg = QMessageBox.question(self,"Continue ?",msg+"\n\nDo you want to continue ?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if msg == QMessageBox.No:
            return
        
        QMessageBox.about(self, "Acquisition", "Initialisation finished\n\nStart of the acquisition")

        self.switch_window.emit(self.path)
        
        self.close()
        

    def ShowPortCall(self):
        """Function to show in a window the different ports open"""
        ports = ""
        
        
        if Arduino.ino.port is None:
            Arduino.ino.port = "Not Define"
        ports = ports +"Arduino:   " + Arduino.ino.port + "\n"
        
        if MotorPI.port is None:
            MotorPI.port = "Not Define"
        ports = ports +"PI Motor:   " + MotorPI.port + "\n"
        
        if Pump_seringe.ser.port is None:
            Pump_seringe.ser.port = "Not Define"
        ports = ports + "Pump:   " + Pump_seringe.ser.port + "\n"
        
        QMessageBox.about(self, "Serial ports:", ports)

    def PumpPortCall(self):
        """Function to change the ports of the Pump"""
        ports = []
        for i in serial.tools.list_ports.comports():
            print(i)
            ports.append(str(i).split()[0])
        items = (ports)
        item, ok = QInputDialog.getItem(self, "Serial ports","Which serial port pump connected:", items, 0, False)
        
        if ok:
            Pump_seringe.ser.port = item
            
            
    def InoPortCall(self):
        """Function to change the ports of the Arduino"""
        ports = []
        for i in serial.tools.list_ports.comports():
            ports.append(str(i).split()[0])
            
        items = (ports)
        item, ok = QInputDialog.getItem(self, "Serial ports","Which serial port Arduino connected:", items, 0, False)
        
        if ok:
            Arduino.ino.port = item
            
    def MotorPortCall(self):
        """Function to change the ports of the Motor"""
        ports = []
        for i in serial.tools.list_ports.comports():
            ports.append(str(i).split()[0])
            
        items = (ports)
        item, ok = QInputDialog.getItem(self, "Serial ports","Which serial port Arduino connected:", items, 0, False)
        
        if ok:
            MotorPI.port = item

####################



    def Ini_process(self):
        """Function that initialise: start the motor to find upper and lower boundaries"""
        
        #Button check not more than one time
        if self.ini_start:
            return
        self.ini_start = True
        
        #Define the progress bar
        self.completed = 0
        
        
        
        #######################################################
        # Define the connections with devices
        
        self.label.setText("Connecting...")
        self.repaint()
        time.sleep(1)
        #######################################################
        ## CONNECTION WITH ARDUINO/PUMP/MOTOR
        
        try:
            Arduino.findport()
        except:
            print("arduino findport problem")
        try:
            Pump_seringe.findport()
        except:
            print("pump findport problem")
        try:
            MotorPI.findport()
        except:
            print("motor findport problem")
        
        
        msg = ""
        try:
            Arduino.connect()
        except:
            print("Can't connect to arduino")
        if Arduino.isconnected():
            msg += "Arduino: Connected\n"
        else:
            msg += "Arduino: Not connected\n"
            
        try:
            Pump_seringe.connect()
        except:
            print("Can't connect to pump")
        if Pump_seringe.isconnected():
            msg += "Pump: Connected\n"
        else:
            msg += "Pump: Not connected\n"
        
        try:
            MotorPI.connect()
            MotorPI.ref()
        except:
            print("Can't connect to motor")
        if MotorPI.isconnected():
            msg += "Motor: Connected\n"
        else:
            msg += "Motor: Not connected\n"
            
        
        
        QMessageBox.about(self, "Connections", msg)
        if Arduino.isconnected() == False or MotorPI.isconnected() == False or Pump_seringe.isconnected() == False :
            print('Connection problem')
            self.ini_start = False
            self.label.setText("Waiting")
            return
        
        
        
        secu = 0
        test = 0
        while test == 0:
            try:
                [secu,ori,F,P] =read()
                test = 1
            except:
                print("read step1 problem")
        
        if secu==1:
            QMessageBox.about(self, "Problem", "Security button activated !")
            self.completed = 0
            self.ini_start = False
            self.timer_ini.stop()
            return
        
        
        
        
        msg = QMessageBox.question(self,"Continue ?","Do you want to start the initialisation ?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if msg == QMessageBox.No:
            self.ini_start = False
            return
        
        self.timer_ini.start(100)
        
        
        #######################################################
        #######################################################
        #------------------
        ## ASK MOTOR SPEED
        #text, okPressed = QInputDialog.getText(self, "Motor velocity","Velocity (deg / s) : ", QLineEdit.Normal, "")
        #MotorPI.vel(text)
        
#        MotorPI.ref()
        #######################################################
        ## SEARCH FOR BOUNDARIES
        
        self.completed = 0
        self.progress.setValue(self.completed)
        self.label.setText("Searching for origin")
        self.repaint()
        #First boundary
        
        MotorPI.vel(75)

        
        MotorPI.ref()
        try:
            MotorPI.move_rel(50)
        except:
            QMessageBox.about(self, "Problem", "Retry please")
            self.ini_start = False
            self.timer_ini.stop()
            return
        
        
        while ori == 0:
            if self.completed >= 100:
                self.completed = 0
                self.progress.setValue(self.completed)
                time.sleep(0.1)
                try:
                    [secu,ori,F,P] =read()
                except:
                    print("read step1 problem")
            self.completed = self.completed + 20
            self.progress.setValue(self.completed)
            time.sleep(0.5)
            try:
                [secu,ori,F,P] =read()
            except:
                print("read step1 problem")
            if secu==1:
                QMessageBox.about(self, "Problem", "Security button activated !")
                self.completed = 0
                self.ini_start = False
                self.timer_ini.stop()
                return
        
            
        try:
            MotorPI.stop()
        except:
            print("motor stop")
        
        MotorPI.ref()
        
        self.completed = 100
        self.progress.setValue(self.completed)
#        QMessageBox.about(self, "Origin", "The origin was found successfully")
        
        time.sleep(1)
        
        self.completed = 0
        self.progress.setValue(self.completed)
        self.label.setText("Returning mid")
        self.repaint()
        
        #Return
        L_return = -50
        
        MotorPI.move_rel(L_return)
        
        deg = 360 * abs(L_return) / MotorPI.p
        t = deg/MotorPI.vel_value()
        
        debut = time.time()
        limit = t/99
        while MotorPI.ismoving():
            if time.time() - debut > limit:
                self.completed = self.completed + 1
                self.progress.setValue(self.completed)
                limit = limit + t/99
            try:
                [secu,ori,F,P] =read()
            except:
                print("read step1 problem")
            if secu == 1:
                QMessageBox.about(self, "Problem", "Security button activated !")
                self.ini_start = False
                self.timer_ini.stop()
                return
        
        
        
        self.completed = 100
        self.progress.setValue(self.completed)
        self.label.setText("Finish")
        
        MotorPI.vel(20)
        
        self.timer_ini.stop()
        

        QMessageBox.about(self, "Acquisition", "Initialisation finished\n\nStart of the acquisition")
        
        self.switch_window.emit(self.path)
        
        self.close()
        
        
        
    def update_ini(self):
        """Method called each time the timer clocks"""
        try:
            [secu,ori,F,P] = read()    #Method to save current value of load and pressure
        except:
            print("read step1 problem")
        
        
        
##############################################################################################################
##############################################################################################################
##############################################################################################################


def ini():
    
    
    def myExitHandler():
        """Function that run when the window is stopped"""
        try:
            MotorPI.stop()
        except:
            pass
        if mainWin.timer_ini.isActive():
            mainWin.timer_ini.stop()    #Stop the timer
            print("Timer stopped")
            
#######################################################
    #Set my window
#######################################################
    
    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(myExitHandler) # myExitHandler is a callable

    
#######################################################
    #Create the window object
#######################################################
    
    mainWin = IniWindow()
    mainWin.show()
    
    try:    #Catch the exceptions
        sys.exit( app.exec_() )
    except SystemExit:
        print("Window closed !")

    
    return mainWin.path, mainWin.disp
    
    
    
    
if __name__ == '__main__':
    
    print("ok")
   #ini()
    
    
    
