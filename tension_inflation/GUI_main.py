#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This script is the main script of the application launching first the initialisation and then the test window
"""

import os, sys
from pathlib import Path

#Configure path for fontconfig for Ubuntu user (solve problems caused by pyinstaller)
if os.path.exists("/etc/fonts/fonts.conf"):
	os.environ['FONTCONFIG_FILE'] = '/etc/fonts/fonts.conf'
	os.environ['FONTCONFIG_PATH'] = '/etc/fonts/'


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QFont, QDoubleValidator, QPixmap, QPalette, QColor, QCursor


import serial.tools.list_ports
from serial import SerialException

from tension_inflation.modules.sensors_dialogs import Arduino    #Program created to connect / read... with the arduino microcontroller
from tension_inflation.modules.sensors_dialogs import Pump_seringe   #Program to communicate with the pump
from tension_inflation.modules.sensors_dialogs import MotorPI    #Program to communicate with the axial motor


from tension_inflation.modules.initialisation import IniWindow  
from tension_inflation.modules.mainwindow import MainWindow



class Controller:
    """
    Class defining the different steps of the application
    """
    def __init__(self):
        pass

    def show_IniWindow(self):
        try:
            self.MainWindow.close()
        except:
            pass
        self.IniWindow = IniWindow()
        self.IniWindow.switch_window.connect(self.show_main)  #Pass to show_main when IniWindow is finished
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

#######################################################
    
    controller = Controller()   #Initialise the class
    controller.show_IniWindow()   #Start the initialisation
    sys.exit(app.exec_())


if __name__ == '__main__':

    main()
