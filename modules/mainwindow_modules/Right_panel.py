
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton, QAction, QStatusBar, QFormLayout, QLabel, QLineEdit,
    QVBoxLayout, QHBoxLayout, QSpacerItem, QMessageBox, QFrame, QSizePolicy, QInputDialog, QGroupBox, QRadioButton, QButtonGroup)
from PyQt5.QtCore import QSize, Qt, QRegExp, QThread, QThreadPool, QObject, pyqtSignal

from PyQt5.QtGui import QIcon, QFont, QDoubleValidator, QPixmap, QPalette, QColor, QCursor, QRegExpValidator

import numpy as np    #For mathematics
import pyqtgraph as pg    #Library to plot graph with pyqt
import time

from modules.sensors_dialogs import MotorPI    #Program to control the axial motor
from modules.sensors_dialogs import Arduino    #Program created to connect / read... with the arduino microcontrol
from modules.sensors_dialogs import Pump_seringe    #Program to control the pump

from simple_pid import PID




class CommandThread(QThread):
    """Command Motor and then Pump"""

    signal_end = pyqtSignal()
    update_thread = QtCore.pyqtSignal()
    signal_pump_run = QtCore.pyqtSignal(bool)

    def __init__(self, dF_target, PV_target, NcycleF, NcycleP, PVmode, FDmode):
        super(QThread, self).__init__()
        self.pause = False
        self.dF_target = dF_target
        self.PV_target = PV_target
        self.NcycleF = NcycleF
        self.NcycleP = NcycleP
        self.PVmode = PVmode
        self.FDmode = FDmode

        self.P = False
        self.F = False

    def stop(self):
        self.pause = True
        try:
            MotorPI.stop()
        except:
            print("CommandThread motor")
        try:
            Pump_seringe.stop()
        except:
            print("CommandThread pump")


    def update_value(self,F,P):
        self.F=F
        self.P=P


    def run(self):
        print("thread start")


        ######################################################################
        ######################################################################
        ## Motor (displacement)
        ######################################################################
        ######################################################################

        if self.FDmode == 'D' and not self.dF_target == '':
            #Cycles first
            if self.NcycleF != 0:
                cycle=0
                while cycle < self.NcycleF:

                    MotorPI.move_rel(self.dF_target)
                    while MotorPI.ismoving():
                        #print("motor running")
                        time.sleep(0.1)
                    if self.pause == True:
                        return
                    MotorPI.move_rel(-self.dF_target)
                    while MotorPI.ismoving():
                        time.sleep(0.1)
                    cycle = cycle +1

            if self.pause:
                return

            MotorPI.move_rel(self.dF_target)
            while MotorPI.ismoving():
                time.sleep(0.1)

        elif self.FDmode == 'F' and not self.dF_target == '':
            self.update_thread.emit()

            while self.F == False:
                time.sleep(0.1)
            while self.F < self.dF_target*0.90  or self.F > self.dF_target*1.10 :
                self.update_thread.emit()
                if self.F < self.dF_target*0.90:
                    MotorPI.move_rel(0.2)
                    while MotorPI.ismoving():
                        time.sleep(0.1)

                if self.F > self.dF_target*1.10:
                    MotorPI.move_rel(-0.2)

                    while MotorPI.ismoving():
                        time.sleep(0.1)

                self.update_thread.emit()
                time.sleep(0.5)



        if self.pause:
            return


        ######################################################################
        ######################################################################
        ## PUMP
        ######################################################################
        ######################################################################



        if self.PVmode == 'V' and not self.PV_target == '':
            #Cycles first
            if self.NcycleP != 0:
                cycle=0
                while cycle < self.NcycleP:

                    self.signal_pump_run.emit(True)
                    Pump_seringe.dose(self.PV_target)

                    waitingTime = abs(float(self.PV_target) / float(Pump_seringe.getFlowRate()))*60 + 2
                    print(str(waitingTime))
                    self.signal_pump_run.emit(False)
                    time.sleep(waitingTime)

                    self.signal_pump_run.emit(True)
                    Pump_seringe.dose(-self.PV_target)

                    waitingTime = abs(float(self.PV_target) / float(Pump_seringe.getFlowRate()))*60 + 2
                    print(str(waitingTime))
                    self.signal_pump_run.emit(False)
                    time.sleep(waitingTime)

                    cycle = cycle +1


            self.signal_pump_run.emit(True)
            Pump_seringe.dose(self.PV_target)

            waitingTime = abs(float(self.PV_target) / float(Pump_seringe.getFlowRate()))*60 + 1
            print(str(waitingTime))
            self.signal_pump_run.emit(False)
            time.sleep(waitingTime)





        ## MODE PRESSURE CONSTANT


        elif self.PVmode == 'P' and not self.PV_target == '':

            if self.P > self.PV_target:
                self.NcycleP=0

            self.update_thread.emit()
            time.sleep(0.1)
            #Cycles first
            if self.NcycleP != 0:
                cycle=0
                while cycle < self.NcycleP:


                    #Cycle montant
                    pump_running = False
                    flag= False
                    while self.pause == False and flag == False:

                        self.update_thread.emit()
                        if self.P > self.PV_target:

                            self.signal_pump_run.emit(True)
                            time.sleep(0.02)
                            Pump_seringe.stop()
                            pump_running = False
                            self.signal_pump_run.emit(False)
                            flag = True


                        if pump_running == False and flag == False:
                            self.signal_pump_run.emit(True)
                            time.sleep(0.05)
                            try:
                                Pump_seringe.run()
                            except:
                                print("error in pump thread")
                            pump_running = True
                            time.sleep(0.02)
                            self.signal_pump_run.emit(False)
                            time.sleep(0.05)

                        self.update_thread.emit()
                        time.sleep(0.05)

                    time.sleep(0.05)

                    #Cycle descendant
                    pump_running = False
                    flag= False
                    while self.pause == False and flag == False:

                        self.update_thread.emit()
                        if self.P <= 0.8*self.PV_target:

                            self.signal_pump_run.emit(True)
                            time.sleep(0.02)
                            Pump_seringe.stop()
                            pump_running = False
                            self.signal_pump_run.emit(False)
                            flag = True


                        if pump_running == False and flag == False:
                            self.signal_pump_run.emit(True)
                            time.sleep(0.02)
                            Pump_seringe.dose(-80)
                            pump_running = True
                            time.sleep(0.02)
                            self.signal_pump_run.emit(False)
                            time.sleep(0.02)

                        self.update_thread.emit()
                        time.sleep(0.05)

                    cycle = cycle +1



            print("Go to "+str(self.PV_target))
            time.sleep(0.05)





            #MANAGE PRESSION INFERIOR TO TARGET
            if self.P < self.PV_target:


                while self.pause == False and self.P < self.PV_target*0.98:
                    self.update_thread.emit()
                    Pump_seringe.setDirection('INF')
                    Pump_seringe.run()
                    time.sleep(0.1)
                Pump_seringe.stop()


                pid = PID(1, 0.1, 0.05, setpoint=self.PV_target)
                pid.sample_time = 0.1  # update every 0.01 seconds
                pid.output_limits = (0, 5)

                start = time.time()
                while self.pause == False:
                    self.update_thread.emit()
                    # compute new ouput from the PID according to the systems current value
                    output = pid(self.P)
                    print(output)

                    if time.time() - start > 0.5:
                        # feed the PID output to the system and get its current value
                        Pump_seringe.stop()
                        Pump_seringe.setFlowRate(output)
                        Pump_seringe.run()
                        start = time.time()
                    time.sleep(0.05)
                time.sleep(0.01)
                Pump_seringe.setFlowRate(5)
                time.sleep(0.01)


            #MANAGE PRESSURE SUPERIOR TO TARGET
            elif self.P > self.PV_target:

                pump_running = False
                flag= False
                Pump_seringe.setFlowRate(5)
                while self.pause == False and flag == False:

                    self.update_thread.emit()
                    if self.P < self.PV_target:

                        self.signal_pump_run.emit(True)
                        time.sleep(0.02)
                        Pump_seringe.stop()
                        pump_running = False
                        self.signal_pump_run.emit(False)
                        flag = True


                    if self.P > self.PV_target and pump_running == False:
                        self.signal_pump_run.emit(True)
                        time.sleep(0.02)
                        Pump_seringe.dose(-60)
                        pump_running = True
                        time.sleep(0.02)
                        self.signal_pump_run.emit(False)
                        time.sleep(0.02)

                    self.update_thread.emit()
                    time.sleep(0.05)


        self.signal_pump_run.emit(False)
        print("QThread terminated")
        self.signal_end.emit()





