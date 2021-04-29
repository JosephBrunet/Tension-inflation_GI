#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
#path = os.path.dirname(os.path.realpath(__file__))   # Find path of the python script file
#os.chdir(path)  #Change current directory


#sys.path.append(os.path.join(os.path.dirname(__file__), "modules/gui"))


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QFont, QDoubleValidator, QPixmap, QPalette, QColor, QCursor


import serial.tools.list_ports
from serial import SerialException

from tension_inflation.modules.sensors_dialogs import Arduino    #Program created to connect / read... with the arduino microcontrol
from tension_inflation.modules.sensors_dialogs import Pump_seringe   #Program to control the pump
from tension_inflation.modules.sensors_dialogs import MotorPI    #Program to control the axial motor


from tension_inflation.modules.initialisation import IniWindow
from tension_inflation.modules.mainwindow import MainWindow



class Controller:

    def __init__(self):
        pass

    def show_IniWindow(self):
        try:
            self.MainWindow.close()
        except:
            pass
        self.IniWindow = IniWindow()
        self.IniWindow.switch_window.connect(self.show_main)
        self.IniWindow.show()

    def show_main(self, path):
        self.MainWindow = MainWindow(path)
        self.MainWindow.return_window.connect(self.show_IniWindow)
        self.IniWindow.close()
        self.MainWindow.show()








def main():

    def myExitHandler():
        """Function that run when the window is stopped"""
        try:
            MotorPI.stop()
        except:
            pass
        try:
            Pump_seringe.stop()
        except:
            pass
        try:
            controller.IniWindow.timer_ini.stop()
        except:
            pass


    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(myExitHandler) # myExitHandler is a callable

#######################################################
    #Palette color for change window type and style
#######################################################

    app.setStyle("Fusion")
    #app.setStyle("Windows")
     #Fusion dark palette from https://gist.github.com/QuantumCD/6245215.
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




    controller = Controller()
    controller.show_IniWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
