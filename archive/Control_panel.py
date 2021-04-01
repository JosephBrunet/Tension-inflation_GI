#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 10:13:14 2018

@author: root
"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton, QAction, QStatusBar, QFormLayout, QLabel, QLineEdit, 
    QVBoxLayout, QHBoxLayout, QSpacerItem, QMessageBox, QFrame, QSizePolicy, QInputDialog, QGroupBox, QRadioButton, QButtonGroup, QGridLayout)
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QFont, QDoubleValidator, QPixmap, QPalette, QColor, QCursor

import MotorPI
import Arduino    #Program created to connect / read... with the arduino microcontrol

import serial
from serial import SerialException
import serial.tools.list_ports


#
class Control_panel(object):
    def setup_control_panel(self, parent=None):
        
        
        

        self.button_positioning = QPushButton('Positioning finished', self)
        self.button_positioning.clicked.connect(self.clickMethod_positioning)
        self.button_positioning.setStatusTip('Tare the pressure sensor')
        self.button_positioning.setIconSize(QSize(100,100))
        self.button_positioning.setMaximumSize(250,200)    #Set the minimum size of the button
        self.button_positioning.setFont(QFont("Arial",16,QFont.Bold))
        
        # Add button for taring load
        tarebutton_load = QPushButton('Tare', self)
        tarebutton_load.clicked.connect(self.clickMethodTare_load)
        tarebutton_load.setStatusTip('Tare the load sensor')
        tarebutton_load.setIconSize(QSize(100,100))
        tarebutton_load.setMaximumSize(100,200)    #Set the minimum size of the button

        tarebutton_pressure = QPushButton('Tare', self)
        tarebutton_pressure.clicked.connect(self.clickMethodTare_pressure)
        tarebutton_pressure.setStatusTip('Tare the pressure sensor')
        tarebutton_pressure.setIconSize(QSize(100,100))
        tarebutton_pressure.setMaximumSize(100,200)    #Set the minimum size of the button
        
        tarebutton_volume = QPushButton('Tare', self)
        tarebutton_volume.clicked.connect(self.clickMethodTare_vol)
        tarebutton_volume.setStatusTip('Tare the pressure sensor')
        tarebutton_volume.setIconSize(QSize(100,100))
        tarebutton_volume.setMaximumSize(100,200)    #Set the minimum size of the button

        tarebutton_disp = QPushButton('Tare', self)
        tarebutton_disp.clicked.connect(self.clickMethodTare_disp)
        tarebutton_disp.setStatusTip('Tare the pressure sensor')
        tarebutton_disp.setIconSize(QSize(100,100))
        tarebutton_disp.setMaximumSize(100,200)    #Set the minimum size of the button
        
        
        
        self.button_vol_more = QPushButton('+', self)
        self.button_vol_more.clicked.connect(self.clickMethod_volMore)
        self.button_vol_more.setStatusTip('Tare the pressure sensor')
        self.button_vol_more.setIconSize(QSize(100,100))
        self.button_vol_more.setMaximumSize(100,200)    #Set the minimum size of the button
        
        self.button_vol_less = QPushButton('-', self)
        self.button_vol_less.clicked.connect(self.clickMethod_volLess)
        self.button_vol_less.setStatusTip('Tare the pressure sensor')
        self.button_vol_less.setIconSize(QSize(100,100))
        self.button_vol_less.setMaximumSize(100,200)    #Set the minimum size of the button
        
        self.button_disp_more = QPushButton('+', self)
        self.button_disp_more.clicked.connect(self.clickMethod_dispMore)
        self.button_disp_more.setStatusTip('Tare the pressure sensor')
        self.button_disp_more.setIconSize(QSize(100,100))
        self.button_disp_more.setMaximumSize(100,200)    #Set the minimum size of the button
        
        self.button_disp_less = QPushButton('-', self)
        self.button_disp_less.clicked.connect(self.clickMethod_dispMore)
        self.button_disp_less.setStatusTip('Tare the pressure sensor')
        self.button_disp_less.setIconSize(QSize(100,100))
        self.button_disp_less.setMaximumSize(100,200)    #Set the minimum size of the button
        

        
        
        #Radio button
        #Add a radio button  step vol
        
        group_vol = QButtonGroup(self.centralWidget)
        
        self.step_vol = 0.01
        self.Radio_step_vol001 = QRadioButton("0.01")
        group_vol.addButton(self.Radio_step_vol001)

        self.Radio_step_vol001.setChecked(True)
        self.Radio_step_vol001.clicked.connect(lambda:self.radio_vol_step(self.Radio_step_vol001))
        
        self.Radio_step_vol01 = QRadioButton("0.1")
        group_vol.addButton(self.Radio_step_vol01)

        self.Radio_step_vol01.clicked.connect(lambda:self.radio_vol_step(self.Radio_step_vol01))
        

        self.Radio_step_vol1 = QRadioButton("1")
        group_vol.addButton(self.Radio_step_vol1)

        self.Radio_step_vol1.clicked.connect(lambda:self.radio_vol_step(self.Radio_step_vol1))

        #Add a radio button  step disp
        group_disp = QButtonGroup(self.centralWidget)

        self.step_disp = 0.1
        self.Radio_step_disp01 = QRadioButton("0.1")
        self.Radio_step_disp01.setChecked(True)
        self.Radio_step_disp01.clicked.connect(lambda:self.radio_disp_step(self.Radio_step_disp01))
        group_disp.addButton(self.Radio_step_disp01)
        
        self.Radio_step_disp05 = QRadioButton("0.5")
        self.Radio_step_disp05.clicked.connect(lambda:self.radio_disp_step(self.Radio_step_disp05))
        group_disp.addButton(self.Radio_step_disp05)

        self.Radio_step_disp1 = QRadioButton("1")
        self.Radio_step_disp1.clicked.connect(lambda:self.radio_disp_step(self.Radio_step_disp1))
        group_disp.addButton(self.Radio_step_disp1)



