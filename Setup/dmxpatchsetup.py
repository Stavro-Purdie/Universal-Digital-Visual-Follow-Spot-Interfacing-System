## Property of Stavro Purdie, 2024
## This program configures the DMX subsystem virtual patch panel
import json
import os
from colorama import init, Fore, Style, Cursor, Back
import time
import configparser
init(autoreset=True)

print(f'{Fore.BLUE + Style.BRIGHT}DMX Virtual Patch Panel First Time Configuration Utility Starting....\n\n')
time.sleep(3)

confirm = input(f"{Fore.RED + Style.BRIGHT}WARNING! | This program resets your entire virtual patch panel. To continue, please type 'YES' otherwise press ENTER for exit >> ")
print('\n')
if confirm == '':
    print(f'{Fore.GREEN}Configuration Utility Exiting, {Style.BRIGHT}No settings have been changed')
    quit()


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
    print(f'{Style.BRIGHT + Fore.BLUE}    [??] User Defined Adapter Data Rate: {adatspeed}Hz {Fore.RED}(Not Recommended)\n')


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
    print(f'{Style.BRIGHT}    [--] {profile}')
print()

procheck = input('Are the profiles listed correct? (Enter to proceed, CTRL-C to cancel) >> ')
if procheck == '':
    print(f'{Fore.BLUE + Style.BRIGHT}DMX Virtual Patch Configuraton Wizard Starting....\n')
    time.sleep(3)

print(f'{Back.BLUE + Style.BRIGHT}<<< You have {dmxchanmax} Channels available >>>')
print(f'{Fore.BLUE + Style.BRIGHT}Please select how many of each fixture you would like to initially start with:')
fixturecount = {}
fixturename = ''
count = 0
for profile, attribute in profiles.items():
    print(f'{Style.BRIGHT}    [--] {profile}')
    count = int(input(f'{Style.BRIGHT}How many of fixture {profile} would you like to add? >> '))
    print(f'{Fore.GREEN + Style.BRIGHT}Adding {count} fixtures of make {profile} to the system...')
    time.sleep(2)

    for i in range(count):
        fixturename = input(f'{Style.BRIGHT}What should fixture {i} of {count} be named eg SPOT1 >> ')
        startingchan = input(f'{Style.BRIGHT}What channel should fixture {i} of {count} start on? >> ')
        