#
class Right_panel(object):
    def setup_right_panel(self, parent=None):

        self.PVmode = 'P'
        self.FDmode = 'D'

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
        self.inibutton.setIcon(QIcon('ressources/button_start_push.png'))   #Change the button's icon by the ressources
        self.inibutton.setIconSize(QSize(30,30))   #Change the size of the icon




        # Add button for stop
        self.stopbutton = QPushButton(self)
        self.stopbutton.clicked.connect(self.clickMethodStop)
        self.stopbutton.setIcon(QIcon('ressources/button_stop.png'))
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
        self.input_sample.setMaxLength(30)     #Number of characters accepted
        self.input_sample.setAlignment(Qt.AlignRight)
        self.input_sample.setFont(QFont("Arial",12))
        self.input_sample.setStyleSheet("QLineEdit{background: white;}")    #Background color of the widget

        #hChange the writing color from write to black because we set the background write (I like when it's beautiful)
        self.input_sample.palette = QPalette()
        self.input_sample.palette.setColor(QPalette.Text, Qt.black)
        self.input_sample.setPalette(self.input_sample.palette)


        #Creation of the label attached to the QLineEdit
        label_sample_input = QLabel("Sample Name:", self)
        label_sample_input.setFont(QFont("Arial",12,QFont.Bold))

        #Put the QLineEdit and the label together (like a form)
        form_sample = QFormLayout()     #Creation of the layout form
        form_sample.addRow(label_sample_input, self.input_sample)     #Add things in the layout (by row)

        #Add the button "Send" to the previous layout by putting all that in another layout
        box_sample_input = QHBoxLayout()
        box_sample_input.addLayout(form_sample)
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
        self.Radio_volumeMode.clicked.connect(lambda:self.Mode(self.Radio_volumeMode))
        group_infl.addButton(self.Radio_volumeMode)

        self.Radio_pressureMode = QRadioButton("Mode: Pressure")
        self.Radio_pressureMode.setChecked(True)
        self.Radio_pressureMode.clicked.connect(lambda:self.Mode(self.Radio_pressureMode))
        group_infl.addButton(self.Radio_pressureMode)

        group_tension = QButtonGroup(self.centralWidget)
        #Add a radio button to select mode of command
        self.Radio_dispMode = QRadioButton("Mode: Displacement")
        self.Radio_dispMode.setChecked(True)
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
        # Choose the pre-loading
