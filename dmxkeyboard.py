## Property of Stavro Purdie, 2024
import configparser
from DMXEnttecPro import Controller
import time
import json
from pynput.keyboard import Listener, Key

def adapter_config():
    config = configparser.ConfigParser()    #INIT section: create a configparser object & read file
    config.read('adapterconfig.ini') 

    dmxchanmax = config.get('dmxconfig', 'dmx_channel_count') #READ section: access all of the config settings
    serialport = config.get('dmxconfig', 'adapter_serial_port')
    adatspeed = config.get('dmxconfig', 'user_adapter_speed')
    autoadatspeed = config.get('data', 'max_dmx_adapter_speed')

    config_values = {                                                   #Export our config values in a nice dictionary for easy upgradibility
        'dmxchanmax': dmxchanmax,   
        'serialport': serialport,
        'adatspeed': adatspeed,
        'autoadatspeed': autoadatspeed,
    }
    return(config_values)

config_data = adapter_config()                                      #Read our data
dmxchanmax = int(config_data['dmxchanmax'])                         #Now we need to assign our config to variables
serialport = config_data['serialport']
adatspeed = int(config_data['adatspeed'])
autoadatspeed = int(config_data['autoadatspeed'])

print('Loaded Adapter Settings:')
print(f'DMX Channels in use: {dmxchanmax}')
print(f'Serial Port selected: {serialport}')
if adatspeed == 0:
    print(f'Automatically Assigned Adapter Data Rate: {autoadatspeed}Hz')
else:
    print(f'User Defined Adapter Data Rate: {adatspeed}Hz')

def load_profiles():
    with open('fixtureprofiles.json', 'r') as profilesjson:         # Read JSON file
        profiles = json.load(profilesjson)
    return(profiles)
print('Loading Fixture Profiles...')

profiles = load_profiles()
time.sleep(5)

print('Fixture Profiles Loaded:')
for profile, attribute in profiles.items():                         #Print Profile Names in the JSON File
    print(profile)

procheck = input('Are these profiles listed correct? (Enter to proceed, CTRL-C to cancel) >> ')
if procheck == '':
    print('DMX Subsystem Starting...')
    time.sleep(3)

dmx = Controller(serialport, auto_submit=True, dmx_size=dmxchanmax)   #Now to run our setup code
dmx.set_dmx_parameters(output_rate=adatspeed)
print('DMX Subsystem Started Successfully')
time.sleep(5)

def on_press(key):
        global dmxval                                                    #Make both vars global
        global dmxchan
        if channel_values[dmxchan] > 0:                                     #Check if there are any saved values
            dmxval = channel_values[dmxchan]
        if key == Key.up:
            dmxval += 1
            dmx.set_channel(dmxchan, dmxval)
        if key == Key.down:
            dmxval -= 1
            dmx.set_channel(dmxchan, dmxval)
        if key == Key.esc:
            print('Saving Channel Values...')
            channel_values[dmxchan] = dmxval
            print('Returning you to the Channel Selector...')
            return

channel_values = {}
flag = True
while flag == True:
    chanin = input('Enter channel to change (ENTER to end) >> ')
    dmxchan = int(chanin)
    dmxval = 0
    with Listener(on_press=on_press) as listener:
        listener.join()