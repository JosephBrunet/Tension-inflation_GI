from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSize, Qt, QRegExp, QThread, QThreadPool, QObject, pyqtSignal


import numpy as np    #For mathematics
import time

from tension_inflation.modules.sensors_dialogs import MotorPI    #Program to control the axial motor
from tension_inflation.modules.sensors_dialogs import Arduino    #Program created to connect / read... with the arduino microcontrol
from tension_inflation.modules.sensors_dialogs import Pump_seringe    #Program to control the pump

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
        self.flowRate = float(Pump_seringe.getFlowRate())

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
            while self.F < self.dF_target*0.9  or self.F > self.dF_target*1.1 :
                self.update_thread.emit()
                if self.F < self.dF_target*0.9:
                    MotorPI.move_rel(0.2)
                    while MotorPI.ismoving():
                        time.sleep(0.1)

                if self.F > self.dF_target*1.1:
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
                            Pump_seringe.run()
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
                        if self.P <= 10:

                            self.signal_pump_run.emit(True)
                            time.sleep(0.02)
                            Pump_seringe.stop()
                            pump_running = False
                            self.signal_pump_run.emit(False)
                            flag = True


                        if pump_running == False and flag == False:
                            self.signal_pump_run.emit(True)
                            time.sleep(0.02)
                            Pump_seringe.run_reverse()
                            #Pump_seringe.dose(-80)
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
                Pump_seringe.setFlowRate(self.flowRate)
                time.sleep(0.01)


            #MANAGE PRESSURE SUPERIOR TO TARGET
            elif self.P > self.PV_target:

                pump_running = False
                flag= False
                Pump_seringe.setFlowRate(self.flowRate)
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
                        Pump_seringe.run_reverse()
                        pump_running = True
                        time.sleep(0.02)
                        self.signal_pump_run.emit(False)
                        time.sleep(0.02)

                    self.update_thread.emit()
                    time.sleep(0.05)


        self.signal_pump_run.emit(False)
        print("QThread terminated")
        self.signal_end.emit()

