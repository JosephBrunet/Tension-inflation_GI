#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 11:14:15 2018

@author: root
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 10:13:14 2018

@author: root
"""
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton, QAction, QStatusBar, QFormLayout, QLabel, QLineEdit, 
    QVBoxLayout, QHBoxLayout, QSpacerItem, QMessageBox, QFrame, QSizePolicy, QInputDialog, QGroupBox, QRadioButton, QButtonGroup)
from PyQt5.QtCore import QSize, Qt, QRegExp
from PyQt5.QtGui import QIcon, QFont, QDoubleValidator, QPixmap, QPalette, QColor, QCursor, QRegExpValidator

import numpy as np    #For mathematics
import pyqtgraph as pg    #Library to plot graph with pyqt


#
class Test_panel(object):
    def setup_test_panel(self, parent=None):

        
        
        # Creation of the separetor object
        sepTestH = [QFrame() for i in range(7)]
        for obj in sepTestH:
            obj.setFrameShape(QFrame.HLine)    #Vertical line
            obj.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)
            obj.setFrameShadow(QFrame.Sunken);
            obj.setLineWidth(1)
            
        sepTestV = [QFrame() for i in range(7)]
        for obj in sepTestV:
            obj.setFrameShape(QFrame.VLine)    #Vertical line
            obj.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)
            obj.setFrameShadow(QFrame.Sunken);
            obj.setLineWidth(1)
            
            
            
    
    
    
    
    
    
    

        # Button for initialisation
        self.inibutton = QPushButton(self)    #Creation of the widget
        self.inibutton.clicked.connect(self.clickMethodIni)    #Method to connect the click on the button with the function clickMethodIni
        #self.inibutton.resize(100,32)
        self.inibutton.setStatusTip('Run the acquisition')    #When cursor on the button the statue bar show the message
        self.inibutton.setIcon(QIcon('image/button_start.png'))   #Change the button's icon by the image
        self.inibutton.setIconSize(QSize(30,30))   #Change the size of the icon




        # Add button for stop
        self.stopbutton = QPushButton(self)
        self.stopbutton.clicked.connect(self.clickMethodStop)
        self.stopbutton.setIcon(QIcon('image/button_stop.png'))
        #self.stopbutton.resize(100,32)
        self.stopbutton.setStatusTip('Stop the acquisition')
        self.stopbutton.setIconSize(QSize(30,30))
        #self.stopbutton.move(10, 30)        
        
        
        #Create label: running or stopped state
        self.label_state = QLabel()    #Creation of the widget
        self.label_state.setText(" Stopped ")    #Set the text in the label
        self.label_state.setAlignment(Qt.AlignCenter)   #Alignement of the label (here it's the vertical alignement)
        self.label_state.setFont(QFont("Arial",16,QFont.Bold))    #Set the writing font with the size
        self.label_state.setStyleSheet("background-color: red;")
        





        #Widget with user input for changing load
        self.input_sample = QLineEdit()   #Creation of the widget
        rx = QRegExp("[a-z-A-Z_]+")
        self.input_sample.setValidator(QRegExpValidator(rx))   #Only str accepted
        self.input_sample.setMaxLength(10)     #Number of characters accepted
        self.input_sample.setAlignment(Qt.AlignRight)
        self.input_sample.setFont(QFont("Arial",12))
        #self.input_sample.setCursor(QCursor(Qt.ArrowCursor))    #If you want a different cursor shape when on the widget
        self.input_sample.setStyleSheet("QLineEdit{background: white;}")    #Background color of the widget
        
        #hChange the writing color from write to black because we set the background write (I like when it's beautiful)
        self.input_sample.palette = QPalette()
        self.input_sample.palette.setColor(QPalette.Text, Qt.black)
        self.input_sample.setPalette(self.input_sample.palette)
        
        
        #Creation of the label attached to the QLineEdit
        label_sample_input = QLabel("Sample Name:", self)
        label_sample_input.setFont(QFont("Arial",12,QFont.Bold))
        #self.lab.setGeometry(QRect(70, 80, 300, 300)) #(x, y, width, height)
        
        #Put the QLineEdit and the label together (like a form)
        form_sample = QFormLayout()     #Creation of the layout form
        form_sample.addRow(label_sample_input, self.input_sample)     #Add things in the layout (by row)
        
        #Add the button "Send" to the previous layout by putting all that in another layout
        box_sample_input = QHBoxLayout()
        box_sample_input.addLayout(form_sample)
        #####################
        box_sample_input.setAlignment(Qt.AlignCenter)

        #Layout at top with buttons start and stop
        box_top = QHBoxLayout()
        box_top.addWidget(self.inibutton)
        box_top.addSpacing (0)
        box_top.addWidget(self.stopbutton)
        box_top.addLayout(box_sample_input)
        box_top.addStretch()

        box_top.addWidget(sepTestV[6])
        box_top.addWidget(self.label_state)


        
########################################################################################
########################################################################################
#######################################################
        # Choose of the commande mode
#######################################################
        

        #Create label: running or stopped state
        label_control = QLabel()    #Creation of the widget
        label_control.setText(" Control: ")    #Set the text in the label
        label_control.setAlignment(Qt.AlignCenter)   #Alignement of the label (here it's the vertical alignement)
        label_control.setFont(QFont("Arial",16,QFont.Bold))    #Set the writing font with the size


        group_infl = QButtonGroup(self.centralWidget)
        #Add a radio button to select mode of command
        self.Radio_volumeMode = QRadioButton("Mode: Volume")
        self.Radio_volumeMode.setChecked(True)
        self.mode = "volume"
        self.Radio_volumeMode.clicked.connect(lambda:self.Mode(self.Radio_volumeMode))
        group_infl.addButton(self.Radio_volumeMode)
        
        self.Radio_pressureMode = QRadioButton("Mode: Pressure")
        self.Radio_pressureMode.clicked.connect(lambda:self.Mode(self.Radio_pressureMode))
        group_infl.addButton(self.Radio_pressureMode)

        group_tension = QButtonGroup(self.centralWidget)
        #Add a radio button to select mode of command
        self.Radio_dispMode = QRadioButton("Mode: Displacement")
        self.Radio_dispMode.setChecked(True)
        self.mode = "disp"
        self.Radio_dispMode.clicked.connect(lambda:self.Mode(self.Radio_dispMode))
        group_tension.addButton(self.Radio_dispMode)
        
        self.Radio_loadMode = QRadioButton("Mode: Load")
        self.Radio_loadMode.clicked.connect(lambda:self.Mode(self.Radio_loadMode))
        group_tension.addButton(self.Radio_loadMode)




        box_control = QHBoxLayout()
        box_control.addSpacing (1)
        box_control.addStretch()
        box_control.addWidget(label_control)
        box_control.addSpacing (1)
        box_control.addStretch()
        box_control.addWidget(sepTestV[0])
        box_control.addSpacing (1)
        box_control.addStretch()
        ################################
        box__radio_infl = QVBoxLayout()
        box__radio_infl.addWidget(self.Radio_volumeMode)
        box__radio_infl.addWidget(self.Radio_pressureMode)
        
        ################################
        box_control.addLayout(box__radio_infl)

        box_control.addSpacing (1)
        box_control.addStretch()
        box_control.addWidget(sepTestV[1])
        
        ################################
        box__radio_tension = QVBoxLayout()
        box__radio_tension.addWidget(self.Radio_dispMode)
        box__radio_tension.addWidget(self.Radio_loadMode)
        
        ################################
        box_control.addLayout(box__radio_tension)


########################################################################################
########################################################################################
#######################################################
        #Choose of relative or absolute
#######################################################
        

        label_abs = QLabel()    #Creation of the widget
        label_abs.setText(" Displacement: ")    #Set the text in the label
        label_abs.setAlignment(Qt.AlignCenter)   #Alignement of the label (here it's the vertical alignement)
        label_abs.setFont(QFont("Arial",16,QFont.Bold))    #Set the writing font with the size


        group_abs = QButtonGroup(self.centralWidget)
        #Add a radio button to select mode of command
        self.Radio_absMode = QRadioButton("Mode: Absolute")
        self.Radio_absMode.setChecked(True)
        self.Radio_absMode.clicked.connect(lambda:self.Mode_disp(self.Radio_absMode))
        group_abs.addButton(self.Radio_absMode)
        
        self.Radio_relMode = QRadioButton("Mode: Relative")
        self.Radio_relMode.clicked.connect(lambda:self.Mode_disp(self.Radio_relMode))
        group_abs.addButton(self.Radio_relMode)





        box_dispMode = QHBoxLayout()
        box_dispMode.addSpacing (20)
        box_dispMode.addStretch()
        box_dispMode.addWidget(label_abs)
        box_dispMode.addSpacing (20)
        box_dispMode.addStretch()
        box_dispMode.addWidget(sepTestV[2])
        box_dispMode.addSpacing (20)
        box_dispMode.addStretch()
        box_dispMode.addWidget(self.Radio_absMode)
        box_dispMode.addSpacing (20)
        box_dispMode.addStretch()
        box_dispMode.addWidget(self.Radio_relMode)

        box_dispMode.addSpacing (20)
        box_dispMode.addStretch()
########################################################################################
########################################################################################
#######################################################
        #Choose command send
#######################################################

        label_commands = QLabel()    #Creation of the widget
        label_commands.setText(" Commands: ")    #Set the text in the label
        label_commands.setAlignment(Qt.AlignCenter)   #Alignement of the label (here it's the vertical alignement)
        label_commands.setFont(QFont("Arial",16,QFont.Bold))    #Set the writing font with the size

        ####################
        #Widget with user input for changing load
        self.input_load = QLineEdit()   #Creation of the widget
        self.input_load.setValidator(QDoubleValidator())   #Only double accepted
        self.input_load.setMaxLength(10)     #Number of characters accepted
        self.input_load.setAlignment(Qt.AlignRight)
        self.input_load.setFont(QFont("Arial",12))
        #self.input_load.setCursor(QCursor(Qt.ArrowCursor))    #If you want a different cursor shape when on the widget
        self.input_load.setStyleSheet("QLineEdit{background: white;}")    #Background color of the widget
        
        #hChange the writing color from write to black because we set the background write (I like when it's beautiful)
        self.input_load.palette = QPalette()
        self.input_load.palette.setColor(QPalette.Text, Qt.black)
        self.input_load.setPalette(self.input_load.palette)
        
        
        #Creation of the label attached to the QLineEdit
        self.label_load_input = QLabel("Disp (mm):", self)
        self.label_load_input.setFont(QFont("Arial",12,QFont.Bold))
        #self.lab.setGeometry(QRect(70, 80, 300, 300)) #(x, y, width, height)
        
        #Put the QLineEdit and the label together (like a form)
        form_load = QFormLayout()     #Creation of the layout form
        form_load.addRow(self.label_load_input, self.input_load)     #Add things in the layout (by row)
        
        #Add the button "Send" to the previous layout by putting all that in another layout
        box_load_input = QHBoxLayout()
        box_load_input.addLayout(form_load)
        #####################
        
        #####################
        #Widget with user input for changing pressure
        self.input_pressure = QLineEdit()
        self.input_pressure.setValidator(QDoubleValidator())
        self.input_pressure.setMaxLength(10)
        self.input_pressure.setAlignment(Qt.AlignRight)
        self.input_pressure.setFont(QFont("Arial",12))
        #input_pressure.setCursor(QCursor(Qt.ArrowCursor))
        self.input_pressure.setStyleSheet("QLineEdit{background: white;}")
        
        self.input_pressure.palette = QPalette()
        self.input_pressure.palette.setColor(QPalette.Text, Qt.black)
        self.input_pressure.setPalette(self.input_pressure.palette)
        
        
        self.label_pressure_input = QLabel("Volume (mL):", self)
        self.label_pressure_input.setFont(QFont("Arial",12,QFont.Bold))
        #self.lab.setGeometry(QRect(70, 80, 300, 300)) #(x, y, width, height)
        
        #Layout input label + input number
        form_pressure = QFormLayout()     #Creation of the layout form
        form_pressure.addRow(self.label_pressure_input, self.input_pressure)     #Add things in the layout
        
        #Add the button "Send" to the previous layout by putting all that in another layout
        box_pressure_input = QHBoxLayout()
        box_pressure_input.addLayout(form_pressure)
        
        
        
        
        box_command = QHBoxLayout()
        box_command.addSpacing (20)
        box_command.addStretch()
        box_command.addLayout(box_load_input)
        box_command.addSpacing (20)
        box_command.addStretch()
        box_command.addWidget(sepTestV[3])
        box_command.addSpacing (20)
        box_command.addStretch()
        box_command.addLayout(box_pressure_input)
        box_command.addSpacing (20)
        box_command.addStretch()





#######################################################
        #Stop & restart
#######################################################

        self.button_stop = QPushButton('Stop', self)
        self.button_stop.clicked.connect(self.clickMethodPause)
        self.button_stop.setStatusTip('Stop the test')
        self.button_stop.setIconSize(QSize(100,100))

        self.button_restart = QPushButton('Restart', self)
        self.button_restart.clicked.connect(self.clickMethodRestart)
        self.button_restart.setStatusTip('Restart the test')
        self.button_restart.setIconSize(QSize(100,100))

        self.button_cyclic = QPushButton('Cyclic', self)
        self.button_cyclic.clicked.connect(self.clickMethodCyclic)
        self.button_cyclic.setStatusTip('Start preconditioning')
        self.button_cyclic.setIconSize(QSize(100,100))

        box_break = QHBoxLayout()
        box_break.addSpacing (20)
        box_break.addStretch()
        box_break.addWidget(self.button_stop)
        box_break.addSpacing (20)
        box_break.addStretch()
        box_break.addWidget(self.button_restart)
        box_break.addSpacing (20)
        box_break.addStretch()
        box_break.addWidget(self.button_cyclic)
        box_break.addSpacing (20)
        box_break.addStretch()




#######################################################
        #Graph definition
#######################################################
        
        
        # Button for clear the graphs
        self.clrGraphButton = QPushButton('Clear Graphs', self)
        self.clrGraphButton.clicked.connect(self.clickMethodClearGraphs)
        self.clrGraphButton.setStatusTip('Clear the graphs')
        self.clrGraphButton.setIconSize(QSize(100,100))
        
        
        self.grapht = pg.PlotWidget(self)   #Creation of the graphic widget
        self.grapht.setMinimumSize(300,200)    #Set the minimum size of the graph

        self.graphd = pg.PlotWidget(self)   #Creation of the graphic widget
        self.graphd.setMinimumSize(300,200)    #Set the minimum size of the graph

        self.graphv = pg.PlotWidget(self)   #Creation of the graphic widget
        self.graphv.setMinimumSize(300,200)    #Set the minimum size of the graph

        #Creat the layout where to put the graph (and other things)
        graph_layout = QHBoxLayout()
#        graph_layout.addSpacing (20)
#        graph_layout.addStretch()
        graph_layout.addWidget(self.grapht)
#        graph_layout.addSpacing (20)
#        graph_layout.addStretch()
        graph_layout.addWidget(self.graphd)
#        graph_layout.addSpacing (20)
#        graph_layout.addStretch()
        graph_layout.addWidget(self.graphv)
#        graph_layout.addSpacing (20)
#        graph_layout.addStretch()


#######################################################
#######################################################


        self.panel_test_layout = QVBoxLayout()
        self.panel_test_layout.addLayout(box_top)
        self.panel_test_layout.addWidget(sepTestH[0])

        self.panel_test_layout.addLayout(box_control)
        self.panel_test_layout.addWidget(sepTestH[1])

        self.panel_test_layout.addLayout(box_dispMode)
        self.panel_test_layout.addWidget(sepTestH[2])

        self.panel_test_layout.addWidget(label_commands)
        
        self.panel_test_layout.addLayout(box_command)
        self.panel_test_layout.addWidget(sepTestH[3])

        self.panel_test_layout.addLayout(box_break)
        self.panel_test_layout.addWidget(sepTestH[4])
        
        self.panel_test_layout.addWidget(self.clrGraphButton)
        
        self.panel_test_layout.addWidget(sepTestH[5])

        self.panel_test_layout.addLayout(graph_layout)





    ###################################
    ###################################
    #Change the mode of command the pump when push the radio button
    
    def Mode(self, radio_mode):
        """Change the command mode (volume / pressure)"""
        if radio_mode.text() == "Mode: Volume":
            if radio_mode.isChecked() == True:
                self.label_pressure_input.setText("Volume (mL):")    #Set the text in the label
                
                
                print("Mode volume is selected")
                
        if radio_mode.text() == "Mode: Pressure":
            if radio_mode.isChecked() == True:
                self.label_pressure_input.setText("Pressure (MPa):")    #Set the text in the label

                
                print("Mode pressure is selected")


        if radio_mode.text() == "Mode: Displacement":
            if radio_mode.isChecked() == True:
                self.label_load_input.setText("Disp (mm):")    #Set the text in the label

                
                print("Mode disp is selected")
                
        if radio_mode.text() == "Mode: Load":
            if radio_mode.isChecked() == True:
                self.label_load_input.setText("Load (N):")    #Set the text in the label
                
                print("Mode load is selected")





    def Mode_disp(self, radio_mode):
        """Change the command mode"""
        if radio_mode.text() == "Mode: Absolute":
            if radio_mode.isChecked() == True:

                
                print("Mode: Absolute is selected")
                
        if radio_mode.text() == "Mode: Relative":
            if radio_mode.isChecked() == True:

                
                
                print("Mode: Relative is selected")



    def clickMethodSendLoad(self):
        """Method active when user push send button, send the value of pressure input"""
        try:
            MotorPI.connect()
            MotorPI.ref()
            MotorPI.move()
            MotorPI.disconnect()
        except:
            QMessageBox.about(self, "WARNING:", "The motor is not connected")

    def clickMethodSendPressure(self):
        """Method active when user push send button, send the value of displacement input"""
        
        if self.mode == "volume":
        
            try:
                PumpWM.dose(self.input_pressure.text())
    #            _thread.start_new_thread(PumpWM.send, (self.input_pressure.text(),mode,))
                #PumpWM.send(self.input_pressure.text())
            except SerialException:
                QMessageBox.about(self, "WARNING:", "The pump is not connected\n(check the serial ports)")

        if self.mode == "pressure":
        
            try:
                self.target_pressure = float(self.input_pressure.text())
                self.pump_run = True
                PumpWM.start()
    #            _thread.start_new_thread(PumpWM.send, (self.input_pressure.text(),mode,))
            except SerialException:
                QMessageBox.about(self, "WARNING:", "The pump is not connected\n(check the serial ports)")

    def clickMethodPause(self):
        """pause"""
        try:
            MotorPI.connect()
            MotorPI.stop()
            MotorPI.disconnect()
        except:
            QMessageBox.about(self, "WARNING:", "The motor is not connected")


        # Stop the pump

    def clickMethodRestart(self):
        """restart"""
        try:
            MotorPI.connect()
            MotorPI.move()
            MotorPI.disconnect()
        except:
            QMessageBox.about(self, "WARNING:", "The motor is not connected")

        # Restart the pump


    def clickMethodCyclic(self):
        """cyclic"""


    def clickMethodClearGraphs(self):
        
        reply = QMessageBox.question(self, 'Annihilation activated', 
                         'Clear them all ?!', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            
            self.grapht.clear()
            self.graphd.clear()
            self.graphv.clear()
            print("Graph cleared")





