#######################################################
        # Creation labels
#######################################################


        #Create label: title 
        label_pressure_title = QLabel()
        label_pressure_title.setText("Pressure")
        label_pressure_title.setAlignment(Qt.AlignCenter)
        label_pressure_title.setFont(QFont("Arial",20,QFont.Bold))
        
        label_volume_title = QLabel()
        label_volume_title.setText("Volume")
        label_volume_title.setAlignment(Qt.AlignCenter)
        label_volume_title.setFont(QFont("Arial",20,QFont.Bold))
        
        label_load_title = QLabel()
        label_load_title.setText("Load")
        label_load_title.setAlignment(Qt.AlignCenter)
        label_load_title.setFont(QFont("Arial",20,QFont.Bold))
        
        label_disp_title = QLabel()
        label_disp_title.setText("Disp")
        label_disp_title.setAlignment(Qt.AlignCenter)
        label_disp_title.setFont(QFont("Arial",20,QFont.Bold))

        #Create label: display values
        self.label_pressure_display = QLabel()
        self.label_pressure_display.setText("Connecting")
        self.label_pressure_display.setAlignment(Qt.AlignCenter)
        self.label_pressure_display.setFont(QFont("Arial",16,))
        
        self.label_volume_display = QLabel()
        self.label_volume_display.setText("Connecting")
        self.label_volume_display.setAlignment(Qt.AlignCenter)
        self.label_volume_display.setFont(QFont("Arial",16,))
        
        self.label_load_display = QLabel()
        self.label_load_display.setText("Connecting")
        self.label_load_display.setAlignment(Qt.AlignCenter)
        self.label_load_display.setFont(QFont("Arial",16,))
        
        self.label_disp_abs_display = QLabel()
        self.label_disp_abs_display.setText("Connecting")
        self.label_disp_abs_display.setAlignment(Qt.AlignCenter)
        self.label_disp_abs_display.setFont(QFont("Arial",16,))
        
        self.label_disp_rel_display = QLabel()
        self.label_disp_rel_display.setText("Connecting")
        self.label_disp_rel_display.setAlignment(Qt.AlignCenter)
        self.label_disp_rel_display.setFont(QFont("Arial",16,))
        
        
        #Label "Step"
        label_step_vol = QLabel()
        label_step_vol.setText("Step")
        label_step_vol.setAlignment(Qt.AlignCenter)
        label_step_vol.setFont(QFont("Arial",16,))

        label_step_disp = QLabel()
        label_step_disp.setText("Step")
        label_step_disp.setAlignment(Qt.AlignCenter)
        label_step_disp.setFont(QFont("Arial",16,))
        
        
