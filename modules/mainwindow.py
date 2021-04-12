
import os
import os.path
#path = os.getcwd()

import sys
import time

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton, QAction, QStatusBar, QFormLayout, QLabel, QLineEdit,
    QVBoxLayout, QHBoxLayout, QSpacerItem, QMessageBox, QFrame, QSizePolicy, QInputDialog, QGroupBox, QRadioButton, QFileDialog,QDesktopWidget)
from PyQt5.QtCore import QSize, Qt, QThread, QThreadPool, QObject, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QDoubleValidator, QPixmap, QPalette, QColor, QCursor

import serial.tools.list_ports
from serial import SerialException

from modules.sensors_dialogs import Arduino    #Program created to connect / read... with the arduino microcontrol
from modules.sensors_dialogs import Pump_seringe    #Program to control the pump
from modules.sensors_dialogs import MotorPI    #Program to control the axial motor


from modules.mainwindow_modules.Left_panel import *
from modules.mainwindow_modules.Right_panel import *
from modules.mainwindow_modules.CommandThread import CommandThread

from simple_pid import PID

import numpy as np    #For mathematics
import pyqtgraph as pg    #Library to plot graph with pyqt


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
        print("Problem read arduino function")

    return data



##############################################################################################################
##############################################################################################################
##############################################################################################################




class ReadThread(QThread):

    job_done = pyqtSignal(object)

    def __init__(self):
        super(QThread, self).__init__()


    def run(self):
        try:
            val = read()
            self.job_done.emit(val)
        except:
            print("ReadThread run problem")


##############################################################################################################
##############################################################################################################
##############################################################################################################


class MainWindow(QMainWindow, Left_panel, Right_panel):    #Definition of the graphical interface (GI) class

    return_window = QtCore.pyqtSignal()


    def __init__(self, path):   #Initiation: It's in there that we create all the widgets needed in our window

        super(MainWindow, self).__init__()

        self.path = path
        self.tare_disp = 0
        self.vol = 0
        self.F = 0
        self.P = 0
        self.secu = 0
        self.pause = False
#        self.clear = False
        self.pump_run = False
        self.c = 0


        self.array_F = []
        self.array_P = []
        self.array_d = []
        self.array_t = []

        self.Lxaxis = "Pressure (mmHg)"
        self.Lyaxis = "Force (N)"
        self.Rxaxis = "Time (s)"
        self.Ryaxis = "Pressure (mmHg)"

        self.time_ini = time.time()     #Save the start time

        try:
            Pump_seringe.setFlowRate(5)
        except SerialException:
            print('pump setflow problem')

        self.ReadThread = ReadThread()
        self.ReadThread.job_done.connect(self.on_job_done)

        QMainWindow.__init__(self)


        #self.setMinimumSize(QSize(1000, 500))
        self.setWindowTitle("Command Panel")     # set window title1
        #self.setMinimumSize(800, 800);
        self.setStyleSheet("background-color: gray;")   #Background color

        self.centralWidget = QWidget()    # Create a central Widgets (It's a big widget that contains all others and the we will assign to the window)
        centralLayout = QHBoxLayout()    # Create a Layout for the central Widget



        #Put window in center
        fg = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        self.move(fg.topLeft())



        self.setup_left_panel(self)
        self.setup_right_panel(self)

        self.positioning_phase()

#######################################################
        #Create all the widgets

        #Create label: running or stopped state
        self.label_left_bot = QLabel()    #Creation of the widget
        self.label_left_bot.setText("  ")    #Set the text in the label
        self.label_left_bot.setAlignment(Qt.AlignCenter)   #Alignement of the label (here it's the vertical alignement)
        self.label_left_bot.setFont(QFont("Arial",16,QFont.Bold))    #Set the writing font with the size
        self.label_left_bot.setStyleSheet("background-color: red;")



        self.statusBar = QStatusBar()        #Create object statusbar
        self.setStatusBar(self.statusBar)      #Activate statue bar

########################################
        '''
        INFORMATION

        "self.something" means that "something" is an atribute of the class
        if you don't put "self." the variable or method will only be local)
        '''

#######################################################
        #Set the Timer and Thread