#######################################################

        label_preloading = QLabel()    #Creation of the widget
        label_preloading.setText(" Pre-loading: ")    #Set the text in the label
        label_preloading.setAlignment(Qt.AlignCenter)   #Alignement of the label (here it's the vertical alignement)
        label_preloading.setFont(QFont("Arial",16,QFont.Bold))    #Set the writing font with the size


        #####################
        self.input_cycleF = QLineEdit()
        self.input_cycleF.setValidator(QDoubleValidator())
        self.input_cycleF.setMaxLength(2)
        self.input_cycleF.setAlignment(Qt.AlignRight)
        self.input_cycleF.setFont(QFont("Arial",12))
        #input_vol_pressure.setCursor(QCursor(Qt.ArrowCursor))
        self.input_cycleF.setStyleSheet("QLineEdit{background: white;}")

        self.input_cycleF.palette = QPalette()
        self.input_cycleF.palette.setColor(QPalette.Text, Qt.black)
        self.input_cycleF.setPalette(self.input_cycleF.palette)


        self.label_cyclF = QLabel("Cycle Disp:", self)
        self.label_cyclF.setFont(QFont("Arial",12,QFont.Bold))
        #self.lab.setGeometry(QRect(70, 80, 300, 300)) #(x, y, width, height)

        #Layout input label + input number
        form_cycleF = QFormLayout()     #Creation of the layout form
        form_cycleF.addRow(self.label_cyclF, self.input_cycleF)     #Add things in the layout

        #Add the button "Send" to the previous layout by putting all that in another layout
        box_cycle_inputF = QHBoxLayout()
        box_cycle_inputF.addLayout(form_cycleF)

        #####################
        self.input_cycleP = QLineEdit()
        self.input_cycleP.setValidator(QDoubleValidator())
        self.input_cycleP.setMaxLength(2)
        self.input_cycleP.setAlignment(Qt.AlignRight)
        self.input_cycleP.setFont(QFont("Arial",12))
        #input_vol_pressure.setCursor(QCursor(Qt.ArrowCursor))
        self.input_cycleP.setStyleSheet("QLineEdit{background: white;}")

        self.input_cycleP.palette = QPalette()
        self.input_cycleP.palette.setColor(QPalette.Text, Qt.black)
        self.input_cycleP.setPalette(self.input_cycleP.palette)


        self.label_cyclP = QLabel("Cycle Pump:", self)
        self.label_cyclP.setFont(QFont("Arial",12,QFont.Bold))
        #self.lab.setGeometry(QRect(70, 80, 300, 300)) #(x, y, width, height)

        #Layout input label + input number
        form_cycleP = QFormLayout()     #Creation of the layout form
        form_cycleP.addRow(self.label_cyclP, self.input_cycleP)     #Add things in the layout

        #Add the button "Send" to the previous layout by putting all that in another layout
        box_cycle_inputP = QHBoxLayout()
        box_cycle_inputP.addLayout(form_cycleP)


        box_preloading = QHBoxLayout()
        box_preloading.addSpacing (5)
        box_preloading.addLayout(box_cycle_inputF)
        box_preloading.addStretch()
        box_preloading.addLayout(box_cycle_inputP)
        box_preloading.addSpacing (5)


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
        self.input_disp_load = QLineEdit()   #Creation of the widget
        self.input_disp_load.setValidator(QDoubleValidator())   #Only double accepted
        self.input_disp_load.setMaxLength(10)     #Number of characters accepted
        self.input_disp_load.setAlignment(Qt.AlignRight)
        self.input_disp_load.setFont(QFont("Arial",12))
        #self.input_disp_load.setCursor(QCursor(Qt.ArrowCursor))    #If you want a different cursor shape when on the widget
        self.input_disp_load.setStyleSheet("QLineEdit{background: white;}")    #Background color of the widget

        #hChange the writing color from write to black because we set the background write (I like when it's beautiful)
        self.input_disp_load.palette = QPalette()
        self.input_disp_load.palette.setColor(QPalette.Text, Qt.black)
        self.input_disp_load.setPalette(self.input_disp_load.palette)


        #Creation of the label attached to the QLineEdit
        self.label_load_input = QLabel("Disp (mm):", self)
        self.label_load_input.setFont(QFont("Arial",12,QFont.Bold))
        #self.lab.setGeometry(QRect(70, 80, 300, 300)) #(x, y, width, height)

        #Put the QLineEdit and the label together (like a form)
        form_load = QFormLayout()     #Creation of the layout form
        form_load.addRow(self.label_load_input, self.input_disp_load)     #Add things in the layout (by row)

        #Add the button "Send" to the previous layout by putting all that in another layout
        box_load_input = QHBoxLayout()
        box_load_input.addLayout(form_load)
        #####################

        #####################
        #Widget with user input for changing pressure
        self.input_vol_pressure = QLineEdit()
        self.input_vol_pressure.setValidator(QDoubleValidator())
        self.input_vol_pressure.setMaxLength(10)
        self.input_vol_pressure.setAlignment(Qt.AlignRight)
        self.input_vol_pressure.setFont(QFont("Arial",12))
        #input_vol_pressure.setCursor(QCursor(Qt.ArrowCursor))
        self.input_vol_pressure.setStyleSheet("QLineEdit{background: white;}")

        self.input_vol_pressure.palette = QPalette()
        self.input_vol_pressure.palette.setColor(QPalette.Text, Qt.black)
        self.input_vol_pressure.setPalette(self.input_vol_pressure.palette)


        self.label_pressure_input = QLabel("Pressure (mmHg):", self)
        self.label_pressure_input.setFont(QFont("Arial",12,QFont.Bold))
        #self.lab.setGeometry(QRect(70, 80, 300, 300)) #(x, y, width, height)

        #Layout input label + input number
        form_pressure = QFormLayout()     #Creation of the layout form
        form_pressure.addRow(self.label_pressure_input, self.input_vol_pressure)     #Add things in the layout

        #Add the button "Send" to the previous layout by putting all that in another layout
        box_pressure_input = QHBoxLayout()
        box_pressure_input.addLayout(form_pressure)


         #####################




        box_command = QHBoxLayout()
        box_command.addSpacing (5)
        box_command.addLayout(box_load_input)
        box_command.addSpacing (5)
        box_command.addWidget(sepTestV[3])
        box_command.addSpacing (5)
        box_command.addLayout(box_pressure_input)
        box_command.addSpacing (5)
        box_command.addWidget(sepTestV[4])
        box_command.addSpacing (5)




