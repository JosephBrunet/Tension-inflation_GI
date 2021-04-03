
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton, QAction, QStatusBar, QFormLayout, QLabel, QLineEdit,
    QVBoxLayout, QHBoxLayout, QSpacerItem, QMessageBox, QFrame, QSizePolicy, QInputDialog, QGroupBox, QRadioButton, QButtonGroup, QGridLayout)
from PyQt5.QtCore import QSize, Qt, QRect, QRegExp, QThread, QThreadPool, QObject, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QDoubleValidator, QPixmap, QPalette, QColor, QCursor

from modules.sensors_dialogs import MotorPI
from modules.sensors_dialogs import Arduino    #Program created to connect / read... with the arduino microcontrol
from modules.sensors_dialogs import Pump_seringe    #Program to control the pump

import serial
from serial import SerialException
import serial.tools.list_ports

import time

from modules.mainwindow_modules.Right_panel import CommandThread




#
class Left_panel(object):
    def setup_left_panel(self, parent=None):

        #######################################################
                #Create all buttons
        #######################################################


        self.button_positioning = QPushButton('Positioning finished =>', self)
        self.button_positioning.clicked.connect(self.clickMethod_positioning)
        self.button_positioning.setStatusTip('Tare the pressure sensor')
        self.button_positioning.setIconSize(QSize(100,100))
        self.button_positioning.setMaximumSize(250,200)    #Set the minimum size of the button
        self.button_positioning.setFont(QFont("Arial",14,QFont.Bold))

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
        self.button_disp_less.clicked.connect(self.clickMethod_dispLess)
        self.button_disp_less.setStatusTip('Tare the pressure sensor')
        self.button_disp_less.setIconSize(QSize(100,100))
        self.button_disp_less.setMaximumSize(100,200)    #Set the minimum size of the button

        self.button_disp_0_d = QPushButton('Return to 0', self)
        self.button_disp_0_d.clicked.connect(self.clickMethod_disp0)
        self.button_disp_0_d.setStatusTip('')
        self.button_disp_0_d.setIconSize(QSize(100,100))
        self.button_disp_0_d.setMaximumSize(100,200)    #Set the minimum size of the button

        self.button_disp_0_P = QPushButton('Return to 0', self)
        self.button_disp_0_P.clicked.connect(self.clickMethod_pres0)
        self.button_disp_0_P.setStatusTip('')
        self.button_disp_0_P.setIconSize(QSize(100,100))
        self.button_disp_0_P.setMaximumSize(100,200)    #Set the minimum size of the button

        self.button_motor_stop = QPushButton('Stop', self)
        self.button_motor_stop.clicked.connect(self.clickMethod_motorStop)
        self.button_motor_stop.setStatusTip('')
        self.button_motor_stop.setIconSize(QSize(100,100))
        self.button_motor_stop.setMaximumSize(100,200)    #Set the minimum size of the button

        self.button_pump_stop = QPushButton('Stop', self)
        self.button_pump_stop.clicked.connect(self.clickMethod_pumpStop)
        self.button_pump_stop.setStatusTip('')
        self.button_pump_stop.setIconSize(QSize(100,100))
        self.button_pump_stop.setMaximumSize(100,200)    #Set the minimum size of the button

        #######################################################
                #Create all radio buttons
        #######################################################
        #Add a radio button  step vol

        group_vol = QButtonGroup(self.centralWidget)

        self.step_vol = 1
        self.Radio_step_vol1 = QRadioButton("1")
        group_vol.addButton(self.Radio_step_vol1)

        self.Radio_step_vol1.setChecked(True)
        self.Radio_step_vol1.clicked.connect(lambda:self.radio_vol_step(self.Radio_step_vol1))

        self.Radio_step_vol2 = QRadioButton("2")
        group_vol.addButton(self.Radio_step_vol2)

        self.Radio_step_vol2.clicked.connect(lambda:self.radio_vol_step(self.Radio_step_vol2))


        self.Radio_step_vol5 = QRadioButton("5")
        group_vol.addButton(self.Radio_step_vol5)

        self.Radio_step_vol5.clicked.connect(lambda:self.radio_vol_step(self.Radio_step_vol5))

        #Add a radio button  step disp
        group_disp = QButtonGroup(self.centralWidget)

        self.step_disp = 1
        self.Radio_step_disp1 = QRadioButton("1")
        self.Radio_step_disp1.setChecked(True)
        self.Radio_step_disp1.clicked.connect(lambda:self.radio_disp_step(self.Radio_step_disp1))
        group_disp.addButton(self.Radio_step_disp1)

        self.Radio_step_disp2 = QRadioButton("2")
        self.Radio_step_disp2.clicked.connect(lambda:self.radio_disp_step(self.Radio_step_disp2))
        group_disp.addButton(self.Radio_step_disp2)

        self.Radio_step_disp5 = QRadioButton("5")
        self.Radio_step_disp5.clicked.connect(lambda:self.radio_disp_step(self.Radio_step_disp5))
        group_disp.addButton(self.Radio_step_disp5)



        #######################################################
                # Creation labels
        #######################################################

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
        self.label_disp_abs_display.setFont(QFont("Arial",8,))

        self.label_disp_rel_display = QLabel()
        self.label_disp_rel_display.setText("Connecting")
        self.label_disp_rel_display.setAlignment(Qt.AlignCenter)
        self.label_disp_rel_display.setFont(QFont("Arial",16,))



        self.label_phase = QLabel()
        self.label_phase.setText("Phase : Positioning")
        self.label_phase.setAlignment(Qt.AlignLeft)
        self.label_phase.setFont(QFont("Arial",24,QFont.Bold))
        self.label_phase.setStyleSheet("background-color: QColor(200, 0, 0)")

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
        box_radio_vol.addWidget(self.Radio_step_vol1)
        box_radio_vol.addWidget(self.Radio_step_vol2)
        box_radio_vol.addWidget(self.Radio_step_vol5)

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
        box_radio_disp.addWidget(self.Radio_step_disp1)
        box_radio_disp.addWidget(self.Radio_step_disp2)
        box_radio_disp.addWidget(self.Radio_step_disp5)

        box_disp_step.addLayout(box_radio_disp)
        ###############


        n=0
        panel_grid = QGridLayout()
        panel_grid.setSpacing(10)
        panel_grid.addWidget(label_pressure_title, 0, n)
        panel_grid.addWidget(sepH[0], 1, n)
        panel_grid.addWidget(self.label_pressure_display, 2, n, Qt.AlignRight)
        panel_grid.addWidget(tarebutton_pressure, 3, n, Qt.AlignCenter)
        panel_grid.addWidget(self.button_disp_0_P, 4, n, Qt.AlignCenter)

        panel_grid.addWidget(sepV[0], 0, 1, 10, 1)


        n=2
        panel_grid.addWidget(label_volume_title, 0, n)
        panel_grid.addWidget(sepH[1], 1, n)
        panel_grid.addWidget(self.label_volume_display, 2, n)
        panel_grid.addWidget(tarebutton_volume, 3, n, Qt.AlignCenter)
        panel_grid.addLayout(box_volume_pm, 4, n)
        panel_grid.addLayout(box_volume_step, 5, n)
        panel_grid.addWidget(self.button_pump_stop, 6, n, Qt.AlignCenter)


        panel_grid.addWidget(sepV[1], 0, 3, 10, 1)


        n=4
        panel_grid.addWidget(label_load_title, 0, n)
        panel_grid.addWidget(sepH[2], 1, n)
        panel_grid.addWidget(self.label_load_display, 2, n, Qt.AlignCenter)
        panel_grid.addWidget(tarebutton_load, 3, n, Qt.AlignCenter)


        panel_grid.addWidget(sepV[2], 0, 5, 10, 1)


        n=6
        panel_grid.addWidget(label_disp_title, 0, n)
        panel_grid.addWidget(sepH[3], 1, n)
        panel_grid.addLayout(box_disp_rel_abs_display, 2, n)
        panel_grid.addWidget(tarebutton_disp, 3, n, Qt.AlignCenter)

        panel_grid.addLayout(box_disp_pm, 4, n)
        panel_grid.addLayout(box_disp_step, 5, n)
        panel_grid.addWidget(self.button_disp_0_d, 6, n, Qt.AlignCenter)
        panel_grid.addWidget(self.button_motor_stop, 7, n, Qt.AlignCenter)


        panel_grid.setColumnMinimumWidth(0, 140)
        panel_grid.setColumnMinimumWidth(2, 140)
        panel_grid.setColumnMinimumWidth(4, 140)
        panel_grid.setColumnMinimumWidth(6, 140)


        layout_pos = QHBoxLayout()
        layout_pos.addWidget(self.label_phase)
        layout_pos.addSpacing (20)
        layout_pos.addWidget(self.button_positioning)

        panel_layout = QVBoxLayout()
        panel_layout.addLayout(layout_pos)
        panel_layout.addStretch()
        panel_layout.addSpacing (100)
        panel_layout.addStretch()
        panel_layout.addLayout(panel_grid)
        panel_layout.addStretch()

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
        self.test_phase()
        self.label_phase.setText("Phase: Test command")

