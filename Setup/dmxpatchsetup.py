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

print(f'{Fore.BLUE + Style.BRIGHT}Please select how many of each fixture you would like to initially start with:')

patchdata = {}                                                                                                          ## Init Patchdata Dict, This stores the patch info                                                                                                      ## Init list to store channel values for how many channels have been used
for profile, attributes in profiles.items():
    profilechancount = int(profiles[profile]['channel_count'])
    print(f'{Style.BRIGHT}    [--] {profile} | {Back.BLUE}<<< Takes up {profilechancount} DMX Channels per fixture >>>')       ## This loop prints to the user the fixtures in the library and how many channels they each take up
    patchdata[profile] = {}
print('')

channels_used = []
for profile in profiles:
    print(f'{Back.BLUE + Style.BRIGHT}<<< You currently have {dmxchanmax - sum(channels_used)} Channels Available >>>')  ## This is then presented to the user as how many channels are left over (max dmx chan (from adapter) - sum of list)

    profilechancount = int(profiles[profile]['channel_count'])
    count = int(input(f'{Style.BRIGHT}How many of fixture {profile} would you like to add? >> '))                           ## Config questions like how many of var fixture to add
    print(f'{Fore.GREEN + Style.BRIGHT}Adding {count} fixtures of make {profile} to the system...')
    print('')
    print(f'{Back.BLUE + Style.BRIGHT}<<< Adding {count} of Fixture {profile} will take up {profilechancount * count} DMX Channels >>>')
    channels_used.append(profilechancount * count)
    print(f'{Back.BLUE + Style.BRIGHT}<<< You will have {(dmxchanmax - sum(channels_used))} DMX Channels left after this operation >>>')   ## Inform the user about how many DMX channels this will take up, aswell as how many would be left after the operation
    time.sleep(2)

    for i in range(count):
        print('')
        fixturename = input(f'{Style.BRIGHT}What should fixture {i+1} of {count} be named eg SPOT1 >> ')                ## More config questions
        startingchan = input(f'{Style.BRIGHT}What channel should fixture {i+1} of {count} start on? >> ')
        patchdata[profile][fixturename] = {}                                                                           ## Save to Dictionary
        patchdata[profile][fixturename]['starting_channel'] = startingchan
        patchdata[profile][fixturename]['channels_used'] = profilechancount

print('')

print(f'{Fore.BLUE + Style.BRIGHT}The DMX Virtual Patch Configuration Wizard has finished\n')
print(f'{Back.BLUE + Style.BRIGHT}<<< SAVING TO PATCHDATA.JSON... PLEASE WAIT >>>')

try:
    path = '../Config'
    os.chdir(path)
    with open('patchdata.json', 'w') as convert_file: 
        convert_file.write(json.dumps(patchdata, indent=4))
except:
    print(f"{Back.RED + Style.BRIGHT}   [XX] UNABLE TO SAVE CONFIG FILE")
    time.sleep(4)
    print(f"{Style.BRIGHT}To diagnose this issue please try these steps:")
    print(f"    [--] Please ensure you are running this script through the {Style.BRIGHT}'setup.py' program in the home directory")
    print(f"    [--] Check that the Config directory exists in the home directory of the program. If it doesen't, please reinstall the program.")
    time.sleep(5)
    print(f'{Fore.RED}The program will now exit as an unrecoverable exception has occured. {Style.BRIGHT}ALL DATA HAS BEEN SAVED')
    quit()

time.sleep(4)
print(f'{Back.GREEN + Style.BRIGHT}<<< CONFIG HAS BEEN SAVED >>>')
print('')
time.sleep(2)
print(f"{Fore.BLUE + Style.BRIGHT}If another fixture profile is added and you need to delete patch data, please rerun this program")
print(f"{Fore.BLUE + Style.BRIGHT}To change the patch data, please navigate to the home directory and run 'dmxpatchedit.py'\n")
print(f'{Fore.CYAN}The Program will now exit....')
quit()