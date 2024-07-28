## Property of Stavro Purdie, 2024
## This program is set up to control a fixture of the user's choosing with the keyboard.
import configparser
from DMXEnttecPro import Controller
import time
import json
from pynput.keyboard import Listener, Key
from colorama import init, Fore, Style, Cursor, Back
import os

init(autoreset=True)

## FUNCTIONS BELOW
def adapter_config():                                           ## The main aim of this function is to get the adapter settings from the config
    path = 'Config'
    os.chdir(path)

    config = configparser.ConfigParser()                        ## INIT section: create a configparser object & read file
    config.read('adapterconfig.ini') 

    dmxchanmax = config.get('dmxconfig', 'dmx_channel_count')   ## READ section: access all of the config settings
    serialport = config.get('dmxconfig', 'adapter_serial_port')
    adatspeed = config.get('dmxconfig', 'user_adapter_speed')
    autoadatspeed = config.get('dmxconfig', 'max_dmx_adapter_speed')

    config_values = {                                           ## Export our config values in a nice dictionary for easy upgradibility
        'dmxchanmax': dmxchanmax,   
        'serialport': serialport,
        'adatspeed': adatspeed,
        'autoadatspeed': autoadatspeed,
    }
    return(config_values)

def load_profiles():                                             ## The main aim of this function is to get the profiles from the profiles file
    with open('profiles.json', 'r') as profilesjson:             ## Read fixture library JSON file
        profiles = json.load(profilesjson)
    return(profiles)

def load_patch():                                                ## The main aim of this function is to get the patching data from the patchdata file
    with open('patchdata.json', 'r') as patchdata:
        patch = json.load(patchdata)
    return(patch)

## MAIN PROGRAM
## PSA
print(f'{Fore.BLUE + Style.BRIGHT}DMX Control V0.1 Alpha Starting....')
print(f'{Back.RED + Style.BRIGHT}<<< THIS PROGRAM IS IN ALPHA, PLEASE REPORT BUGS TO GITHUB >>>\n\n')
time.sleep(3)

## This section deals with the adapter config function to retrieve the adapterconfig.ini file and extract the adapter values

try:
    config_data = adapter_config()                                      #Read our data
except:
    print(f"{Style.BRIGHT + Fore.RED}    [XX] File 'adapterconfig.ini' could not be opened!\n")                                                         ## If the function fails, run this code....
    time.sleep(2)
    print(f'{Style.BRIGHT}To diagnose this issue please try these steps:')
    print(f'    [--] Make sure you have run the {Style.BRIGHT}adaptersetup.py{Style.RESET_ALL} program which sets this file up!')
    print(f'    [--] If the progrm is still not working, feel free to {Style.BRIGHT}create an issue in the github with a copy of the exception\n')
    time.sleep(5)
    print(f'{Fore.RED}The program will now exit as an unrecoverable exception has occured. {Style.BRIGHT}ALL DATA HAS BEEN SAVED')
    quit()

dmxchanmax = int(config_data['dmxchanmax'])                         #assign our config to variables
serialport = config_data['serialport']
adatspeed = int(config_data['adatspeed'])
autoadatspeed = int(config_data['autoadatspeed'])

## Print the values we just extracted
print(Fore.GREEN + Style.BRIGHT + 'Loaded Adapter Settings:')                                       
print(f'{Style.BRIGHT}    [--] DMX Channels in use: {dmxchanmax}')
print(f'{Style.BRIGHT}    [--] Serial Port selected: {serialport}')
if adatspeed == 0:
    print(f'{Style.BRIGHT}    [--] Automatically Assigned Adapter Data Rate: {autoadatspeed}Hz\n')
else:
    print(f'{Style.BRIGHT + Fore.BLUE}    [??] User Defined Adapter Data Rate: {adatspeed}Hz {Fore.RED}(Not Recommended)\n')

## This section deals with the load_profiles function to retreve the profiles.json file and extract the fixture values

print(f'{Fore.BLUE + Style.BRIGHT}Loading Fixture Profiles...')
time.sleep(5)
try:
    profiles = load_profiles()                              ## Run the load_profiles() function and return the values to the profiles variable
except:
    print(f"{Style.BRIGHT + Fore.RED}    [XX] File 'profiles.json' could not be opened!\n")                                                                 ## If function fails, run this code....
    time.sleep(2)
    print(f'{Style.BRIGHT}To diagnose this issue please try these steps:')
    print(f'    [--] Make sure you have run the {Style.BRIGHT}fixturelibrarysetup.py{Style.RESET_ALL} program which sets this file up!')
    print(f'    [--] Make sure you are running this program in the {Style.BRIGHT} SAME DIRECTORY as the config file (should be the main directory)')
    print(f'    [--] If the program is still not working, feel free to {Style.BRIGHT}create an issue in the github with a copy of the exception\n')
    time.sleep(5)
    print(f'{Fore.RED}The program will now exit as an unrecoverable exception has occured. {Style.BRIGHT}ALL DATA HAS BEEN SAVED')
    quit()

time.sleep(5)

## Print the fixture profiles, Confirm if they are right. Proceed with program