#        QMessageBox.about(self, "Run the engine:", "The positioning is now finished.\n\nThe test phase will start, when you are ready clic on the white arrow")



    def test_phase(self):
        """Method to activate the test phase"""

        self.input_sample.setDisabled(False)
        self.inibutton.setDisabled(False)
        self.stopbutton.setDisabled(False)
        self.input_sample.setDisabled(False)
        self.Radio_volumeMode.setDisabled(False)
        self.Radio_pressureMode.setDisabled(False)
        self.Radio_dispMode.setDisabled(False)
        self.Radio_loadMode.setDisabled(False)
        self.input_disp_load.setDisabled(False)
        self.input_vol_pressure.setDisabled(False)
        self.input_cycleF.setDisabled(False)
        self.input_cycleP.setDisabled(False)



        self.button_vol_more.setDisabled(True)
        self.button_vol_less.setDisabled(True)
        self.button_disp_more.setDisabled(True)
        self.button_disp_less.setDisabled(True)
        self.Radio_step_vol1.setDisabled(True)
        self.Radio_step_vol2.setDisabled(True)
        self.Radio_step_vol5.setDisabled(True)
        self.Radio_step_disp1.setDisabled(True)
        self.Radio_step_disp2.setDisabled(True)
        self.Radio_step_disp5.setDisabled(True)
        self.button_positioning.setDisabled(True)
        self.button_pause.setDisabled(True)
        self.button_restart.setDisabled(True)
        self.button_scan.setDisabled(True)



    def positioning_phase(self):
        """Method to activate the positionning phase"""

        self.input_sample.setDisabled(True)
        self.inibutton.setDisabled(True)
        self.stopbutton.setDisabled(True)
        self.input_sample.setDisabled(True)
        self.Radio_volumeMode.setDisabled(True)
        self.Radio_pressureMode.setDisabled(True)
        self.Radio_dispMode.setDisabled(True)
        self.Radio_loadMode.setDisabled(True)
        self.input_disp_load.setDisabled(True)
        self.input_vol_pressure.setDisabled(True)
        self.input_cycleF.setDisabled(True)
        self.input_cycleP.setDisabled(True)
        self.button_pause.setDisabled(True)
        self.button_restart.setDisabled(True)
        self.button_scan.setDisabled(True)

        self.button_vol_more.setDisabled(False)
        self.button_vol_less.setDisabled(False)
        self.button_disp_more.setDisabled(False)
        self.button_disp_less.setDisabled(False)
        self.Radio_step_vol1.setDisabled(False)
        self.Radio_step_vol2.setDisabled(False)
        self.Radio_step_vol5.setDisabled(False)
        self.Radio_step_disp1.setDisabled(False)
        self.Radio_step_disp2.setDisabled(False)
        self.Radio_step_disp5.setDisabled(False)

        self.button_positioning.setDisabled(False)
        self.Radio_graphON.setDisabled(False)
        self.Radio_graphOFF.setDisabled(False)


    def running_phase(self):
        """Method to activate the running phase"""
        self.input_sample.setDisabled(True)
        self.inibutton.setDisabled(True)
