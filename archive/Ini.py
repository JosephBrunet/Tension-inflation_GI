# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 13:52:53 2018

@author: joseph.brunet
"""



#    
#

#def rep de travail
# Faire les bornes
#enregistrer données
#Recevoir donnée de arduino
#label pour dire ce qu'il se passe 
# barre de progression
#faire revenir moteur





import os
import os.path

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

import PumpWM    #Program to control the pump

import MotorPI    #Program to control the axial motor 


import _thread
from threading import Thread    #To create program that run in parallel




##############################################################################################################
##############################################################################################################
##############################################################################################################



class Thread_ino(Thread):     #Class that read the arduino's information

    """Thread that connect to the arduino and read the information send by the port."""

    def __init__(self):     #Special method: initialisation / attributes creation
        Thread.__init__(self)

        Arduino.connect(Arduino.ino)    #Function for openning the port (argument is the port name and baudrate define in Arduino)

#        try:
#            Arduino.connect(Arduino.ino)    #Function for openning the port (argument is the port name and baudrate define in Arduino)
#        except:
#            print("Problem with Arduino connection")

    def run(self):
        """Code to execute during the thread execution, start connection following by a loop that read th arduino"""
        print('test')
#        try:    #Read the values send by the arduino and catch the errors
        Arduino.read_ino()    #Function to read the information send by arduino, loop that stop only when the method stop() is execute
#        except:
#            sys.exit("Problem with arduino's program !")
            
            
            
    def stop(self):
        """Code to execute when you want to finish the thread, this stop the reading"""
        Arduino.read_ino.stop = 1    #This varable stop the reading loop when set to 1
        Arduino.disconnect(Arduino.ino)    #Function for open the port (argument is the port name and baudrate define in Arduino)

    def read(self):
        """This method is used to take the information given by the arduino in atributes of the class"""
        if Arduino.read_ino.data_ino[0:1] == "V" and Arduino.read_ino.data_ino[9:10] == "F":   #Check the letter before value (to not take into account the partial value)
            try:
                self.b1 = Arduino.read_ino.data_ino[-7:]
                self.b2 = Arduino.read_ino.data_ino[1:8]
            except:
                sys.exit("Problem with arduino's sent values !")


##############################################################################################################
##############################################################################################################
##############################################################################################################



class IniWindow(QMainWindow):    #Definition of the graphical interface (GI) class

    def __init__(self):   #Initiation: It's in there that we create all the widgets needed in our window
        
        QMainWindow.__init__(self)
 
        #self.setMinimumSize(QSize(1000, 500))    
        self.setWindowTitle("Initialisation")     # set window title
        self.setMinimumSize(300, 200);
#        self.setStyleSheet("background-color: gray;")   #Background color
        
        centralWidget = QWidget()    # Create a central Widgets (It's a big widget that contains all others and the we will assign to the window)
        centralLayout = QHBoxLayout()    # Create a Layout for the central Widget
        
        
        #Put window in center
        fg = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        self.move(fg.topLeft())


#######################################################
        #Create all labels
#######################################################
       
        #Create label
        self.label = QLabel()
        self.label.setText("Waiting")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial",20,QFont.Bold))
        
#######################################################
        #Set the Timer and Thread
#######################################################
        
        

        
        self.timer = QtCore.QTimer()    #Set the timer
        self.timer.timeout.connect(self.update_label)   #Each time the timer clock, this method is called


        self.path = str(QFileDialog.getExistingDirectory(self, "Select yout main directory")) #Choose a path
        
        
        self.progress = QProgressBar(self)
        self.progress.setGeometry(200, 80, 250, 20)


        self.ini_start = False
        self.btn = QPushButton("Start initialisation",self)
        self.btn.clicked.connect(self.Ini_process)
        
        
        
#######################################################
        #Def menubar
#######################################################
        
        menuBar = self.menuBar()   #Creation of the menubar


#############
        #Def port definition
        fileMenu = menuBar.addMenu('&File')

        changeFileAction = QAction(QIcon('new.png'), '&Change working directory', self)        
        changeFileAction.setStatusTip('Change working directory')
        changeFileAction.triggered.connect(self.ChangeDir)    #Call the fonction when this action is selected
        fileMenu.addAction(changeFileAction)    #Put the new action in the item


#############
        #Def port definition
        portMenu = menuBar.addMenu('&Serial Ports')

        ShowPortAction = QAction(QIcon('new.png'), '&Show Serial Ports', self)        
        ShowPortAction.setStatusTip('Show Serial Ports')
        ShowPortAction.triggered.connect(self.ShowPortCall)    #Call the fonction when this action is selected
        portMenu.addAction(ShowPortAction)    #Put the new action in the item

        chooseMenu = portMenu.addMenu('&Choose Serial Port')
        # Create new action (for menubar)
        PumpPortAction = QAction(QIcon('new.png'), '&Watson-Marlow Pump', self)        
        PumpPortAction.setStatusTip('Define the serial ports of the PI motor')
        PumpPortAction.triggered.connect(self.PumpPortCall)    #Call the fonction when this action is selected
        chooseMenu.addAction(PumpPortAction)    #Put the new action in the item
        
        
        InoPortAction = QAction(QIcon('new.png'), '&Arduino', self)        
        InoPortAction.setStatusTip('Define the serial port of the arduino')
        InoPortAction.triggered.connect(self.InoPortCall)    #Call the fonction when this action is selected
        chooseMenu.addAction(InoPortAction)    #Put the new action in the item
        
        

#######################################################
        # Creation of the different composent of the window (Layout !!)
#######################################################
        
        
        final_layout = QVBoxLayout()
        final_layout.addWidget(self.label)
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

    def ShowPortCall(self):
        """Function to show in a window the different ports open"""
        ports = ""
        
        if PumpWM.pump.port is None:
            PumpWM.pump.port = "Not Define"
        ports = ports + "Pump:   " + PumpWM.pump.port + "\n"
        
        if Arduino.ino.port is None:
            Arduino.ino.port = "Not Define"
        ports = ports +"Arduino:   " + Arduino.ino.port + "\n"
        
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
            PumpWM.pump.port = item
            
            
    def InoPortCall(self):
        """Function to change the ports of the Arduino"""
        ports = []
        for i in serial.tools.list_ports.comports():
            ports.append(str(i).split()[0])
            
        items = (ports)
        item, ok = QInputDialog.getItem(self, "Serial ports","Which serial port Arduino connected:", items, 0, False)
        
        if ok:
            Arduino.ino.port = item

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
        
        self.label.setText("Connecting")
        
        ports = ""
        if PumpWM.pump.port is None:
            PumpWM.pump.port = "Not Define"
        ports+= "Pump:   " + PumpWM.pump.port + "\n"
        
        if Arduino.ino.port is None:
            Arduino.ino.port = "Not Define"
        ports+= "Arduino:   " + Arduino.ino.port
        
        QMessageBox.about(self, "Serial ports:", ports)
        
        #######################################################
        ## CONNECTION WITH ARDUINO
        
        test = False
        while not test:
            try:
                self.thread_1 = Thread_ino()    #Set the thread
                self.thread_1.start()
                self.timer.start(50)
                test = True
            except:
                QMessageBox.about(self, "WARNING:", "The arduino is not connected")
        
        #######################################################
        ## CONNECTION WITH MOTOR
        
        
        ############
        test = False
        while not test:
            try:
                MotorPI.connect()
                test = True
            except:
                QMessageBox.about(self, "WARNING:", "The motor is not connected")
                
        
        #------------------
        ## ASK MOTOR SPEED
        text, okPressed = QInputDialog.getText(self, "Motor velocity","Velocity (deg / s) : ", QLineEdit.Normal, "")

        MotorPI.vel(text)
        
#        MotorPI.ref()


        #######################################################
        ## SEARCH FOR BOUNDARIES
        
        self.completed = 30
        self.progress.setValue(self.completed)
        self.label.setText("Searching for lower boundary")
        #First boundary

        while self.b1 == False:
            
            MotorPI.move(-1)
            
        d = 0
        
        
        self.completed = 60
        self.progress.setValue(self.completed)
        self.label.setText("Searching for upper boundary")
        #Second boundary
        while self.b2 == False:
            
            MotorPI.move(1)
            d = d + 1
            
        
        self.completed = 90
        self.progress.setValue(self.completed)
        self.label.setText("Returning at standart position")
        
        #Return
        MotorPI.move(-5)
        
        MotorPI.deconnect
        
        self.completed = 100
        self.progress.setValue(self.completed)
        self.label.setText("Finish")
        
        
        
        
        
        
    def clickMethodIni(self):
        """"Method to start the acquisition (thread and timer)"""
        
        ############
        #Test in order to know if arduino is connected
        self.thread_1 = Thread_ino()     #Initialisation 
        if not Arduino.isconnected(Arduino.ino):
            QMessageBox.about(self, "WARNING:", "The arduino is not connected\n(check the serial ports)")
            return
        
        
            
        self.thread_1 = Thread_ino()     #Creation of the object
        self.thread_1.start()     #Start of the thread
        print('Start thread')
        
        self.label.setText(" Collecting arduino's data ")     #Show the runing state
        
        
        if self.timer.isActive():     #Check if timer active
            print("Timer already active")
        else:
            self.timer.start(50)    #Start the timer with clocking of 50 ms
            print('Timer restarted')
            
        
        
        
        
        
    def update_label(self):
        """Method called each time the timer clocks"""
        
        self.thread_1.read()   #Method to save current value of load and pressure
        
        
        
##############################################################################################################
##############################################################################################################
##############################################################################################################


def initialisation():
    
    
    def myExitHandler():
        """Function that run when the window is stopped"""
                
        if mainWin.thread_1.is_alive():
             mainWin.thread_1.stop()     #Stop the thread
             print("Thread stopped")
        
        if mainWin.timer.isActive():
            mainWin.timer.stop()    #Stop the timer
            print("Timer stopped")
            
#######################################################
    #Set my window
#######################################################
    
    app = QtWidgets.QApplication(sys.argv)
    
    
#######################################################
    #Create the window object
#######################################################
    
    mainWin = IniWindow()
    mainWin.show()
    
    try:    #Catch the exceptions
        sys.exit( app.exec_() )
    except SystemExit:
        print("Window closed !")
    a=1
    
    return mainWin.path, a
    
    
    
    
if __name__ == '__main__':

   
   
   initialisation()
    
    
    
