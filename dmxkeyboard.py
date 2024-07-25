## Property of Stavro Purdie, 2024
## This program is set up to individually control a channel of the user's choosing with the keyboard.
## THIS PROGRAM IS OBSOLETE AND IS JUST FOR REFERENCE (as of 23rd Jul 2024)
import configparser
from DMXEnttecPro import Controller
import time
import json
from pynput.keyboard import Listener, Key
from colorama import init, Fore, Style, Cursor, Back
import os

init(autoreset=True)

def adapter_config():
    path = 'Config'
    os.chdir(path)

    config = configparser.ConfigParser()    #INIT section: create a configparser object & read file
    config.read('adapterconfig.ini') 

    dmxchanmax = config.get('dmxconfig', 'dmx_channel_count') #READ section: access all of the config settings
    serialport = config.get('dmxconfig', 'adapter_serial_port')
    adatspeed = config.get('dmxconfig', 'user_adapter_speed')
    autoadatspeed = config.get('dmxconfig', 'max_dmx_adapter_speed')

    config_values = {                                                   #Export our config values in a nice dictionary for easy upgradibility
        'dmxchanmax': dmxchanmax,   
        'serialport': serialport,
        'adatspeed': adatspeed,
        'autoadatspeed': autoadatspeed,
    }
    return(config_values)
try:
    config_data = adapter_config()                                      #Read our data
except:
    print(f"{Style.BRIGHT + Fore.RED}    [XX] File 'adapterconfig.ini' could not be opened!\n")
    time.sleep(2)
    print(f'{Style.BRIGHT}To diagnose this issue please try these steps:')
    print(f'    [--] Make sure you have run the {Style.BRIGHT}adaptersetup.py{Style.RESET_ALL} program which sets this file up!')
    print(f'    [--] If the progrm is still not working, feel free to {Style.BRIGHT}create an issue in the github with a copy of the exception\n')
    time.sleep(5)
    print(f'{Fore.RED}The program will now exit as an unrecoverable exception has occured. {Style.BRIGHT}ALL DATA HAS BEEN SAVED')
    quit()

dmxchanmax = int(config_data['dmxchanmax'])                         #Now we need to assign our config to variables
serialport = config_data['serialport']
adatspeed = int(config_data['adatspeed'])
autoadatspeed = int(config_data['autoadatspeed'])

print(Fore.GREEN + Style.BRIGHT + 'Loaded Adapter Settings:')
print(f'{Style.BRIGHT}    [--] DMX Channels in use: {dmxchanmax}')
print(f'{Style.BRIGHT}    [--] Serial Port selected: {serialport}')
if adatspeed == 0:
    print(f'{Style.BRIGHT}    [--] Automatically Assigned Adapter Data Rate: {autoadatspeed}Hz\n')
else:
    print(f'{Style.BRIGHT + Fore.BLUE}    [??] User Defined Adapter Data Rate: {adatspeed}Hz (Not Recommended)\n')

def load_profiles():
    with open('profiles.json', 'r') as profilesjson:         # Read JSON file
        profiles = json.load(profilesjson)
    return(profiles)

print(f'{Fore.BLUE + Style.BRIGHT}Loading Fixture Profiles...')
time.sleep(5)
try:
    profiles = load_profiles()
except:
    print(f"{Style.BRIGHT + Fore.RED}    [XX] File 'profiles.json' could not be opened!\n")
    time.sleep(2)
    print(f'{Style.BRIGHT}To diagnose this issue please try these steps:')
    print(f'    [--] Make sure you have run the {Style.BRIGHT}fixturelibrarysetup.py{Style.RESET_ALL} program which sets this file up!')
    print(f'    [--] Make sure you are running this program in the {Style.BRIGHT} SAME DIRECTORY as the config file (should be the main directory)')
    print(f'    [--] If the progrm is still not working, feel free to {Style.BRIGHT}create an issue in the github with a copy of the exception\n')
    time.sleep(5)
    print(f'{Fore.RED}The program will now exit as an unrecoverable exception has occured. {Style.BRIGHT}ALL DATA HAS BEEN SAVED')
    quit()

time.sleep(5)

print(f'{Fore.GREEN + Style.BRIGHT}Fixture Profiles Loaded:')
for profile, attribute in profiles.items():                         #Print Profile Names in the JSON File
    print(f'    [--] {profile}')
print()

procheck = input('Are the profiles listed correct? (Enter to proceed, CTRL-C to cancel) >> ')
if procheck == '':
    print(f'{Fore.BLUE + Style.BRIGHT}Loading DMX Patch Information....')
    time.sleep(3)

def load_patch():                                                                                   ## Load Patch Data
    with open('patchdata.json', 'r') as patchdata:
        patch = json.load(patchdata)
    return(patch)

try:
    patchdata = load_patch()
