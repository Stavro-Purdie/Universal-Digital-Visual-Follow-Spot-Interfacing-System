## Property of Stavro Purdie, 2024
## This program configures the DMX subsystem virtual patch panel edit values 
import json
import os
from colorama import init, Fore, Style, Cursor, Back
import time
import configparser
init(autoreset=True)

print(f'{Fore.BLUE + Style.BRIGHT}DMX Virtual Patch Panel Configuration Utility Starting....\n\n')
time.sleep(3)

def adapter_config():                                           ## Retreve Adapter Settings
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

print(Fore.GREEN + Style.BRIGHT + 'Loaded Adapter Settings:')                                       ## Print out our adapter settings for the user
print(f'{Style.BRIGHT}    [--] DMX Channels in use: {dmxchanmax}')
print(f'{Style.BRIGHT}    [--] Serial Port selected: {serialport}')
if adatspeed == 0:
    print(f'{Style.BRIGHT}    [--] Automatically Assigned Adapter Data Rate: {autoadatspeed}Hz\n')
else:
    print(f'{Style.BRIGHT + Fore.BLUE}    [??] User Defined Adapter Data Rate: {adatspeed}Hz {Fore.RED}(Not Recommended)\n')


def load_profiles():
    with open('profiles.json', 'r') as profilesjson:         # Read fixture library JSON file
        profiles = json.load(profilesjson)
    return(profiles)

print(f'{Fore.BLUE + Style.BRIGHT}Loading Fixture Profiles...')
time.sleep(5)
try:
    profiles = load_profiles()
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

print(f'{Fore.GREEN + Style.BRIGHT}Fixture Profiles Loaded:')
for profile, attribute in profiles.items():                         #Print Profile Names in the JSON File
    print(f'{Style.BRIGHT}    [--] {profile}')
print()

procheck = input('Are the profiles listed correct? (Enter to proceed, CTRL-C to cancel) >> ')
if procheck == '':
    print(f'{Fore.BLUE + Style.BRIGHT}DMX Virtual Patch Configuraton Wizard Starting....\n')
    time.sleep(3)

def load_patch():
    with open('patchdata.json', 'r') as patchdata:
        patch = json.load(patchdata)
    return(patch)


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
print(f'{Fore.BLUE + Style.BRIGHT}DMX Virtual Patch Configuration Wizard Starting....')

channels_used = []
for profilename, attribute1 in profiles.items():
    for profile, attribute2 in patchdata.items():
        for fixturename, attribute3 in patchdata[profilename].items():
            channels_used.append(patchdata[profilename][fixturename]['channels_used'])
print(f'{Back.BLUE + Style.BRIGHT}<<< You currently have {dmxchanmax - sum(channels_used)} Channels Available of {dmxchanmax} >>>')

print(f'\n {Fore.BLUE + Style.BRIGHT}Fixture Profiles in Library:')
for profile, attributes in profiles.items():
    profilechancount = int(profiles[profile]['channel_count'])
    print(f'{Style.BRIGHT}      [--] {profile} | {Back.BLUE}<<< Takes up {profilechancount} DMX Channels per fixture >>>')       ## This loop prints to the user the fixtures in the library and how many channels they each take up
print('')

print(f'\n {Fore.BLUE + Style.BRIGHT}Breakdown of Patched Fixtures:')
for profilename, attribute1 in profiles.items():
    print(f'      [--] {profilename} has {len(patchdata[profilename])} fixtures patched')
    for profile, attribute2 in patchdata.items():
        for fixturename, attribute3 in patchdata[profilename].items():
            profilename = list(patchdata[profilename].keys())
            print(f'        [->]', str(profilename).strip("['']"), 'Starts on channel {patchdata[profilename][fixturename]["starting_channel"]}')