#######################################################
        # Creation of the different composent of the window (Layout !!)
#######################################################
        
        
        #Creation of a line of separation

        sepH = [QFrame() for i in range(10)]
        for obj in sepH:
            obj.setFrameShape(QFrame.HLine)    #Vertical line
            obj.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)
            obj.setFrameShadow(QFrame.Sunken);
            obj.setLineWidth(1)
            
        sepV = [QFrame() for i in range(10)]
        for obj in sepV:
            obj.setFrameShape(QFrame.VLine)    #Vertical line
            obj.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)
            obj.setFrameShadow(QFrame.Sunken);
            obj.setLineWidth(1)
            
        ##################################

        #Layout volume vertical
        box_volume_pm = QHBoxLayout()
        box_volume_pm.addWidget(self.button_vol_more)
        box_volume_pm.addWidget(self.button_vol_less)

        ###############
        box_volume_step = QHBoxLayout()
        box_volume_step.addWidget(label_step_vol)
        
        box_radio_vol = QVBoxLayout(); 
        box_radio_vol.addWidget(self.Radio_step_vol001)
        box_radio_vol.addWidget(self.Radio_step_vol01)
        box_radio_vol.addWidget(self.Radio_step_vol1)
        
        box_volume_step.addLayout(box_radio_vol)
        ###############

        #Layout disp vertical

        ###############
        box_disp_rel_abs_display = QVBoxLayout()
        box_disp_rel_abs_display.addWidget(self.label_disp_rel_display)
        box_disp_rel_abs_display.addWidget(self.label_disp_abs_display)
        ###############
        box_disp_pm = QHBoxLayout()
        box_disp_pm.addWidget(self.button_disp_more)
        box_disp_pm.addWidget(self.button_disp_less)

        ###############
        box_disp_step = QHBoxLayout()
        box_disp_step.addWidget(label_step_disp)
        
        box_radio_disp = QVBoxLayout(); 
        box_radio_disp.addWidget(self.Radio_step_disp01)
        box_radio_disp.addWidget(self.Radio_step_disp05)
        box_radio_disp.addWidget(self.Radio_step_disp1)
        
        box_disp_step.addLayout(box_radio_disp)
        ###############


        n=0
        panel_grid = QGridLayout()
        panel_grid.setSpacing(10)
        panel_grid.addWidget(label_pressure_title, 0, n)
        panel_grid.addWidget(sepH[0], 1, n)
        panel_grid.addWidget(self.label_pressure_display, 2, n)
        panel_grid.addWidget(tarebutton_pressure, 3, n, Qt.AlignCenter)
        
        panel_grid.addWidget(sepV[0], 0, 1, 10, 1)
        
        
        n=2
        panel_grid.addWidget(label_volume_title, 0, n)
        panel_grid.addWidget(sepH[1], 1, n)
        panel_grid.addWidget(self.label_volume_display, 2, n)
        panel_grid.addWidget(tarebutton_volume, 3, n, Qt.AlignCenter)
        panel_grid.addLayout(box_volume_pm, 4, n)
        panel_grid.addLayout(box_volume_step, 5, n)


        panel_grid.addWidget(sepV[1], 0, 3, 10, 1)


        n=4
        panel_grid.addWidget(label_load_title, 0, n)
        panel_grid.addWidget(sepH[2], 1, n)
        panel_grid.addWidget(self.label_load_display, 2, n)
        panel_grid.addWidget(tarebutton_load, 3, n, Qt.AlignCenter)

        
        panel_grid.addWidget(sepV[2], 0, 5, 10, 1)
        

        n=6
        panel_grid.addWidget(label_disp_title, 0, n)
        panel_grid.addWidget(sepH[3], 1, n)
        panel_grid.addLayout(box_disp_rel_abs_display, 2, n)
        panel_grid.addWidget(tarebutton_disp, 3, n, Qt.AlignCenter)

        panel_grid.addLayout(box_disp_pm, 4, n)
        panel_grid.addLayout(box_disp_step, 5, n)


        panel_layout = QVBoxLayout()
        panel_layout.addLayout(panel_grid)
        panel_layout.addWidget(self.button_positioning)
        
        
        










        self.panel_control_layout = panel_layout
        