#        self.stopbutton.setDisabled(True)
        self.input_sample.setDisabled(True)
        self.Radio_volumeMode.setDisabled(True)
        self.Radio_pressureMode.setDisabled(True)
        self.Radio_dispMode.setDisabled(True)
        self.Radio_loadMode.setDisabled(True)
        self.input_disp_load.setDisabled(True)
        self.input_vol_pressure.setDisabled(True)
        self.input_cycleF.setDisabled(True)
        self.input_cycleP.setDisabled(True)

        self.button_vol_more.setDisabled(True)
        self.button_vol_less.setDisabled(True)
        self.button_disp_more.setDisabled(True)
        self.button_disp_less.setDisabled(True)
        self.Radio_step_vol1.setDisabled(True)
        self.Radio_step_vol2.setDisabled(True)
        self.Radio_step_vol5.setDisabled(True)
        self.Radio_step_disp1.setDisabled(True)
        self.Radio_step_disp2.setDisabled(True)
        self.Radio_step_disp5.setDisabled(True)
        self.button_positioning.setDisabled(True)
        self.Radio_graphON.setDisabled(True)
        self.Radio_graphOFF.setDisabled(True)
        self.button_pause.setDisabled(False)
        self.button_restart.setDisabled(False)
        self.button_scan.setDisabled(False)


    def pause_phase(self):
        """Method to activate the pause phase"""

        self.input_disp_load.setDisabled(False)
        self.input_vol_pressure.setDisabled(False)
        self.Radio_volumeMode.setDisabled(False)
        self.Radio_pressureMode.setDisabled(False)
        self.Radio_dispMode.setDisabled(False)
        self.Radio_loadMode.setDisabled(False)
        self.input_cycleF.setDisabled(False)
        self.input_cycleP.setDisabled(False)






    def clickMethodTare_vol(self):
        """Method to tare volume"""

        reply = QMessageBox.question(self, 'To Tare or not to tare, that is the question !',
                         'Are you sure ?', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            Pump_seringe.vol_clear()
            print("Vol tare")

        else:
            print("no")
            #do something if no

    def clickMethodTare_pressure(self):
        """Method to tare pressure"""
        reply = QMessageBox.question(self, 'To Tare or not to tare, that is the question !',
                         'Are you sure ?', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                Arduino.write_ino("tare_P")   #Send to the arduino the command that activate the function Tare
                print("Tare Pressure")
            except SerialException:
                QMessageBox.about(self, "WARNING:", "Problem with arduino program sending !")


    def clickMethodTare_disp(self):
        """Method to tare displacement"""
        reply = QMessageBox.question(self, 'To Tare or not to tare, that is the question !',
                         'Are you sure ?', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.tare_disp = MotorPI.motor_pos()
            print("Disp tare")



    def clickMethodTare_load(self):
        """Method to tare load"""
        reply = QMessageBox.question(self, 'To Tare or not to tare, that is the question !',
                         'Are you sure ?', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                Arduino.write_ino("tare_F")   #Send to the arduino the command that activate the function Tare
            except SerialException:
                QMessageBox.about(self, "WARNING:", "Problem with arduino program sending !")





    def clickMethod_volMore(self):
        """Method to """
        self.pump_run = True
        time.sleep(0.1)
        try:
            Pump_seringe.dose(self.step_vol)
        except:
            QMessageBox.about(self, "WARNING:", "The pump is not connected")
        self.pump_run = False

    def clickMethod_volLess(self):
        """Method to """
        self.pump_run=True
        time.sleep(0.1)
        try:
            Pump_seringe.dose(-self.step_vol)
        except:
            QMessageBox.about(self, "WARNING:", "The pump is not connected")
        self.pump_run=False

    def clickMethod_dispMore(self):
        """Method to """
        try:
            MotorPI.move_rel(self.step_disp)
        except:
            QMessageBox.about(self, "WARNING:", "The motor is not connected")


    def clickMethod_dispLess(self):
        """Method to """

        try:
            MotorPI.move_rel(-self.step_disp)
        except:
            QMessageBox.about(self, "WARNING:", "The motor is not connected")

    def clickMethod_disp0(self):
        """Method to """
        msg = QMessageBox.question(self,"Come back to the base","Are u sure ?",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if msg == QMessageBox.Yes:
            try:
                MotorPI.move_rel(-round((self.d-self.tare_disp),2))
            except:
                QMessageBox.about(self, "WARNING:", "The motor is not connected")

    def clickMethod_pres0(self):
        """Method for pressure to return to 0 mmHg"""
        msg = QMessageBox.question(self,"Come back to 0 pressure","Are u sure ?",
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if msg == QMessageBox.Yes:
            self.CommandThread = CommandThread(0, 10, 0, 0, 'P', 'D')
            self.CommandThread.signal_end.connect(self.test_end)
            self.CommandThread.update_thread.connect(self.update_value)
            self.CommandThread.signal_pump_run.connect(self.pump_state)
            self.CommandThread.start()




    def clickMethod_motorStop(self):
        """Method to """
        MotorPI.stop()

    def clickMethod_pumpStop(self):
        """Method to """
        Pump_seringe.stop()


###############################################
#Function for radio buttons
###############################################

    def radio_vol_step(self, radio_value):
        if radio_value.text() == "1":
            if radio_value.isChecked() == True:
                self.step_vol = 1

        if radio_value.text() == "2":
            if radio_value.isChecked() == True:
                self.step_vol = 2

        if radio_value.text() == "5":
            if radio_value.isChecked() == True:
                self.step_vol = 5


    def radio_disp_step(self, radio_value):
        if radio_value.text() == "1":
            if radio_value.isChecked() == True:
                self.step_disp = 1

        if radio_value.text() == "2":
            if radio_value.isChecked() == True:
                self.step_disp = 2

        if radio_value.text() == "5":
            if radio_value.isChecked() == True:
                self.step_disp = 5