#######################################################
        #Stop & restart
#######################################################

        self.button_pause = QPushButton( self)
        self.button_pause.clicked.connect(self.clickMethodPause)
        self.button_pause.setIcon(QIcon('ressources/button_pause.png'))
        self.button_pause.setStatusTip('Stop the test')
        self.button_pause.setFixedSize( 60, 50 )
        self.button_pause.setIconSize(QSize(40, 40))

        self.button_restart = QPushButton( self)
        self.button_restart.clicked.connect(self.clickMethodRestart)
        self.button_restart.setIcon(QIcon('ressources/button_restart.png'))
        self.button_restart.setStatusTip('Restart the test')
        self.button_restart.setFixedSize( 60, 50 )
        self.button_restart.setIconSize(QSize(40, 40))

        self.button_scan = QPushButton('SCAN', self)
        self.button_scan.clicked.connect(self.clickMethodScan)
        self.button_scan.setStatusTip('Scan start')
        self.button_scan.setFixedSize( 60, 50 )
        self.button_scan.setIconSize(QSize(40, 40))

        box_break = QHBoxLayout()
        box_break.addSpacing (20)
        box_break.addStretch()
        box_break.addWidget(self.button_pause)
        box_break.addSpacing (20)
        box_break.addStretch()
        box_break.addWidget(self.button_restart)
        box_break.addSpacing (20)
        box_break.addStretch()
        box_break.addWidget(self.button_scan)
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


        self.graph1 = pg.PlotWidget(self, title="Graph 1")   #Creation of the graphic widget
        self.graph1.setMinimumSize(300,300)    #Set the minimum size of the graph
        self.graph1.showGrid(x=True, y=True)
        self.graph1.setLabel('left', 'Load (N)')
        self.graph1.setLabel('bottom', 'Pressure (mmHg)')

        self.graphL=self.graph1.plot(pen=None, symbol='+')    #Show on the graph


        self.graph2 = pg.PlotWidget(self, title="Graph 2")   #Creation of the graphic widget
        self.graph2.setMinimumSize(300,300)    #Set the minimum size of the graph
        self.graph2.showGrid(x=True, y=True)
        self.graph2.setLabel('left', 'Pressure (mmHg)')
        self.graph2.setLabel('bottom', 'Time (s)')


        self.graphR=self.graph2.plot(pen=None, symbol='+')    #Show on the graph


        group_graph = QButtonGroup(self.centralWidget)
        #Add a radio button to select mode of command
        self.Radio_graphON = QRadioButton("Graph: On")

        self.Radio_graphON.clicked.connect(lambda:self.graph_state(self.Radio_graphON))
        group_graph.addButton(self.Radio_graphON)

        self.Radio_graphOFF = QRadioButton("Graph: Off")
        self.Radio_graphOFF.setChecked(True)
        self.Radio_graphOFF.clicked.connect(lambda:self.graph_state(self.Radio_graphOFF))
        group_graph.addButton(self.Radio_graphOFF)





        #Creat the layout where to put the graph (and other things)
        graph_layout = QHBoxLayout()
        graph_layout.addWidget(self.graph1)
        graph_layout.addWidget(self.graph2)
        graph_mode = QHBoxLayout()
        graph_mode.addWidget(self.Radio_graphON)
        graph_mode.addWidget(self.Radio_graphOFF)
        graph_mode.addWidget(self.clrGraphButton)