print(f'{Fore.GREEN + Style.BRIGHT}Fixture Profiles Loaded:')
for profile, attribute in profiles.items():                         #Print Profile Names in the JSON File
    print(f'{Style.BRIGHT}    [--] {profile}')
print()

procheck = input('Are the profiles listed correct? (Enter to proceed, CTRL-C to cancel) >> ')
if procheck == '':
    print(f'{Fore.BLUE + Style.BRIGHT}DMX Virtual Patch Configuraton Wizard Starting....\n')
    time.sleep(3)

## This section deals with the load_patch function to retreve the patchdata.json file and extract the patch values

print(f'{Fore.BLUE + Style.BRIGHT}Loading DMX Patch Values...')
time.sleep(5)
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

time.sleep(5)
print(f'{Fore.GREEN + Style.BRIGHT}DMX Patch Values Loaded...')

channels_used = []          ## Init channels_used list
## This initially shows how many channels are in use
for profilename, attribute1 in profiles.items():
    for profile, attribute2 in patchdata.items():
        for fixturename, attribute3 in patchdata[profilename].items():
            channels_used.append(patchdata[profilename][fixturename]['channels_used'])
print(f'{Back.BLUE + Style.BRIGHT}<<< You currently have {dmxchanmax - sum(channels_used)} Channels Available of {dmxchanmax} >>>')

## This prints out the fixture profiles and how many channels they each take up
print(f'\n {Fore.BLUE + Style.BRIGHT}Fixture Profiles in Library:')
for profile, attributes in profiles.items():
    profilechancount = int(profiles[profile]['channel_count'])
    print(f'{Style.BRIGHT}      [--] {profile} | {Back.BLUE}<<< Takes up {profilechancount} DMX Channels per fixture >>>')       ## This loop prints to the user the fixtures in the library and how many channels they each take up
print('')

## This prints out what fixture is patched where aswell as what fixture is what
print(f'\n {Fore.BLUE + Style.BRIGHT}Breakdown of Patched Fixtures:')
for profilename, attribute1 in profiles.items():
    print(f'{Style.BRIGHT}      [--] {profilename} has {len(patchdata[profilename])} fixtures patched')
    for profile, attribute2 in patchdata.items():
        fixturename = list(patchdata[profilename].keys())
    startingchannel = {}
    for fixname in fixturename:
        startingchannel[fixname] = patchdata[profilename][fixname]['starting_channel']
        print(f'{Style.BRIGHT}        [->]', str(fixname).strip("['']"), f'Starts on channel {startingchannel[fixname]}')

time.sleep(5)

## Starting DMX Subsystem
print(f'{Fore.BLUE + Style.BRIGHT}Starting the DMX Subsystem')
time.sleep(3)

## This section of the program initialized the adapter using the adapterconfig.ini file
try:
    dmx = Controller(serialport, auto_submit=True, dmx_size=dmxchanmax) 
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
#    quit()
print(f'{Fore.GREEN + Style.BRIGHT}DMX Subsystem Started Successfully')
time.sleep(5)

## The business end of the program, This is the bit that controls the lights

def on_press(key):
    global dmxval                                                    #Make vars global so that we can easily obtain access
    global fixturename
    global fixturestartchan
    global fixtureprofilename
    global profiles
    global savedfixturechan

    loaded_controlvars = 
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
fixtureindex = {}
savedfixturechan = {}
flag = True
while flag == True:
    ## This prints out what fixture is patched where aswell as what fixture is what
    i = 0
    print(f'\n {Fore.BLUE + Style.BRIGHT}Fixtures available to control:')
    for profilename, attribute1 in profiles.items():
        print(f'{Style.BRIGHT}      [--] {profilename} has {len(patchdata[profilename])} fixtures patched')
        for profile, attribute2 in patchdata.items():
            fixturename = list(patchdata[profilename].keys())
        startingchannel = {}
        for fixname in fixturename:
            i = int(i + 1)
            startingchannel[fixname] = patchdata[profilename][fixname]['starting_channel']
            print(f'{Style.BRIGHT}        [{i}->]', str(fixname).strip("['']"), f'Starts on channel {startingchannel[fixname]}')
            fixtureindex[i] = {}
            fixtureindex[i]['fixturename'] = {}
            fixtureindex[i]['fixturename'] = str(fixname)
            fixtureindex[i]['startingchannel'] = {}
            fixtureindex[i]['startingchannel'] = startingchannel[fixname]
            fixtureindex[i]['profilename'] = profilename

    fixturenum = int(input('Enter fixture number to change (ENTER to end) >> '))
    if fixturenum == '':
        print(f'{Fore.GREEN + Style.BRIGHT} Program Quitting....')
        quit()
    
    fixturename = fixtureindex[fixturenum]['fixturename']
    fixturestartchan = fixtureindex[fixturenum]['startingchannel']
    fixtureprofilename = fixtureindex[fixturenum]['profilename']
    print(f'\n {Fore.BLUE + Style.BRIGHT}You Have Selected {fixturename}')

    
    dmxval = 0
    with Listener(on_press=on_press) as listener:
        listener.join()
