# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 11:23:54 2018

@author: joseph.brunet
"""


import sys
import serial
from serial import SerialException
import serial.tools.list_ports


# configure the serial connections (the parameters differs on the device you are connecting to)
ino = serial.Serial()
#ino.port = '/dev/ttyACM0'
ino.baudrate = 115200
ino.timeout = 3

for i in serial.tools.list_ports.comports():
    #print(i)
    if str(i).split()[2].find('ttyACM') != -1:
        ino.port = str(i).split()[0]
        print('Arduino port: '+ino.port)



def findport():      
    for i in serial.tools.list_ports.comports():
        #print(i)
        if str(i).split()[2].find('ttyACM') != -1:
            ino.port = str(i).split()[0]
            print('Arduino port: '+ino.port)
        
        
def CheckPort():

    print("Ports available :\n")
    for i in serial.tools.list_ports.comports():
        print(i)

def connect():
    
    for i in serial.tools.list_ports.comports():
        #print(i)
        if str(i).split()[2].find('ttyACM') != -1:
            ino.port = str(i).split()[0]
            print('Arduino port: '+ino.port)
    
    
    ino.close()
    ino.open()


def disconnect():
    
    ino.close()

def isconnected():
    
    return ino.isOpen()
    


def write_ino(user_input):

    ino.write(str.encode(user_input))
    
    #ino.send_break(duration=0.2)         # let's wait one second before reading output (let's give device time to answer)
    

def read_ino():
    
    
    ino.flushOutput()
    ino.flushInput()
    data_ino = ino.readline().decode("utf-8").rstrip()
    return data_ino




if __name__ == '__main__':
   #CheckPort()
   pass


##  ino.reset_input_buffer()      #Flush input buffer, discarding all its contents.