#######################################################

        self.running = False
        self.pump_run = False

        #Start thread and timer for positioning

        self.timer = QtCore.QTimer()    #Set the timer
        self.timer.timeout.connect(self.update_window)
        self.timer.start(70)    #Start the timer with clocking of 70 ms

#######################################################
        #Def menubar
#######################################################

        menuBar = self.menuBar()   #Creation of the menubar


#############
        #Def port definition
        fileMenu = menuBar.addMenu('&File')

        changeFileAction = QAction('&TEST', self)
        changeFileAction.triggered.connect(self.Test_call)    #Call the fonction when this action is selected
        fileMenu.addAction(changeFileAction)    #Put the new action in the item

        changeFileAction = QAction('&Change working directory', self)
        changeFileAction.setStatusTip('Change working directory')
        changeFileAction.triggered.connect(self.ChangeDir)    #Call the fonction when this action is selected
        fileMenu.addAction(changeFileAction)    #Put the new action in the item

        changeFileAction = QAction('&Initialisation', self)
        changeFileAction.setStatusTip('Initialisation')
        changeFileAction.triggered.connect(self.Ini)    #Call the fonction when this action is selected
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
        PumpPortAction = QAction('&Watson-Marlow Pump', self)
        PumpPortAction.setStatusTip('Define the serial ports of the PI motor')
        PumpPortAction.triggered.connect(self.PumpPortCall)    #Call the fonction when this action is selected
        chooseMenu.addAction(PumpPortAction)    #Put the new action in the item


        InoPortAction = QAction('&Arduino', self)
        InoPortAction.setStatusTip('Define the serial port of the arduino')
        InoPortAction.triggered.connect(self.InoPortCall)    #Call the fonction when this action is selected
        chooseMenu.addAction(InoPortAction)    #Put the new action in the item

        TestConnectionAction = QAction('&Test connections', self)
        TestConnectionAction.setStatusTip('')
        TestConnectionAction.triggered.connect(self.TestConnectionCall)    #Call the fonction when this action is selected
        portMenu.addAction(TestConnectionAction)    #Put the new action in the item



#############
        #Def pump
        pump_menu = menuBar.addMenu("&Pump")

        vel_p_action = QAction("&Change Flow velocity", self)
        vel_p_action.setStatusTip('Change flow velocity')  # Hungry!
        vel_p_action.triggered.connect(self.VelPumpCall)
        pump_menu.addAction(vel_p_action)




#############
        #Def motor
        motor_menu = menuBar.addMenu("&Motor")

        vel_m_action = QAction("&Change Motor speed", self)
        vel_m_action.setStatusTip('Change motor speed')  # Hungry!
        vel_m_action.triggered.connect(self.VelMotorCall)
        motor_menu.addAction(vel_m_action)


#############
        #Def graph
        graph_menu = menuBar.addMenu("&Graph")


        LgraphMenu = graph_menu.addMenu('&Left graph')


        Lx_action = QAction("&Change x axis", self)
        Lx_action.setStatusTip('Change x axis')  # Hungry!
        Lx_action.triggered.connect(self.LxAxisCall)
        LgraphMenu.addAction(Lx_action)

        Ly_action = QAction("&Change y axis", self)
        Ly_action.setStatusTip('Change y axis')  # Hungry!
        Ly_action.triggered.connect(self.LyAxisCall)
        LgraphMenu.addAction(Ly_action)

        RgraphMenu = graph_menu.addMenu('&Right graph')

        Rx_action = QAction("&Change x axis", self)
        Rx_action.setStatusTip('Change x axis')  # Hungry!
        Rx_action.triggered.connect(self.RxAxisCall)
        RgraphMenu.addAction(Rx_action)

        Ry_action = QAction("&Change y axis", self)
        Ry_action.setStatusTip('Change y axis')  # Hungry!
        Ry_action.triggered.connect(self.RyAxisCall)
        RgraphMenu.addAction(Ry_action)


#############
        #Def help
        help_menu = menuBar.addMenu("&Help")


        about_action = QAction("&Only when u\'re desesperate", self)
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

        #QMessageBox.about(self, "2nd step:", "Place your sample correctly and tare the sensors\n\nOnce it's done, clic on 'Positioning finished'")



#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------

#######################################################
        # Def functions
