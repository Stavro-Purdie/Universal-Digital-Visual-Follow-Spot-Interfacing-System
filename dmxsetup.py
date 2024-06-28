## Property of Stavro Purdie, 2024
## This program exists as a one time setup for your DMX Nodes
import configparser
import platform
import os
import sys


def dmxchan():
    print('Heads Up!, This value affects how fast you can run your DMX adapter!')                                         
    inchanmax = input('Enter how many channels you want to run (Default is 512) (Press ENTER for default) >> ')       #Ask user for how many channels they want (starts at 1)
    global dmxchanmax                                                                                                 #Make variable global
    if inchanmax == '':
        dmxchanmax = int(512)                                                                                         #Default 512 channels
        print('Default channel count of 512 used')                                                                                      
    else:
        dmxchanmax = int(inchanmax)                                                                                   #Else input user value
        print(f'Channel count manually set to {dmxchanmax}')                                                                                               
    return(dmxchanmax)

def serialport():
    opsys = platform.system()                                                                                         #Find out operating system

    if opsys == 'Windows':
        import serial.tools.list_ports
        ports = serial.tools.list_ports.comports()
        print('COM Devices open in your PC are:')
        for port, desc, hwid in sorted(ports):
            print("{}: {} [{}]".format(port, desc, hwid))                                                              #List open COM ports on windows 

        comport = input("Enter COM port of adapter (eg 'COM4') >> ")


    if opsys == 'Linux':
        import subprocess
        command = "dmesg | grep tty"
        print('TTY Devices available are:')                                                                            #Find all Serial Devices by checking the kernal log
        output = subprocess.check_output(command, shell=True, text=True)                                               #This will output tty devices detected by kernel, in the order that they were detected and with a time stamp
        print(output)

        comport = input("Enter TTY port path of adapter (eg '/dev/ttyUSB0') >> ")
    return(comport)
 
def dmxspeed(dmxchanmax):
    intimingcontrol = input("How fast do you want to send data in Hz (Recommended starting point is 40Hz, For the fastest supported by adapter press ENTER) >> ")    # Ask user for polling rate
    if intimingcontrol == '':
        timingcontrol = int(0)
        esthz = int(1000000 / (140 + (44 * dmxchanmax)))
        print('You have selected to run your adapter at the fastest allowed speed.')                                  #Calculate and run adapter at the fastest polling rate (mathmatical relationship between channel count and Hz)
        print(f'Speed set to {esthz}Hz')
    else:
        timingcontrol = int(intimingcontrol)                                                             #Else run adapter at user setting
        print(f'Speed manually set to {timingcontrol}Hz')
    return(timingcontrol)

def create_config():
    dmxchanmax = dmxchan()
    config = configparser.ConfigParser()
    config['dmxconfig'] = {'dmx_channel_count': dmxchanmax, 
                           'adapter_serial_port': serialport(), 
                            'adapter_speed': dmxspeed(dmxchanmax)}

    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    
    print('The config program has now finished. Please run the dmxtest.py program')
    print('If your settings change or there are any config related errors in dmxtest.py, please re-run this program')

if __name__ == "__main__":                                                                                    #This if statement only runs the program if it is manually ran.
    create_config()
