# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 13:52:53 2018

@author: joseph.brunet
"""


import os
import os.path
os.chdir('/home/local/EMSE2000/joseph.brunet/Documents/PhD/Experiments/System_tomo/Code test')

import sys
import time

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton, QAction, QStatusBar, QFormLayout, QLabel, QLineEdit, 
    QVBoxLayout, QHBoxLayout, QSpacerItem, QMessageBox, QFrame, QSizePolicy, QInputDialog, QGroupBox, QRadioButton, QFileDialog)
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QFont, QDoubleValidator, QPixmap, QPalette, QColor, QCursor

import serial.tools.list_ports
from serial import SerialException

import Arduino    #Program created to connect / read... with the arduino microcontrol

import PumpWM    #Program to control the pump

import MotorPI    #Program to control the axial motor 


from Control_panel import Control_panel
from Test_panel import Test_panel



import _thread
from threading import Thread    #To create program that run in parallel

import numpy as np    #For mathematics
import pyqtgraph as pg    #Library to plot graph with pyqt


class Thread_ino(Thread):     #Class that read the arduino's information

    """Thread that connect to the arduino and read the information send by the port."""

    def __init__(self):     #Special method: initialisation / attributes creation
        Thread.__init__(self)
        self.load = ""   #Initialisation of variables
        self.pressure = ""
        
        try:
            Arduino.connect(Arduino.ino)    #Function for openning the port (argument is the port name and baudrate define in Arduino)
        except:
            print("Problem with Arduino connection")

    def run(self):
        """Code to execute during the thread execution, start connection following by a loop that read th arduino"""
        
        try:    #Read the values send by the arduino and catch the errors
            Arduino.read_ino()    #Function to read the information send by arduino, loop that stop only when the method stop() is execute
        except:
            sys.exit("Problem with arduino's program !")
            
            
    def stop(self):
        """Code to execute when you want to finish the thread, this stop the reading"""
        Arduino.read_ino.stop = 1    #This varable stop the reading loop when set to 1
        Arduino.disconnect(Arduino.ino)

    def measure(self):
        """This method is used to take the information given by the arduino in atributes of the class"""
        if Arduino.read_ino.data_ino[0:1] == "V" and Arduino.read_ino.data_ino[19:20] == "L":   #Check the letter before value (to not take into account the partial value)
            try:
                self.load = Arduino.read_ino.data_ino[-7:-1]
                self.pressure = Arduino.read_ino.data_ino[9:15]
            except:
                print("Problem with arduino's sent values !")
                #sys.exit("Problem with arduino's sent values !")
                
            
 

##############################################################################################################
##############################################################################################################
##############################################################################################################


class MainWindow(QMainWindow, Control_panel, Test_panel):    #Definition of the graphical interface (GI) class

    def __init__(self, path, disp, vol):   #Initiation: It's in there that we create all the widgets needed in our window
        
        super(MainWindow, self).__init__()
        
        self.path = path
        self.disp = disp
        self.vol = vol
        
        QMainWindow.__init__(self)
        
        
        #self.setMinimumSize(QSize(1000, 500))    
        self.setWindowTitle("Command Panel")     # set window title
        #self.setMinimumSize(800, 800);
        self.setStyleSheet("background-color: gray;")   #Background color
        
        self.centralWidget = QWidget()    # Create a central Widgets (It's a big widget that contains all others and the we will assign to the window)
        centralLayout = QHBoxLayout()    # Create a Layout for the central Widget
        
        
        self.setup_control_panel(self)
        self.setup_test_panel(self)
        
        
        self.inibutton.setDisabled(True)
        self.stopbutton.setDisabled(True)
        self.input_sample.setDisabled(True)
        self.Radio_volumeMode.setDisabled(True)
        self.Radio_pressureMode.setDisabled(True)
        self.Radio_dispMode.setDisabled(True)
        self.Radio_loadMode.setDisabled(True)
        self.Radio_absMode.setDisabled(True)
        self.Radio_relMode.setDisabled(True)
        self.input_load.setDisabled(True)
        self.input_pressure.setDisabled(True)
        self.button_stop.setDisabled(True)
        self.button_restart.setDisabled(True)
        self.button_cyclic.setDisabled(True)
        
#######################################################
        #Create all the widgets
        
        self.statusBar = QStatusBar()        #Create object statusbar
        self.setStatusBar(self.statusBar)      #Activate statue bar

########################################
        '''
        INFORMATION
        
        "self.something" means that "something" is an atribute of the class
        if you don't put it "something" will only be local)
        '''

#######################################################
        #Set the Timer and Thread
#######################################################
        
        self.running = False
        self.pump_run = False
        
        #Start thread and timer for positioning
        
        self.thread_1 = Thread_ino()     #Creation of the object
        self.thread_1.start()     #Start of the thread
        print('Start thread')
        
        self.timer = QtCore.QTimer()    #Set the timer
        self.timer.timeout.connect(self.update_label)
        self.timer.start(50)    #Start the timer with clocking of 50 ms

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
        
#############
        #Def pump
        pump_menu = menuBar.addMenu("&Pump")

        vel_p_action = QAction(QIcon('new.png'),"&Change Flow velocity", self)
        vel_p_action.setStatusTip('Change flow velocity')  # Hungry!
        vel_p_action.triggered.connect(self.VelPumpCall)
        pump_menu.addAction(vel_p_action)
        
        
        doc_action = QAction(QIcon('new.png'),"&Help Pump Commands", self)
        doc_action.setStatusTip('Help Pump')  # Hungry!
        doc_action.triggered.connect(self.helpPumpCall)
        pump_menu.addAction(doc_action)

#############
        #Def motor
        motor_menu = menuBar.addMenu("&Motor")

        vel_m_action = QAction(QIcon('new.png'),"&Change Motor speed", self)
        vel_m_action.setStatusTip('Change motor speed')  # Hungry!
        vel_m_action.triggered.connect(self.VelMotorCall)
        motor_menu.addAction(vel_m_action)

#############
        #Def help
        help_menu = menuBar.addMenu("&Help")


        about_action = QAction(QIcon('new.png'),"&Only when u\'re desesperate", self)
        about_action.setStatusTip('Only when u\'re desesperate')  # Hungry!
        about_action.triggered.connect(self.helpCall)
        help_menu.addAction(about_action)
        


#######################################################
       #Def of separation lines 
#######################################################
       
        sepGUIH = [QFrame() for i in range(5)]
        for obj in sepGUIH:
            obj.setFrameShape(QFrame.HLine)    #Vertical line
            obj.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)
            obj.setFrameShadow(QFrame.Sunken);
            obj.setLineWidth(1)
            
        sepGUIV = [QFrame() for i in range(5)]
        for obj in sepGUIV:
            obj.setFrameShape(QFrame.VLine)    #Vertical line
            obj.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)
            obj.setFrameShadow(QFrame.Sunken);
            obj.setLineWidth(1)

        
################################################
        # Layout : Disposition of the different elements in the window
#######################################################

        test = QVBoxLayout()
        test.addLayout(self.panel_control_layout)
        test.addStretch()


        #Put all the layout together
        final_layout = QVBoxLayout()
        final_layout.addWidget(sepGUIH[0])
#        final_layout.addLayout(box_command)
        final_layout.addWidget(sepGUIH[1])
        final_layout.addSpacing (20)
        final_layout.addStretch(1)
        ##########################
        final_layoutH = QHBoxLayout()
        final_layoutH.addSpacing (20)
        final_layoutH.addStretch(1)
        final_layoutH.addLayout(test)
        final_layoutH.addSpacing (20)
        final_layoutH.addStretch(1)
        final_layoutH.addWidget(sepGUIV[0])
        final_layoutH.addWidget(sepGUIV[1])
        final_layoutH.addSpacing (20)
        final_layoutH.addStretch(1)
        final_layoutH.addLayout(self.panel_test_layout)
        final_layoutH.addSpacing (20)
        final_layoutH.addStretch(1)
        ##########################
        final_layout.addLayout(final_layoutH)
        final_layout.addSpacing (20)
        final_layout.addStretch(1)




        centralLayout.addLayout(final_layout)    #Add the layout to the central widget
        # Set the Layout
        self.centralWidget.setLayout(centralLayout)

        # Set the Widget
        self.setCentralWidget(self.centralWidget)     
        
        self.show


        print("End of initiation !")




#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------

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
        
    def helpCall(self):
        QMessageBox.about(self, "Tip", "Call me if you have questions :\nJoseph Brunet\njoseph.brunet@emse.fr")

    def helpPumpCall(self):
        """Show the pump doc"""
        QMessageBox.about(self, "Pump doc", PumpWM.doc)
        
        
    def VelPumpCall(self):
        """Change the pump flow rate"""
        text, okPressed = QInputDialog.getText(self, "Set flow rate","Flow Rate (mL/min) :", QLineEdit.Normal, "")
        if okPressed and text != '':
            try:
                PumpWM.setFlowRate(text)
            except SerialException:
                QMessageBox.about(self, "WARNING:", "The pump is not connected\n(check the serial ports)")
            
    def VelMotorCall(self):
        """Change the motor rotation speed"""
        text, okPressed = QInputDialog.getText(self, "Set motor speed","Motor speed (deg/s) :", QLineEdit.Normal, "")
        if okPressed and text != '':
            try:
                MotorPI.vel(float(text))
            except:
                QMessageBox.about(self, "WARNING:", "The motor is not connected")

            
###################################
###################################
        



###################################
###################################


    def clickMethodIni(self):
        """"Method to start the acquisition (thread and timer)"""
        
        ############
        #Test in order to know if arduino is connected
        if not Arduino.isconnected(Arduino.ino):
            QMessageBox.about(self, "WARNING:", "The arduino is not connected\n(check the serial ports)")
            return
        ############
        #Test if the programm is already runnung
        if self.running:   #Avoid problem if user push several time the start button
            print("Already running !!")
            return 
        
        
        
        ############################################################################
        ############################################################################
        
        
        #Saving file
        
        
        if self.input_sample.text():
            msg = QMessageBox.question(self,"Sample name","Sample name: '"+ self.input_sample.text() + "' ?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if msg == QMessageBox.Yes:
                self.file_save = self.input_sample.text()
                
                if not os.path.exists(self.input_sample.text() + ".txt"):
                    self.file_save = self.input_sample.text()
                    with open(self.file_save + '.txt', 'a') as mon_fichier:     #Initialize the saving file
                        mon_fichier.write(self.file_save + "\nNew run\nTime , Load , Pressure\n")
                
                else:
                    msg = QMessageBox.question(self,"WARNING: File already exist","Do you want to replace it ?",
                                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if msg == QMessageBox.Yes:
                        self.file_save = self.input_sample.text()
                        with open(self.file_save + '.txt', 'w') as mon_fichier:     #Initialize the saving file
                            mon_fichier.write(self.file_save + "\nNew run\nTime , Load , Pressure\n")
            else:
                while 1:
                    text, okPressed = QInputDialog.getText(self, "Sample name","Name :", QLineEdit.Normal, "")
                    if not okPressed:
                        return
                    if okPressed and text != '':
                        if not os.path.exists(text + ".txt"):
                            self.file_save = text
                            with open(self.file_save + '.txt', 'a') as mon_fichier:     #Initialize the saving file
                                mon_fichier.write(self.file_save + "\nNew run\nTime , Load , Pressure\n")
                            break
                        
                        else:
                            msg = QMessageBox.question(self,"WARNING: File already exist","Do you want to replace it ?",
                                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                            if msg == QMessageBox.Yes:
                                self.file_save = text
                                with open(self.file_save + '.txt', 'w') as mon_fichier:     #Initialize the saving file
                                    mon_fichier.write(self.file_save + "\nNew run\nTime , Load , Pressure\n")
                                break
                    else:
                        return
        else:
            while 1:
                text, okPressed = QInputDialog.getText(self, "Sample name","Name :", QLineEdit.Normal, "")
                if not okPressed:
                    return
                if okPressed and text != '':
                    if not os.path.exists(text + ".txt"):
                        self.file_save = text
                        with open(self.file_save + '.txt', 'a') as mon_fichier:     #Initialize the saving file
                            mon_fichier.write(self.file_save + "\nNew run\nTime , Load , Pressure\n")
                        break
                    
                    else:
                        msg = QMessageBox.question(self,"WARNING: File already exist","Do you want to replace it ?",
                                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        if msg == QMessageBox.Yes:
                            self.file_save = text
                            with open(self.file_save + '.txt', 'w') as mon_fichier:     #Initialize the saving file
                                mon_fichier.write(self.file_save + "\nNew run\nTime , Load , Pressure\n")
                            break
                else:
                    return

        ############################################################################
        ############################################################################
        
        self.running = True   # Set the variable to running
        self.grapht.clear()
        self.graphd.clear()
        self.graphv.clear()
        ############
        
        
        self.label_state.setText(" Running ")     #Show the runing state
        self.label_state.setStyleSheet("background-color: green;")    #Put the background color in green
        
        self.time_ini = time.time()     #Save the start time
        
        if self.timer.isActive():     #Check if timer active
            print("Timer already active")
        else:
            self.timer.start(50)    #Start the timer with clocking of 50 ms
            print('Timer restarted')
            
        
    def clickMethodStop(self):
        """Method to stop the acquisition"""
        
        self.running = False
        self.label_state.setText(" Stopped ")
        self.label_state.setStyleSheet("background-color: red;")
        
        
        
        
    def update_label(self):
        """Method called each time the timer clocks"""
        
        self.thread_1.measure()   #Method to save current value of load and pressure
        self.label_pressure_display.setText(self.thread_1.pressure + " mmHg")   #Display the value
        self.label_volume_display.setText(str(self.vol) + " ml")   #Display the value
        self.label_load_display.setText(self.thread_1.load + " N")   #Display the value
        self.label_disp_abs_display.setText(str(self.disp) + " mm")   #Display the value
        self.label_disp_rel_display.setText("a coder" + " mm")   #Display the value
        

        #------------------------------------------------------------------
        ## This part is activate when the user start the machanical test
        #------------------------------------------------------------------
        if not self.running:
            return

        self.time_now = time.time() - self.time_ini    #Save the timepassed since the starting time
        
        #####################
        #Graphic update
        
        if not self.time_now or self.thread_1.load or self.thread_1.pressure :       #If value are null don't show on graph (because at the beginning values null)
            xt = np.array([self.time_now])   #Create vector with the values
            xd = np.array([self.time_now])
            xv = np.array([self.time_now])
            
            y_load = np.array([float(self.thread_1.load)])
            y_pressure = np.array([float(self.thread_1.pressure)])
#            y_volume = np.array([float(self.thread_1.load)])
#            y_disp = np.array([float(self.thread_1.load)])
        
            self.grapht.plot(xt,y_load,pen=None, symbol='o')    #Show on the graph
            self.grapht.plot(xt,y_pressure,pen=None, symbol='+')    #Show on the graph
            
            self.graphd.plot(xd,y_load,pen=None, symbol='o')    #Show on the graph
            self.graphd.plot(xd,y_pressure,pen=None, symbol='+')    #Show on the graph
            
            self.graphv.plot(xv,y_load,pen=None, symbol='o')    #Show on the graph
            self.graphv.plot(xv,y_pressure,pen=None, symbol='+')    #Show on the graph
        #####################
        # Result file update
        with open(self.file_save + '.txt', 'a') as mon_fichier:
            mon_fichier.write(str(round(self.time_now,4)) + " , " + self.thread_1.load + " , " + self.thread_1.pressure + "\n")
        #####################
        # Pessure mode update
        if self.pump_run:
            if self.mode == "pressure" and self.target_pressure < float(self.thread_1.pressure) :
                    PumpWM.stop()
                    self.pump_run = False
        
        
##############################################################################################################
##############################################################################################################
##############################################################################################################

def main(path,disp,vol):
    
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
    app.aboutToQuit.connect(myExitHandler) # myExitHandler is a callable

#######################################################
    #Palette color for change window type and style
#######################################################

    app.setStyle("Fusion")

    # Fusion dark palette from https://gist.github.com/QuantumCD/6245215.
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.black)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")

#######################################################
    #Create the window object
#######################################################
    
    mainWin = MainWindow(path,disp,vol)
    mainWin.show()
    
    try:    #Catch the exceptions
        sys.exit( app.exec_() )
    except SystemExit:
        print("Window closed !")

#######################################################
#All is defined, we can start the script
#######################################################

if __name__ == '__main__':
    
   path = '/home/local/EMSE2000/joseph.brunet/Documents/PhD/Experiments/System_tomo/Code test'
   disp = 10
   vol = 1
   
   
   main(path, disp, vol)