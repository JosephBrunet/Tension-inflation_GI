# -*- coding: utf-8 -*-

"""
Mode that control the pump Watson Marlow 530 DuN through the serial port RS485
"""

doc = ('------------------------------------------------------------------------------------------\n'
     'DOC :\n'
     '------------------------------------------------------------------------------------------\n\n'
     '    Protocol to command the pump :\n\n\n'
     'CA - Clear LCD display\n\n'
    'CH - Home the cursor\n\n'
    'DO Num1, or Num1,Num2 Set and run one dose of Num1 tacho pulses. Note that "Num2",\n\n'
        'is optional and specifies the number of drip tacho pulses (maximum 11000) (see Note 2)\n\n'
    'TC - Clear the cumulative tachometer count\n\n'
    'SP Num1 or Num1,Num2 Set speed to Num1 RPM (Range 0.1 - 999.9 in steps of 0.1)\n\n'
    'SI - Increment the speed by 1 RPM\n\n'
    'SD - Decrement the speed by 1 RPM\n\n'
    'GO - Start running\n\n'
    'ST - Stop running\n\n'
    'RC - Change direction\n\n'
    'RR - Set direction to clockwise\n\n'
    'RL - Set direction to counter-clockwise\n\n'
    'RS - Return status (see Note 3)\n\n'
    'RT - Return the total deci pump revolutions count\n\n'
    'W "Line1","Line2","Line3","Line4", Display text on 1 to 4 lines (lines 2,3 and 4 are optional so that between 1 and 4 lines can be displayed).\n' 
        'The text must be enclosed by a comma, as shown. The allowable characters are: \n'
        '! # % \' ( ) + , - . / 0 1 2 3 4 5 6 7 8 9 :; < = > ? A B C D E F G H I J K L M N O P Q R S T U V W X Y Z a b c d e f g h i j k l m n o p q r s t u v w x y z\n\n'
    'ZY - Return ) for stopped or 1 for running. This is returned to the sender in the following format: SOM, address, ) or 1, checksum, EOM e.g. <1,0,47>)\n\n'
    
    '------------------------------------------------------------------------------------------\n'
    'Commandes :\n'
    '------------------------------------------------------------------------------------------\n\n'
    '<number of pump, command above, parameters x N, ??> - Generic command to control the pump\n\n'
    )

import serial
import serial.rs485
import serial.tools.list_ports

import time


#configure the serial connections (the parameters differs on the device you are connecting to)
pump = serial.rs485.RS485()
#pump.port = '/dev/ttyUSB0'
pump.baudrate = 19200
pump.parity=serial.PARITY_NONE
pump.stopbits=serial.STOPBITS_TWO
pump.bytesize=serial.EIGHTBITS
pump.timeout = 5    #Wait until the timeout is finished and return all bytes that were received until then

pump.rs485_mode = serial.rs485.RS485Settings(
        rts_level_for_tx=True, 
        rts_level_for_rx=False, 
        loopback=False, 
        delay_before_tx=None, 
        delay_before_rx=None)



for i in serial.tools.list_ports.comports():
    #print(i)
    if str(i).split()[2].find('CP2102') != -1:
        pump.port = str(i).split()[0]
        print('Pump port: '+pump.port)




def findport():      
    for i in serial.tools.list_ports.comports():
        #print(i)
        if str(i).split()[2].find('CP2102') != -1:
            pump.port = str(i).split()[0]
            print('Pump port: '+pump.port)



def connect():
    
    for i in serial.tools.list_ports.comports():
        #print(i)
        if str(i).split()[2].find('CP2102') != -1:
            pump.port = str(i).split()[0]
            print('Pump port: '+pump.port)
    
    if pump.port is None:
        print("Pump serial port is not defined")
        
    else:
        if pump.is_open:     #We verify that the port is closed, if not we close it
            pump.close()
        pump.open()    #We open the port
        

def isconnected():
    return pump.is_open


def disconnect():

    pump.close()





def start():
    

    user_input = "<1,GO,??>"
    pump.write(str.encode(user_input))


def stop():
    

    user_input = "<1,ST,??>"
    pump.write(str.encode(user_input))


def setFlowRate(user_input):
    

    user_input = str(float(user_input.replace(',','.')))
    
    user_input = "<1,SP," + user_input + ",??>"
    pump.write(str.encode(user_input))





def dose(vol):
    #  0.0017566 ml/tacho
    
    user_input = "<1,RL,??>"
    pump.write(str.encode(user_input))
    time.sleep(0.2)
    
    if vol >= 0:
        Ntacho = vol / 0.0017566
        Ntacho = round(Ntacho)
        user_input = "<1,DO,"+str(Ntacho)+",??>"
        pump.write(str.encode(user_input))
    else:
        vol = - vol
        ChangeDir()
        Ntacho = vol / 0.0017566
        Ntacho = round(Ntacho)
        user_input = "<1,DO,"+str(Ntacho)+",??>"
        #print(user_input)
        time.sleep(0.2)
        pump.write(str.encode(user_input))




def isrunning():
    user_input = "<1,ZY,??>"
    pump.write(str.encode(user_input))
    time.sleep(0.05)
    run = pump.read_all().decode()
    if run == '':
        return 'noRes'
    else:
        run = run.split(',')[1]
    return int(run)


def ChangeDir():
    user_input = "<1,RC,??>"
    pump.write(str.encode(user_input))






















    #################
    #  INFO:  14.62 mL / tr
    #################
#
#def dose(vol):
#    """thread worker function"""
#    stop_dose = False
#
#    setFlowRate(str(velocity))
#
#    start_time = time.time()
#    
#    start()
#    
#    delay = (vol / (velocity * flow))*60
#    delay=vol
#    for i in range(100):
#        time.sleep(delay/100)
#        if stop_dose:
#            return
#    
#    stop()
#
#    print("--- %s seconds ---" % (time.time() - start_time))
#
#    print('Finish!')
#    return
#
#













