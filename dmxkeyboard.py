## Property of Stavro Purdie, 2024
import configparser
from DMXEnttecPro import Controller
import time
import json
from pynput import keyboard

def adapter_config():
    config = configparser.ConfigParser()    #INIT section: create a configparser object & read file
    config.read('adapterconfig.ini') 

    dmxchanmax = config.get('dmxconfig', 'dmx_channel_count') #READ section: access all of the config settings
    serialport = config.get('dmxconfig', 'adapter_serial_port')
    adatspeed = config.get('dmxconfig', 'adapter_speed')

    config_values = {                                                   #Export our config values in a nice dictionary for easy upgradibility
        'dmxchanmax': dmxchanmax,   
        'serialport': serialport,
        'adatspeed': adatspeed,
    }
    return(config_values)

config_data = adapter_config()                                      #Read our data
dmxchanmax = int(config_data['dmxchanmax'])                         #Now we need to assign our config to variables
serialport = config_data['serialport']
adatspeed = int(config_data['adatspeed'])

print('Loaded Adapter Settings:')
print(f'DMX Channels in use: {dmxchanmax}')
print(f'Serial Port selected: {serialport}')
print(f'Adapter Data Rate: {adatspeed}')

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

flag = True
while flag == True:
    chanin = input('Enter channel to change (ENTER to end) >> ')
    dmxchan = int(chanin)
    def on_press(key):
        i = 0
        if key == keyboard.Key.up:
            dmx.set_channel(dmxchan, i+1)
        if key == keyboard.Key.down:
            dmx.set_channel(dmxchan, i-1)
        if key == keyboard.Key.esc:
            print('Exiting Channel Listener. Hang on...')
            time.sleep(3)
            print('Returning you to the Channel Selector...')

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

               
               
               

    
    