#######################################################
    def Test_call(self):

        print('start test')

        self.Radio_graphOFF.setChecked(True)
        self.graph_state(self.Radio_graphOFF)
        print('end test')






    def ChangeDir(self):


        self.path = str(QFileDialog.getExistingDirectory(self, "Select Directory")) #Choose a path
        print(self.path)


    def Ini(self):

        """Function to change directory"""
        msg = QMessageBox.question(self,"Continue ?","Do you want to start the initialisation ?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if msg == QMessageBox.No:
            return

        self.timer.stop()
        self.return_window.emit()


    def ShowPortCall(self):
        """Function to show in a window the different ports open"""
        ports = ""

        if Pump_seringe.ser.port is None:
            Pump_seringe.ser.port = "Not Define"
        ports = ports + "Pump:   " + Pump_seringe.ser.port + "\n"

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

    def TestConnectionCall(self):
        #######################################################
        ## CONNECTION WITH ARDUINO/PUMP/MOTOR

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
            #MotorPI.ref()
        except:
            print("Can't connect to motor")
        if MotorPI.isconnected():
            msg += "Motor: Connected\n"
        else:
            msg += "Motor: Not connected\n"


        QMessageBox.about(self, "Connections", msg)



    def LxAxisCall(self):

        item, ok = QInputDialog.getItem(self, "Left graph","Which x axis:", ["Displacement (mm)","Force (N)","Pressure (mmHg)", "Time (s)"], 0, False)

        if ok:
            self.Lxaxis = item

            self.graph1.setLabel('bottom', item)

    def LyAxisCall(self):

        item, ok = QInputDialog.getItem(self, "Left graph","Which y axis:", ["Displacement (mm)","Force (N)","Pressure (mmHg)", "Time (s)"], 0, False)

        if ok:
            self.Lyaxis = item
            self.graph1.setLabel('left', item)

    def RxAxisCall(self):

        item, ok = QInputDialog.getItem(self, "Right graph","Which x axis:", ["Displacement (mm)","Force (N)","Pressure (mmHg)", "Time (s)"], 0, False)

        if ok:
            self.Rxaxis = item
            self.graph2.setLabel('bottom', item)

    def RyAxisCall(self):

        item, ok = QInputDialog.getItem(self, "Right graph","Which y axis:", ["Displacement (mm)","Force (N)","Pressure (mmHg)", "Time (s)"], 0, False)

        if ok:
            self.Ryaxis = item
            self.graph2.setLabel('left', item)



    def helpCall(self):
        QMessageBox.about(self, "Tip", "Call me if you have questions :\nJoseph Brunet\njoseph.brunet@emse.fr")



    def VelPumpCall(self):
        """Change the pump flow rate"""
        try:
            default_value = Pump_seringe.getFlowRate()
            text, okPressed = QInputDialog.getText(self, "Set flow rate","Flow Rate (mL/min) :", QLineEdit.Normal, default_value)
            if okPressed and text != '':
                try:
                    Pump_seringe.setFlowRate(text)
                except SerialException:
                    QMessageBox.about(self, "WARNING:", "The pump is not connected\n(check the serial ports)")
        except:
            print("Error VelPumpCall")


    def VelMotorCall(self):
        """Change the motor rotation speed"""
        text, okPressed = QInputDialog.getText(self, "Set motor speed","Motor speed (mm/min) :", QLineEdit.Normal, "")
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
        if not Arduino.isconnected():
            QMessageBox.about(self, "WARNING:", "The arduino is not connected\n(check the serial ports)")
            return

        self.Radio_graphOFF.setChecked(True)
        self.graph_state(self.Radio_graphOFF)
        self.array_F = []
        self.array_P = []
        self.array_d = []
        self.array_t = []
        self.graphL.clear()
        self.graphR.clear()

        ############
        #Test if the programm is already running
        if self.running:   #Avoid problem if user push several time the start button
            print("Already running !!")
            return


        ############################################################################
        ############################################################################


        items = ["rad","long","circ"]
        item, ok = QInputDialog.getItem(self, "Serial ports","Which serial port pump connected:", items, 0, False)

        direction = item



        #Saving file
        header ="\n"+str(direction)+"\nTime , Disp, Load , Pressure, Volume\n"

        if self.input_sample.text():
            msg = QMessageBox.question(self,"Sample name","Sample name: '"+ self.input_sample.text() + "' ?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if msg == QMessageBox.Yes:
                self.file_save = self.input_sample.text()

                if not os.path.exists(self.input_sample.text() + ".txt"):
                    self.file_save = self.input_sample.text()
                    with open(self.path + '/' + self.file_save + '.txt', 'a') as mon_fichier:     #Initialize the saving file
                        mon_fichier.write(self.file_save + header)

                else:
                    msg = QMessageBox.question(self,"WARNING: File already exist","Do you want to replace it ?",
                                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    if msg == QMessageBox.Yes:
                        self.file_save = self.input_sample.text()
                        with open(self.path + '/' + self.file_save + '.txt', 'w') as mon_fichier:     #Initialize the saving file
                            mon_fichier.write(self.file_save + header)
                    else:
                        return
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
                        with open(self.path + '/' + self.file_save + '.txt', 'a') as mon_fichier:     #Initialize the saving file
                            mon_fichier.write(self.file_save + "\nNew run\nTime , Disp, Load , Pressure, Volume\n")
                        break

                    else:
                        msg = QMessageBox.question(self,"WARNING: File already exist","Do you want to replace it ?",
                                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        if msg == QMessageBox.Yes:
                            self.file_save = text
                            with open(self.path + '/' + self.file_save + '.txt', 'w') as mon_fichier:     #Initialize the saving file
                                mon_fichier.write(self.file_save + "\nNew run\nTime , Disp, Load , Pressure, Volume\n")
                            break
                else:
                    return

        ############################################################################
        ############################################################################

        self.running = True   # Set the variable to running


        self.graphL.clear()
        self.graphR.clear()
        ############


        self.label_state.setText(" Running ")     #Show the runing state
        self.label_state.setStyleSheet("background-color: green;")    #Put the background color in green
        self.inibutton.setIcon(QIcon('ressources/button_start_push.png'))   #Change the button's icon by the ressources

        self.time_ini = time.time()     #Save the start time
        self.time_ini_graph  = time.time()     #Save the start time

        #----------------------------------------------------------------------
        #----------------------------------------------------------------------
        ## Run the motor to the targeted distance
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

        self.running_phase()



    def update_value(self):
        self.CommandThread.update_value(self.F,self.P)

    def pump_state(self, test):
        self.pump_run = test


    def test_end(self):
        """Method to stop the acquisition"""

        if not self.pause:

            self.pause = True
            self.CommandThread.stop()
            self.pause_phase()
            QMessageBox.about(self, "Ending", "Test finished\nWaiting for Stop or Restart button")
#            self.running = False
#            self.positioning_phase()
#
#            self.label_state.setText(" Stopped ")
#            self.label_state.setStyleSheet("background-color: red;")
#
#            self.label_phase.setText("Phase: Positioning")
#            #QMessageBox.about(self, "Test", "Test finished. Positionning phase started")



    def clickMethodStop(self):
        """Method to stop the acquisition"""

        self.running = False
        self.pump_run = False
        self.button_pause.setIcon(QIcon('ressources/button_pause.png'))
        self.inibutton.setIcon(QIcon('ressources/button_start_push.png'))   #Change the button's icon by the ressources
        self.positioning_phase()

        self.label_state.setText(" Stopped ")
        self.label_state.setStyleSheet("background-color: red;")
        self.label_phase.setText("Phase: Positioning")
        self.pause = False
        try:
            self.CommandThread.stop()
        except:
            print("problem CommandThread.stop()")
        MotorPI.stop()
        Pump_seringe.stop()

        QMessageBox.about(self, "Test", "Positionning phase")

















    def on_job_done(self, generated_obj):
        try:
            [self.secu,self.ori,self.F,self.P] = generated_obj
        except:
            print("error on job done")

    def on_jobVol_done(self, generated_obj_vol):
        self.vol = generated_obj_vol





    def update_window(self):
        """Method called each time the timer clocks"""
        
        self.connectionCall()  #Method to check the connection of the devices (method in "Left_panel")

        try:
            #[self.secu,self.ori,self.F,self.P] = read()    #Method to save current value of load and pressure
            self.ReadThread.start()
        except:
            print("ReadThread pb")
        self.vol=0

#
        try:
            self.d = MotorPI.motor_pos()

            if self.d < -50.1:
                self.clickMethodStop()
                MotorPI.move_rel(1)
                QMessageBox.about(self, "Warning", "The end course was reached")

            self.label_disp_abs_display.setText("Abs: "+str(round(self.d,2))+" mm")   #Display the value
            self.label_disp_rel_display.setText(str(round((self.d-self.tare_disp),2)) + " mm")   #Display the value
        except:
            print("Problem MotorPI.motor_pos() in update()")

        self.label_pressure_display.setText(f"{self.P:.3f} mmHg")   #Display the value
        self.label_volume_display.setText(str(round(self.vol,4)) + " ml")   #Display the value
        self.label_load_display.setText(f"{self.F:.3f} N")   #Display the value




        if self.secu == 1:

            self.clickMethodStop()

            msg = QMessageBox.question(self,"Arret d'urgence ou Fin de course !","Did you push the emergency stop button ?",
                                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if msg == QMessageBox.No:
                QMessageBox.about(self, "Warning", "The end course was activated, you have to move the motor manually and restart the initialisation")
                self.timer.stop()
                self.return_window.emit()
            else:

                try:
                    [self.secu,self.ori,self.F,self.P] = read()    #Method to save current value of load and pressure
                except:
                    print("Read problem")
                while self.secu == 1:
                    QMessageBox.about(self, "Warning", "Un-push the emergency stop button")
                    try:
                        [self.secu,self.ori,self.F,self.P] = read()    #Method to save current value of load and pressure
                    except:
                        pass
                MotorPI.connect()
                return




        #------------------------------------------------------------------
        ## This part is activate when the user start the machanical test
        #------------------------------------------------------------------


        if not self.running:
            return

        self.time_now = time.time() - self.time_ini_graph    #Save the timepassed since the starting time
        #####################
        #Graphic update

        if not self.time_now or self.F or self.P :       #If value are null don't show on graph (because at the beginning values null)
            #xv = np.array([self.time_now])

            self.array_F.append(float(self.F))
            self.array_P.append(float(self.P))
            self.array_d.append(float(self.d-self.tare_disp))
            self.array_t.append(float(self.time_now))

            if self.Lxaxis == "Displacement (mm)":
                Lx = self.array_d
            elif self.Lxaxis == "Force (N)":
                Lx = self.array_F
            elif self.Lxaxis == "Pressure (mmHg)":
                Lx = self.array_P
            elif self.Lxaxis == "Time (s)":
                Lx = self.array_t

            if self.Lyaxis == "Displacement (mm)":
                Ly = self.array_d
            elif self.Lyaxis == "Force (N)":
                Ly = self.array_F
            elif self.Lyaxis == "Pressure (mmHg)":
                Ly = self.array_P
            elif self.Lyaxis == "Time (s)":
                Ly = self.array_t

            if self.Rxaxis == "Displacement (mm)":
                Rx = self.array_d
            elif self.Rxaxis == "Force (N)":
                Rx = self.array_F
            elif self.Rxaxis == "Pressure (mmHg)":
                Rx = self.array_P
            elif self.Rxaxis == "Time (s)":
                Rx = self.array_t

            if self.Ryaxis == "Displacement (mm)":
                Ry = self.array_d
            elif self.Ryaxis == "Force (N)":
                Ry = self.array_F
            elif self.Ryaxis == "Pressure (mmHg)":
                Ry = self.array_P
            elif self.Ryaxis == "Time (s)":
                Ry = self.array_t

            self.graphL.setData(Lx,Ly)    #Show on the graph

            self.graphR.setData(Rx,Ry)    #Show on the graph

            #####################
        # Result file update

        with open(self.path + '/' + self.file_save + '.txt', 'a') as mon_fichier:
            mon_fichier.write(str(round(time.time()-self.time_ini,2)) + " , " + str(round(self.d-self.tare_disp,3)) + " , " + str(self.F) + " , " + str(self.P) + " , " + str(self.vol) + "\n")
        #####################
        # Pessure mode update
#        if self.pump_run:
#            if self.mode == "pressure" and self.target_pressure < float(self.P) :
#                    Pump_seringe.stop()
#                    self.pump_run = False

    def closeEvent(self, event):
        print("Close event")
        reply = QMessageBox.question(self, 'Message',"Are you sure to quit?", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            self.timer.stop()
            #sys.exit("end")
        else:
            event.ignore()


