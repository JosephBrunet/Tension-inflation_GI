"""
Script for the dialog with the Arduino
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
    print(i)
    if str(i).split()[2].find('ttyACM') != -1 or str(i).find('Périphérique série USB') != -1:
        ino.port = str(i).split()[0]
        print('Arduino port found: '+ino.port)
        break



def findport():
    #Find the port of the Arduino
    for i in serial.tools.list_ports.comports():
        #print(i)
        if str(i).split()[2].find('ttyACM') != -1 or str(i).find('Périphérique série USB') != -1:
            ino.port = str(i).split()[0]
            print('Arduino port found: '+ino.port)


def CheckPort():
    print("Ports available :\n")
    for i in serial.tools.list_ports.comports():
        print(i)


def connect():
    
    if isconnected():
        return
    
    findport()
    ino.close()
    ino.open()


def disconnect():
    ino.close()


def isconnected():
    isconnected = False
    for i in serial.tools.list_ports.comports():
        if (str(i).split()[2].find('ttyACM') != -1 or str(i).find('Périphérique série USB') != -1) and ino.isOpen():
            isconnected = True
    return isconnected



def write_ino(user_input):
    ino.write(str.encode(user_input))
    #ino.send_break(duration=0.2)         # let's wait one second before reading output (let's give device time to answer)


def read_ino():
    ino.flushOutput()
    ino.flushInput()
    data_ino = ino.readline().decode("utf-8").rstrip()
    return data_ino
