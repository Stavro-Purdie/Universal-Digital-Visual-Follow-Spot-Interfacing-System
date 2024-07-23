## Property of Stavro Purdie, 2024
## This program exists as a one time setup for your DMX Nodes
import configparser
import platform
import os
import sys
import time
from colorama import init, Fore, Style, Cursor, Back
init(autoreset=True)

print(f'{Fore.BLUE + Style.BRIGHT}Adapter Configuration Utility Starting....\n \n')
time.sleep(3)

confirm = input(f"{Fore.RED + Style.BRIGHT}WARNING! | This program resets your entire adapter config file. To continue, please type 'YES' otherwise press ENTER for exit >> \n \n")
if confirm == '':
    print(f'{Fore.GREEN}Configuration Utility Exiting, {Style.BRIGHT}No settings have been changed')
    quit()

def dmxchan():
    print(f'{Fore.BLUE}Heads Up!, This value affects how fast you can run your DMX adapter!')                                         
    inchanmax = input(f'{Fore.LIGHTYELLOW_EX}Enter how many channels you want to run (Default is 512) (Press ENTER for default) >> ')       #Ask user for how many channels they want (starts at 1)
    global dmxchanmax                                                                                                 #Make variable global
    if inchanmax == '':
        dmxchanmax = int(512)                                                                                         #Default 512 channels
        print(f'{Fore.GREEN + Style.BRIGHT}Default channel count of 512 used\n')                                                                                      
    else:
        dmxchanmax = int(inchanmax)                                                                                   #Else input user value
        print(f'{Fore.BLUE + Style.BRIGHT}Channel count manually set to {dmxchanmax}\n')                                                                                               
    return(dmxchanmax)

def serialport():
    opsys = platform.system()                                                                                         #Find out operating system

    if opsys == 'Windows':
        import serial.tools.list_ports
        ports = serial.tools.list_ports.comports()
        print(f'{Fore.YELLOW + Style.BRIGHT}COM Devices open in your PC are:')
        for port, desc, hwid in sorted(ports):
            print("{}: {} [{}]".format(port, desc, hwid))                                                              #List open COM ports on windows 

        comport = input(f"{Fore.YELLOW + Style.BRIGHT}Enter COM port of adapter (eg 'COM4') >> ")
        print('')


    if opsys == 'Linux':
        import subprocess
        command = "sudo dmesg | sudo grep tty"
        print(f'{Fore.YELLOW + Style.BRIGHT}TTY Devices available are:')                                                                            #Find all Serial Devices by checking the kernal log
        output = subprocess.check_output(command, shell=True, text=True)                                               #This will output tty devices detected by kernel, in the order that they were detected and with a time stamp
        print(output)

        comport = input(f"{Fore.YELLOW + Style.BRIGHT}Enter TTY port path of adapter (eg '/dev/ttyUSB0') >> ")
        print('')
    return(comport)
 
def dmxspeed(dmxchanmax):
    intimingcontrol = input(f"{Fore.YELLOW + Style.BRIGHT}How fast do you want to send data in Hz (Recommended starting point is 40Hz, For the fastest supported by adapter press ENTER) >> ")    # Ask user for polling rate
    if intimingcontrol == '':
        timingcontrol = int(0)
        esthz = int(1000000 / (140 + (44 * dmxchanmax)))
        print(f'{Fore.GREEN + Style.BRIGHT}You have selected to run your adapter at the fastest allowed speed.')                                  #Calculate and run adapter at the fastest polling rate (mathmatical relationship between channel count and Hz)
        print(f'{Fore.LIGHTGREEN_EX + Style.BRIGHT}Speed set to {esthz}Hz\n')
    else:
        timingcontrol = int(intimingcontrol)                                                             #Else run adapter at user setting
        print(f'{Fore.BLUE + Style.BRIGHT}Speed manually set to {timingcontrol}Hz\n')
    return(timingcontrol)


def create_config():
    opsys = platform.system()
    dmxchanmax = dmxchan()
    config = configparser.ConfigParser()
    esthz = int(1000000 / (140 + (44 * dmxchanmax)))
    config['dmxconfig'] = {'dmx_channel_count': dmxchanmax, 
                           'adapter_serial_port': serialport(), 
                            'user_adapter_speed': dmxspeed(dmxchanmax),
                            'max_dmx_adapter_speed': esthz}
    
    if opsys == 'Windows':
        os.chdir('..\\Config')
        with open('adapterconfig.ini', 'w') as configfile:
            config.write(configfile)

    if opsys == 'Linux':
        path = 'Config'
        os.chdir(path)
        with open('adapterconfig.ini', 'w') as configfile:
            config.write(configfile)
         
    time.sleep(3)
    print(f'{Fore.GREEN + Style.BRIGHT}The adapter config program has now finished.')
    print(f'{Fore.BLUE + Style.BRIGHT}If your settings change or there are any config related errors in dmxkeyboard.py, please re-run this program\n')
                          
create_config()