#######################################################
#######################################################


        self.panel_test_layout = QVBoxLayout()
        self.panel_test_layout.addLayout(box_top)
        self.panel_test_layout.addWidget(sepTestH[0])
        self.panel_test_layout.addLayout(box_control)
        self.panel_test_layout.addWidget(sepTestH[1])

        self.panel_test_layout.addWidget(label_preloading)
        self.panel_test_layout.addSpacing (20)
        self.panel_test_layout.addLayout(box_preloading)
        self.panel_test_layout.addWidget(sepTestH[2])



        self.panel_test_layout.addWidget(label_commands)
        self.panel_test_layout.addSpacing (20)
        self.panel_test_layout.addLayout(box_command)
        self.panel_test_layout.addWidget(sepTestH[3])
        self.panel_test_layout.addLayout(box_break)
        self.panel_test_layout.addWidget(sepTestH[4])
        self.panel_test_layout.addLayout(graph_mode)
        self.panel_test_layout.addLayout(graph_layout)



    ###################################
    ###################################
    #Change the mode of command the pump when push the radio button

    def Mode(self, radio_mode):
        """Change the command mode (volume / pressure)"""
        if radio_mode.text() == "Mode: Volume":
            if radio_mode.isChecked() == True:
                self.label_pressure_input.setText("Volume (mL):")    #Set the text in the label
                self.PVmode = 'V'

                print("Mode volume is selected")

        if radio_mode.text() == "Mode: Pressure":
            if radio_mode.isChecked() == True:
                self.label_pressure_input.setText("Pressure (MPa):")    #Set the text in the label
                self.PVmode = 'P'

                print("Mode pressure is selected")


        if radio_mode.text() == "Mode: Displacement":
            if radio_mode.isChecked() == True:
                self.label_load_input.setText("Disp (mm):")    #Set the text in the label
                self.FDmode = 'D'

                print("Mode disp is selected")

        if radio_mode.text() == "Mode: Load":
            if radio_mode.isChecked() == True:
                self.label_load_input.setText("Load (N):")    #Set the text in the label
                self.FDmode = 'F'
                print("Mode load is selected")


    def graph_state(self, test):
        if test.text() == "Graph: On":
            self.file_save = 'dumb'
            self.running = True
            self.time_ini_graph = time.time()
        elif test.text() == "Graph: Off":
            self.running = False



    def clickMethodPause(self):
        """pause"""
        self.pause = True
        self.pump_run = False
        self.button_pause.setIcon(QIcon('ressources/button_pause_push.png'))
        self.CommandThread.stop()
        self.pause_phase()

        #Write in the savefile
        with open(self.path + '/' + self.file_save + '.txt', 'a') as mon_fichier:
            mon_fichier.write("\nPause\n\n")




    def clickMethodRestart(self):
        """restart"""

        self.button_pause.setIcon(QIcon('ressources/button_pause.png'))
        if not self.pause:
            return



        with open(self.path + '/' + self.file_save + '.txt', 'a') as mon_fichier:
            mon_fichier.write("\nEnd Pause\n\n")

        if not self.input_disp_load.text() == '':
            disp_load_target = float(self.input_disp_load.text().replace(',','.'))
        else:
            disp_load_target=''
        if not self.input_vol_pressure.text() == '':
            vol_pressure_target = float(self.input_vol_pressure.text())
        else:
            vol_pressure_target=''
        if not self.input_cycleF.text() == '':
            cycleF = float(self.input_cycleF.text())
        else:
            cycleF = 0
        if not self.input_cycleP.text() == '':
            cycleP = float(self.input_cycleP.text())
        else:
            cycleP = 0


        self.CommandThread = CommandThread(disp_load_target, vol_pressure_target, cycleF, cycleP, self.PVmode, self.FDmode)
        self.CommandThread.signal_end.connect(self.test_end)
        self.CommandThread.update_thread.connect(self.update_value)
        self.CommandThread.signal_pump_run.connect(self.pump_state)
        self.CommandThread.start()

        self.pause = False
        self.running_phase()
        # Restart the pump



    def clickMethodScan(self):
        """Scan"""
        with open(self.path + '/' + self.file_save + '.txt', 'a') as mon_fichier:
            mon_fichier.write("Scan start: " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "\n")
        print('Scan started')


    def clickMethodClearGraphs(self):

        reply = QMessageBox.question(self, 'Annihilation activated',
                         'Clear them all ?!', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.array_F = []
            self.array_P = []
            self.array_d = []
            self.array_t = []
            self.time_ini_graph = time.time()
            self.graphL.clear()
            self.graphR.clear()
            #self.clear = True
            #self.graphv.clear()