###############################################
        #Function button
###############################################


    def clickMethod_positioning(self):
        """Method to """
        msg = QMessageBox.question(self,"End of positioning","Do you want to pass to the Test ?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if msg == QMessageBox.No:
            return

        self.inibutton.setDisabled(False)
        self.stopbutton.setDisabled(False)
        self.input_sample.setDisabled(False)
        self.Radio_volumeMode.setDisabled(False)
        self.Radio_pressureMode.setDisabled(False)
        self.Radio_dispMode.setDisabled(False)
        self.Radio_loadMode.setDisabled(False)
        self.Radio_absMode.setDisabled(False)
        self.Radio_relMode.setDisabled(False)
        self.input_load.setDisabled(False)
        self.input_pressure.setDisabled(False)
        self.button_stop.setDisabled(False)
        self.button_restart.setDisabled(False)
        self.button_cyclic.setDisabled(False)
        
        
        
        self.button_vol_more.setDisabled(True)
        self.button_vol_less.setDisabled(True)
        self.button_disp_more.setDisabled(True)
        self.button_disp_less.setDisabled(True)
        self.Radio_step_vol001.setDisabled(True)
        self.Radio_step_vol01.setDisabled(True)
        self.Radio_step_vol1.setDisabled(True)
        self.Radio_step_disp01.setDisabled(True)
        self.Radio_step_disp05.setDisabled(True)
        self.Radio_step_disp1.setDisabled(True)
        
        self.button_positioning.setDisabled(True)
        
        

    def clickMethodTare_vol(self):
        """Method to """

        reply = QMessageBox.question(self, 'To Tare or not to tare, that is the question !', 
                         'Are you sure ?', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print("yes")
            
            
                    
        else:
            print("no")
            #do something if no   
                
    def clickMethodTare_pressure(self):
        """Method to """
        
        reply = QMessageBox.question(self, 'To Tare or not to tare, that is the question !', 
                         'Are you sure ?', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                Arduino.write_ino("tP")   #Send to the arduino the command that activate the function Tare
            except SerialException:
                QMessageBox.about(self, "WARNING:", "Problem with arduino program sending !")
                    
        else:
            print("no")
            #do something if no   

    def clickMethodTare_disp(self):
        """Method to """

        reply = QMessageBox.question(self, 'To Tare or not to tare, that is the question !', 
                         'Are you sure ?', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print("yes")
            
            
            
                    
        else:
            print("no")
            #do something if no   

    def clickMethodTare_load(self):
        """Method to """
        
        reply = QMessageBox.question(self, 'To Tare or not to tare, that is the question !', 
                         'Are you sure ?', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                Arduino.write_ino("tL")   #Send to the arduino the command that activate the function Tare
            except SerialException:
                QMessageBox.about(self, "WARNING:", "Problem with arduino program sending !")
                    
        else:
            print("no")
            #do something if no   
            



    def clickMethod_volMore(self):
        """Method to """
        
        try:
            PumpWM
            self.vol = self.vol 
        except:
            QMessageBox.about(self, "WARNING:", "The motor is not connected")


    def clickMethod_volLess(self):
        """Method to """
        
        try:
            self.vol = self.vol 
        except:
            QMessageBox.about(self, "WARNING:", "The motor is not connected")

        
    def clickMethod_dispMore(self):
        """Method to """
        try:
            MotorPI.move(self.step_disp)
            self.disp = self.disp + self.step_disp
        except:
            QMessageBox.about(self, "WARNING:", "The motor is not connected")

        
    def clickMethod_dispMore(self):
        """Method to """
        
        try:
            MotorPI.move(-self.step_disp)
            self.disp = self.disp - self.step_disp
        except:
            QMessageBox.about(self, "WARNING:", "The motor is not connected")



###############################################

###############################################


    def radio_vol_step(self, radio_value):
        
        if radio_value.text() == "0.01":
            if radio_value.isChecked() == True:
                self.step_vol = 0.01
                
                
        if radio_value.text() == "0.1":
            if radio_value.isChecked() == True:
                self.step_vol = 0.1
                
        if radio_value.text() == "1":
            if radio_value.isChecked() == True:
                self.step_vol = 1
                
        print(self.step_vol)
                

    def radio_disp_step(self, radio_value):

        if radio_value.text() == "0.1":
            if radio_value.isChecked() == True:
                self.step_disp = 0.1
                
                
        if radio_value.text() == "0.5":
            if radio_value.isChecked() == True:
                self.step_disp = 0.5
                
        if radio_value.text() == "1":
            if radio_value.isChecked() == True:
                self.step_disp = 1
                
        print(self.step_disp)












#
#        #Layout Pressure vertical
#        box_pressure = QVBoxLayout()    #Creation of a vertical layout
#        box_pressure.addWidget(label_pressure_title)    #Put the widget in the layout
#        box_pressure.addWidget(sepH[0])    #Put the widget in the layout
#        box_pressure.addSpacing (20)
#        box_pressure.addStretch()   #Add a 0 space element that stretch when you stretch the window
#        ###############
#        box_pressure_display = QHBoxLayout()
#        box_pressure_display.addWidget(self.label_pressure_display)
#        box_pressure_display.addWidget(tarebutton_pressure)
#        ###############
##        box_pressure.addLayout(box_pressure_display)
##        box_pressure.addSpacing (20)
##        box_pressure.addStretch()
#        
#
#
#        #Layout volume vertical
#        box_volume = QVBoxLayout()    #Creation of a vertical layout
#        box_volume.addWidget(label_volume_title)    #Put the widget in the layout
#        box_volume.addWidget(sepH[1])    #Put the widget in the layout
#        box_volume.addSpacing (20)
#        box_volume.addStretch()   #Add a 0 space element that stretch when you stretch the window
#        ###############
#        box_volume_display = QHBoxLayout()
#        box_volume_display.addWidget(self.label_volume_display)
#        box_volume_display.addWidget(tarebutton_volume)
#        ###############
##        box_volume.addLayout(box_volume_display)
#        box_volume.addSpacing (20)
#        box_volume.addStretch()
#        ###############
#        box_volume_pm = QHBoxLayout()
#        box_volume_pm.addWidget(button_vol_more)
#        box_volume_pm.addWidget(button_vol_less)
#        ###############
##        box_volume.addLayout(box_volume_pm)
#        box_volume.addSpacing (20)
#        box_volume.addStretch()
#        ###############
#        box_volume_step = QHBoxLayout()
#        box_volume_step.addWidget(label_step_vol)
#        
#        box_radio_vol = QVBoxLayout(); 
#        box_radio_vol.addWidget(self.Radio_step_vol001)
#        box_radio_vol.addWidget(self.Radio_step_vol01)
#        box_radio_vol.addWidget(self.Radio_step_vol1)
#        
#        box_volume_step.addLayout(box_radio_vol)
#        ###############
##        box_volume.addLayout(box_volume_step)
#        box_volume.addSpacing (20)
#        box_volume.addStretch()
#        
#
#
#
#        test = QGridLayout()
#        test.setSpacing(10)
#        test.addWidget(label_pressure_title, 0, 0)
#        test.addWidget(sepH[0], 1, 0)
#        test.addLayout(box_pressure_display, 2, 0)
#        
#        test.addWidget(sepV[5], 0, 1, 10, 1)
#        
#        test.addWidget(label_volume_title, 0, 2)
#        test.addWidget(sepH[1], 1, 2)
#        test.addLayout(box_volume_display, 2, 2)
#        test.addLayout(box_volume_pm, 3, 2)
#        test.addLayout(box_volume_step, 4, 2)
#
#
#
#
#        #Layout Load vertical
#        box_load = QVBoxLayout()
#        #box_pressure.addStretch()
#        box_load.addWidget(label_load_title)
#        box_load.addWidget(sepH[2])    #Put the widget in the layout
#        box_load.addSpacing (20)
#        box_load.addStretch()
#
#        ###############
#        box_load_display = QHBoxLayout()
#        box_load_display.addWidget(self.label_load_display)
#        box_load_display.addWidget(tarebutton_load)
#        ###############
#        
#        box_load.addLayout(box_load_display)
#        box_load.addSpacing (20)
#        box_load.addStretch()
##        box_load.addLayout(box_load_input)
#        
#        
#
#        #Layout disp vertical
#        box_disp = QVBoxLayout()    #Creation of a vertical layout
#        box_disp.addWidget(label_disp_title)    #Put the widget in the layout
#        box_disp.addWidget(sepH[3])    #Put the widget in the layout
#        box_disp.addSpacing (20)
#        box_disp.addStretch()   #Add a 0 space element that stretch when you stretch the window
#        ###############
#        box_disp_rel_abs_display = QVBoxLayout()
#        box_disp_rel_abs_display.addWidget(self.label_disp_rel_display)
#        box_disp_rel_abs_display.addWidget(self.label_disp_abs_display)
#        box_disp_display = QHBoxLayout()
#        box_disp_display.addLayout(box_disp_rel_abs_display)
#        box_disp_display.addWidget(tarebutton_disp)
#        ###############
#        box_disp.addLayout(box_disp_display)
#        box_disp.addSpacing (20)
#        box_disp.addStretch()
#        ###############
#        box_disp_pm = QHBoxLayout()
#        box_disp_pm.addWidget(button_disp_more)
#        box_disp_pm.addWidget(button_disp_less)
#        ###############
#        box_disp.addLayout(box_disp_pm)
#        box_disp.addSpacing (20)
#        box_disp.addStretch()
#        ###############
#        box_disp_step = QHBoxLayout()
#        box_disp_step.addWidget(label_step_disp)
#        
#        box_radio_disp = QVBoxLayout(); 
#        box_radio_disp.addWidget(self.Radio_step_disp01)
#        box_radio_disp.addWidget(self.Radio_step_disp05)
#        box_radio_disp.addWidget(self.Radio_step_disp1)
#        
#        box_disp_step.addLayout(box_radio_disp)
#        ###############
#        box_disp.addLayout(box_disp_step)
#        box_disp.addSpacing (20)
#        box_disp.addStretch()
#
#################################################
#        # Layout : Disposition of the different elements in the window
########################################################
#
#        #Put the panels (pressure / volume / load / disp) 
#        self.panel_layout = QHBoxLayout()
#        self.panel_layout.addStretch(1)
#        self.panel_layout.addLayout(box_pressure)
#        self.panel_layout.addSpacing (15)
#        self.panel_layout.addStretch(1)
#        self.panel_layout.addWidget(sepV[4])
#        self.panel_layout.addSpacing (15)
#        self.panel_layout.addStretch(1)
#        self.panel_layout.addLayout(box_volume)
#        self.panel_layout.addSpacing (15)
#        self.panel_layout.addStretch(1)
#        self.panel_layout.addWidget(sepV[5])
#        self.panel_layout.addSpacing (15)
#        self.panel_layout.addStretch(1)
#        self.panel_layout.addLayout(box_load)
#        self.panel_layout.addSpacing (15)
#        self.panel_layout.addStretch(1)
#        self.panel_layout.addWidget(sepV[6])
#        self.panel_layout.addSpacing (15)
#        self.panel_layout.addStretch(1)
#        self.panel_layout.addLayout(box_disp)
#        self.panel_layout.addStretch(1)
#
#        self.panel_layout = test




