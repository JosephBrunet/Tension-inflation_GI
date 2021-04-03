"""
Script for the dialog with the Motor
"""

import sys
from pipython import pitools
from pipython import GCSDevice
from pipython import gcscommands

import serial
import serial.tools.list_ports


pi_device = GCSDevice ('C-863.11')       #Create object

#Vis
p = 5 #pas (mm)




#Find the port of the Motor
for i in serial.tools.list_ports.comports():
    #print(i)
    if str(i).split()[2].find('US232') != -1:
        port = str(i).split()[0]
        print('Motor port: '+port)
#port = "/dev/ttyUSB0"


def findport():
    for i in serial.tools.list_ports.comports():
        #print(i)
        if str(i).split()[2].find('US232') != -1:
            port = str(i).split()[0]
            print('Motor port: '+port)



def connect():
    """Function to connect the object with the computer"""
    for i in serial.tools.list_ports.comports():
        #print(i)
        if str(i).split()[2].find('US232') != -1:
            port = str(i).split()[0]
            print('Motor port: '+port)


    pi_device.ConnectRS232(comport=port, baudrate=115200) #Connection by RS232
    pi_device.SVO (pi_device.axes,1)     # Turn on servo control of axis first axes
    print('connected: {}'.format(pi_device.qIDN().strip()))
    print('\nConnection succeed !!')

def disconnect():
    """Function to disconnect the device"""
    pi_device.CloseConnection()    #Close the connection with device

def isconnected():
    return pi_device.IsConnected()


def ref():
    """Function to set the reference of the device"""
    if pi_device.qRON(pi_device.axes):
        pi_device.RON(pi_device.axes,False)
    pi_device.POS(pi_device.axes,0)
    #gcscommands.GCSCommands.FRF(pi_device,pi_device.axes)   #Set ref position
    #pitools.waitontarget(pi_device)    #Time to the device to find ref
    if gcscommands.GCSCommands.qFRF(pi_device,pi_device.axes)[pi_device.axes[0]] != True:   #Check if the ref is set
        print('Error: Axis has no reference')
        sys.exit("Error ref")
    else:
        print('Reference set !')



def vel(v):
    p = 5
    v_deg = (v /60)*(360 / p)
    pi_device.VEL(pi_device.axes[0],values= v)     #Set the velocity

def vel_value():
    return pi_device.qVEL(pi_device.axes)['1']


def move(L):
    """Move the motor to an absolute location"""
    # L=(p*a)/ (2*pi)
    # L : Longueur parcourue (m)
    # p : pas (m)
    # a : angle (rad)

    # L = (p * deg)/360

    # 4 mm/ tr selon Nico
    p = 5
    deg = - 360 * L / p    #Calcul du nombre de degrés
    pi_device.MOV (pi_device.axes, deg)     # Command first axis to position deg

    #pitools.waitontarget(pi_device)   #Wait that the displacement is finished
    #positions = pi_device.qPOS(pi_device.axes)             # Query current position of first axis
    #print('Position of motor (deg){} = {:.2f}'.format('', positions[pi_device.axes[0]]))       #Print the position


def move_rel(L):
    """Move the motor of a relative displacement"""

    # L=(p*a)/ (2*pi)
    # L : Longueur parcourue (m)
    # p : pas (mm)
    # a : angle (rad)

    # L = (p * deg)/360

    # 4 mm/ tr selon Nico
    p = 5
    deg = - 360 * L / p    #Calcul du nombre de degrés
    pi_device.MVR (pi_device.axes, deg)     # Command first axis to position deg

    #pitools.waitontarget(pi_device)   #Wait that the displacement is finished
    #positions = pi_device.qPOS(pi_device.axes)             # Query current position of first axis
    #print('Position of motor (deg){} = {:.2f}'.format('', positions[pi_device.axes[0]]))       #Print the position


def motor_pos():
    """Return the position of the motor"""
    pos = - pi_device.qPOS(pi_device.axes)['1'] * p / 360             # Query current position of first axis
    return pos

def ismoving():
    return not pi_device.qONT()[pi_device.axes[0]]


def stop():
    try:
        pi_device.STP() #Halt the motion of given 'axes' smoothly.
    except:
        pass
    #pi_device.HLT(pi_device.axes) #Halt the motion of given 'axes' smoothly.