except:
    print(f"{Style.BRIGHT + Fore.RED}    [XX] File 'patchdata.json' could not be opened!\n")                                                                 ## If function fails, run this code....
    time.sleep(2)
    print(f'{Style.BRIGHT}To diagnose this issue please try these steps:')
    print(f'    [--] Make sure you have run the {Style.BRIGHT}dmxpatchsetup.py{Style.RESET_ALL} program which sets this file up!')
    print(f'    [--] Make sure you are running this program in the {Style.BRIGHT} HOME DIRECTORY)')
    print(f'    [--] If the program is still not working, feel free to {Style.BRIGHT}create an issue in the github with a copy of the exception\n')
    time.sleep(5)
    print(f'{Fore.RED}The program will now exit as an unrecoverable exception has occured. {Style.BRIGHT}ALL DATA HAS BEEN SAVED')
    quit()

print(f'{Fore.GREEN + Style.BRIGHT}DMX Patching Information Loaded....')

channels_used = []          ## Init channels_used list
for profilename, attribute1 in profiles.items():
    for profile, attribute2 in patchdata.items():
        for fixturename, attribute3 in patchdata[profilename].items():
            channels_used.append(patchdata[profilename][fixturename]['channels_used'])
print(f'{Back.BLUE + Style.BRIGHT}<<< You currently have {dmxchanmax - sum(channels_used)} Channels Left of {dmxchanmax} >>>')

print(f'\n {Fore.BLUE + Style.BRIGHT}Breakdown of Patched Fixtures:')
for profilename, attribute1 in profiles.items():
    print(f'{Style.BRIGHT}      [--] {profilename} has {len(patchdata[profilename])} fixtures patched')
    for profile, attribute2 in patchdata.items():
        fixturename = list(patchdata[profilename].keys())
    startingchannel = {}
    for fixname in fixturename:
        startingchannel[fixname] = patchdata[profilename][fixname]['starting_channel']
        print(f'{Style.BRIGHT}        [->]', str(fixname).strip("['']"), f'Starts on channel {startingchannel[fixname]}')

print(f'{Fore.BLUE + Style.BRIGHT}DMX Subsystem starting....')

try:
    dmx = Controller(serialport, auto_submit=True, dmx_size=dmxchanmax)   #Now to run our setup code
    dmx.set_dmx_parameters(output_rate=adatspeed)
except:
    print(f'{Fore.RED + Style.BRIGHT}    [XX] Serial Port {serialport} is unreachable. The DMX Subsystem is unable to start.\n')
    time.sleep(2)
    print(f'{Style.BRIGHT}To diagnose this issue please try these steps:')
    print(f'    [--] Make sure the DMX adapter is {Style.BRIGHT}plugged in and recieving power')
    print(f'    [--] Run the {Style.BRIGHT}adaptersetup.py{Style.RESET_ALL} program and ensure the correct {Style.BRIGHT}COM/TTY port{Style.RESET_ALL} is selected aswell as the corect {Style.BRIGHT}sample rate')
    print(f'    [--] Ensure the adapter is based on the {Style.BRIGHT}RS485 protocol{Style.RESET_ALL} OR is based around an {Style.BRIGHT}ENTTEC/DMXKing Adapter')
    print(f'    [--] If the progrm is still not working, feel free to {Style.BRIGHT}create an issue in the github with a copy of the exception\n')
    time.sleep(5)
    print(f'{Fore.RED}The program will now exit as an unrecoverable exception has occured. {Style.BRIGHT}ALL DATA HAS BEEN SAVED')
    quit()
print(f'{Fore.GREEN + Style.BRIGHT}DMX Subsystem Started Successfully')
time.sleep(5)

def on_press(key):
    global dmxval                                                    #Make both vars global so that we can easily obtain access to such vars
    global dmxchan
    if channel_values[dmxchan] > 0:                                     #Check if there are any saved values
        dmxval = channel_values[dmxchan]                                #Apply Saved Channel Values
    if key == Key.up:                                                   #If Up Arrow Key Pressed...
        dmxval += 1                                                     #Add 1 to the channel val
        dmx.set_channel(dmxchan, dmxval)                                #Run DMX Frame Through DMX Subsystem
    if key == Key.down:
        dmxval -= 1
        dmx.set_channel(dmxchan, dmxval)
    if key == Key.esc:
        print(f'{Fore.GREEN}Saving Channel Values...')
        channel_values[dmxchan] = dmxval
        print(f'{Fore.BLUE}Returning you to the Channel Selector...')
        print()
        Listener.stop()
        return

channel_values = {}
flag = True
while flag == True:
    chanin = input('Enter channel to change (ENTER to end) >> ')
    dmxchan = int(chanin)
    dmxval = 0
    with Listener(on_press=on_press) as listener:
        listener.join()