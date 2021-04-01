# -*- coding: utf-8 -*-

"""

"""


import serial
import serial.tools.list_ports
import sys

ser = serial.Serial()
ser.baudrate = 19200
ser.timeout = .1



for i in serial.tools.list_ports.comports():
    print(i)
    if str(i).split()[2].find('USB-Serial') != -1:
        ser.port = str(i).split()[0]
        print('\n\nPump port: '+ser.port)

pump = 0

def test():

    connect()
    pump = find_pumps(tot_range=10)[0]
    
    getFlowRate()
    get_diameter()
    get_vol()
    
    rate = 10  # mL/min
    dia = 29  # mm
    vol = 1   # mL
    
    setFlowRate(rate)
    set_diameter(dia)
    set_vol(vol)
    
    
    run()
    stop()
    
    vol_dispensed()



def findport():      
    for i in serial.tools.list_ports.comports():
        print(i)
        if str(i).split()[2].find('USB-Serial') != -1:
            ser.port = str(i).split()[0]
            print('\n\nPump port: '+ser.port)

def connect():
    ser.open()    #We open the port
        

def isconnected():
    return ser.is_open


def disconnect():
    ser.close()



def find_pumps(tot_range=10):
    """Find the n° of the pump (in case there is several)"""
    pumps = []
    for i in range(tot_range):
        ser.write((str(i)+'ADR\x0D').encode())
        output = ser.readline()
        if len(output)>0:
            pumps.append(i)
    return pumps





def setDirection(direction):
    """Set the direction INF/WDR"""
    cmd = ''
    if direction != 'INF' and direction != 'WDR':
        sys.exit('problem with direction argument')
    frcmd = (str(pump)+'DIR'+str(direction)+'\x0D').encode()
    ser.write(frcmd)
    output = ser.readline()
#    if '?' in output.decode(): print(frcmd.decode().strip()+' from set_rate not understood')

def getDirection():
    """GEt the direction INF/WDR"""
    cmd = ''
    frcmd = (str(pump)+'DIR\x0D').encode()
    ser.write(frcmd)
    output = ser.readline()
    #if '?' in output.decode(): print(frcmd.decode().strip()+' from set_rate not understood')
    direction = output.decode()[4:-1]
    return direction




def setFlowRate(rate):
    """Set the flowrate in mL/min (units can be change, see doc)"""
    cmd = ''

    flowrate = float(rate)
    direction = 'INF'
    if flowrate<0: direction = 'WDR'
    frcmd = (str(pump)+'DIR'+str(direction)+'\x0D').encode()
    ser.write(frcmd)
    output = ser.readline()
    #if '?' in output.decode(): print(frcmd.decode().strip()+' from set_rate not understood')
    fr = abs(flowrate)
    
    cmd += str(pump)+'RAT'+str(fr)[:5]+'MM'
    cmd += '\x0D'
    cmd=cmd.encode()
    ser.write(cmd)
    output = ser.readline()
#    if '?' in output.decode(): print(cmd.decode().strip()+' from set_rates not understood')

def getFlowRate():
    """What is the flowrate ?"""
    #get direction
    cmd = (str(pump)+'DIR\x0D').encode()
    ser.write(cmd)
    try:
        output = ser.readline()
    except:
        print('function getFlowRate pump= read failed')
    sign = ''
    if output[4:7]=='WDR':
        sign = '-'
    cmd = (str(pump)+'RAT\x0D').encode()
    ser.write(cmd)
    output = ser.readline()
    output = output.decode()
    #if '?' in output: print(cmd.decode().strip()+' from get_rate not understood')
    units = output[-3:-1]
    rate = str(float(output[4:-3]))
    return sign+rate #+units




def set_diameter(dia):
    """Set the diameter of the seringe"""
    cmd = (str(pump)+'DIA'+str(dia)+'\x0D').encode()
    ser.write(cmd)
    output = ser.readline()
#    if '?' in output.decode(): print(cmd.decode().strip()+' from set_diameter not understood')

    
def get_diameter():
    """What is the diameter of the seringe set ?"""
    cmd = (str(pump)+'DIA\x0D').encode()
    ser.write(cmd)
    output = ser.readline()
    #if '?' in output.decode(): print(cmd.decode().strip()+' from get_diameter not understood')
    dia = output.decode()[4:-1]
    return dia


def set_vol(vol):
    """Give the volume to be infuse in mL"""
    vol=float(vol)
    cmd = ('0VOL'+str(vol)+'\x0D').encode()
    ser.write(cmd)
    output = ser.readline()
#    if '?' in output.decode(): print(cmd.decode().strip()+' from stop_pump not understood')

def vol_target():
    """How much the volume is set"""
    cmd = ('0VOL\x0D').encode()
    ser.write(cmd)
    output = ser.readline()
    #if '?' in output.decode(): print(cmd.decode().strip()+' from stop_pump not understood')
    vol =output.decode()[4:-1]
    if vol[-2:] == 'ML':
        vol = vol[:-2]
    else:
        sys.exit()    
    return vol



def vol_count():
    """How much the pump dispenses volume"""
    cmd = (str(pump)+'DIS\x0D').encode()
    ser.write(cmd)
    output = ser.readline()
    #if '?' in output.decode(): print(cmd.decode().strip()+' from run_all not understood')
    try:
        vol_I = output.decode()[5:10]
        vol_W =output.decode()[11:-1]
        if vol_W[-2:] == 'ML':
            vol_W = vol_W[:-2]
        else:
            sys.exit()    
        vol = float(vol_I)-float(vol_W)
    except:
        vol = 'Error'
    return vol

 
def vol_clear():
    """CLEAR VOLUME DISPENSED"""
    cmd = (str(pump)+'CLDWDR\x0D').encode()
    ser.write(cmd)
    cmd = (str(pump)+'CLDINF\x0D').encode()
    ser.write(cmd)
    ser.readline()


def run():
    """Start the pump"""
    cmd = (str(pump)+'RUN\x0D').encode()
    ser.write(cmd)
#    try:
    output = ser.readline()
#        if '?' in output.decode(): print(cmd.decode().strip()+' from run_all not understood')
#    except:
#        print('function run pump= read failed')


def stop():
    """Stop the pump"""
    cmd = (str(pump)+'STP\x0D').encode()
    ser.write(cmd)
#    output = ser.readline()
#    if '?' in output.decode(): print(cmd.decode().strip()+' from run_all not understood')


    

def dose(vol):
    """Stop the pump"""
    disconnect()
    connect()
    vol = float(vol)
    if vol < 0:
        setDirection('WDR')
        
    else:
        setDirection('INF')
    set_vol(abs(vol))
    run()



#######################################################
#All is defined, we can start the script
#######################################################

if __name__ == '__main__':
     
    connect()
    stop()
    disconnect()
    
    
    
    
    