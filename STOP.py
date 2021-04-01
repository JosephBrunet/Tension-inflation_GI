#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 11:42:09 2020

@author: utilisateur
"""


import Pump_seringe   #Program to control the pump
import MotorPI 
import time

Pump_seringe.disconnect()
Pump_seringe.connect()

try:
    MotorPI.stop()
except:
    pass
try:
    Pump_seringe.stop()
except:
    pass