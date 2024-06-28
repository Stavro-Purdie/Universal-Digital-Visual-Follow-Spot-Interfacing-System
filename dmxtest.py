## Property of Stavro Purdie, 2024
import platform
import os
import sys
import configparser
from DMXEnttecPro import Controller

def read_config():
    config = configparser.ConfigParser()    #INIT section: create a configparser object & read file
    config.read('config.ini') 

    dmxchanmax = config.get('dmxconfig', 'dmx_channel_count') #READ section: access all of the config settings
    serialport = config.get('dmxconfig', 'adapter_serial_port')
    adatspeed = config.get('dmxconfig', 'adapter_speed')

    config_values = {                                                   #Export our config values in a nice dictionary for easy upgradibility
        'dmxchanmax': dmxchanmax,   
        'serialport': serialport,
        'adatspeed': adatspeed,
    }
    return(config_values)

config_data = read_config()                                         #Read our data
dmxchanmax = int(config_data['dmxchanmax'])                         #Now we need to assign our config to variables
serialport = config_data['serialport']
adatspeed = int(config_data['adatspeed'])

print('Loaded Settings:')
print(f'DMX Channels in use: {dmxchanmax}')
print(f'Serial Port selected: {serialport}')
print(f'Adapter Data Rate: {adatspeed}')

dmx = Controller(serialport, auto_submit=True, dmx_size=dmxchanmax)   #Now to run our setup code
dmx.set_dmx_parameters(output_rate=adatspeed)

flag = True
while flag == True:
    chanin = input('Input channel to change (ENTER to end) >> ')
    if chanin == '':
        print('Program Exiting... Goodbye')
        quit()
    dmxchan = int(chanin)
    dmxval = int(input('Input DMX value >> '))
    dmx.set_channel(dmxchan, dmxval)