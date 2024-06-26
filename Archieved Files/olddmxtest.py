## Property of Stavro Purdie, 2024
import platform
import os
import sys
from DMXEnttecPro import Controller

print('Heads Up!, This value affects how fast you can run your DMX adapter!')                                         
inchanmax = input('Enter how many channels you want to run (Default is 512) (Press ENTER for default) >> ')       #Ask user for how many channels they want (starts at 1)
if inchanmax == '':
    dmxchanmax = int(512)                                                                                         #Default 512 channels
    print('Default channel count of 512 used')                                                                                      
else:
    dmxchanmax = int(inchanmax)                                                                                   #Else input user value
    print(f'Channel count manually set to {dmxchanmax}')

opsys = platform.system()                                                                                         #Find out operating system

if opsys == 'Windows':
    import serial.tools.list_ports
    ports = serial.tools.list_ports.comports()
    print('COM Devices open in your PC are:')
    for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))                                                              #List open COM ports on windows 

    comport = input("Enter COM port of adapter (eg 'COM4') >> ")
    dmx = Controller(comport, auto_submit=True, dmx_size=dmxchanmax)                                               #Set COM port for windows, with auto dmx submit and size todo add COM list

if opsys == 'Linux':
    import subprocess
    command = "dmesg | grep tty"
    print('TTY Devices available are:')                                                                            #Find all Serial Devices by checking the kernal log
    output = subprocess.check_output(command, shell=True, text=True)                                               #This will output tty devices detected by kernel, in the order that they were detected and with a time stamp
    print(output)

    comport = input("Enter TTY port path of adapter (eg '/dev/ttyUSB0') >> ")
    dmx = Controller(comport, auto_submit=True, dmx_size=dmxchanmax)                                               #Set TTY port for Linux, same options as above, todo add TTY list

intimingcontrol = input("How fast do you want to send data in Hz (Recommended starting point is 40Hz, For the fastest supported by adapter press ENTER) >> ")    # Ask user for polling rate
if intimingcontrol == '':
    dmx.set_dmx_parameters(output_rate=0)
    esthz = 1,000,000 / (140 + (44 * dmxchanmax))
    print('You have selected to run your adapter at the fastest allowed speed.')                                  #Calculate and run adapter at the fastest polling rate (mathmatical relationship between channel count and Hz)
    print(f'Speed set to {esthz}Hz')
else:
    timingcontrol = int(intimingcontrol)
    dmx.set_dmx_parameters(output_rate=timingcontrol)                                                             #Else run adapter at user setting
    print(f'Speed manually set to {timingcontrol}Hz')

flag = True
while flag == True:
    chanin = input('Input channel to change (ENTER to end) >> ')
    if chanin == '':
        print('Program Exiting... Goodbye')
        quit()
    dmxchan = int(chanin)
    dmxval = int(input('Input DMX value >> '))
    dmx.set_channel(dmxchan, dmxval)