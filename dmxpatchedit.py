## Property of Stavro Purdie, 2024
## This program configures the DMX subsystem virtual patch panel edit values 
import json
import os
from colorama import init, Fore, Style, Cursor, Back
import time
import configparser
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
print(f'{Fore.BLUE + Style.BRIGHT}DMX Virtual Patch Panel Configuration Utility Starting....\n\n')
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

## Fixture Patch Config Code Below

print(f'{Fore.BLUE + Style.BRIGHT}DMX Virtual Patch Configuration Wizard Starting....')

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

## This asks the user some basic questions and presents them with how many DMX channels would be left/taken up after the operation
for profile, attributes in profiles.items():
    profilechancount = int(profiles[profile]['channel_count'])
    count = int(input(f'{Style.BRIGHT}How many of fixture {profile} would you like to add? >> '))                           ## Config questions like how many of var fixture to add
    print(f'{Fore.GREEN + Style.BRIGHT}Adding {count} fixtures of make {profile} to the system...')
    print('')
    print(f'{Back.BLUE + Style.BRIGHT}<<< Adding {count} of Fixture {profile} will take up {profilechancount * count} DMX Channels >>>')
    print(f'{Back.BLUE + Style.BRIGHT}<<< You will have {(dmxchanmax - sum(channels_used)) - (profilechancount * count)} DMX Channels left after this operation >>>')   ## Inform the user about how many DMX channels this will take up, aswell as how many would be left after the operation
    time.sleep(2)

    ## This asks the user some basic fixture questions
    for i in range(count):
        print('')
        fixturename = input(f'{Style.BRIGHT}What should fixture {i+1} of {count} be named eg SPOT1 >> ')                ## More config questions
        startingchan = input(f'{Style.BRIGHT}What channel should fixture {i+1} of {count} start on? >> ')
        patchdata[profile][fixturename] = {}                                                                            ## Save to Dictionary
        patchdata[profile][fixturename]['starting_channel'] = startingchan
        patchdata[profile][fixturename]['channels_used'] = profilechancount
        
print('')

## Finish!
print(f'{Fore.BLUE + Style.BRIGHT}The DMX Virtual Patch Configuration Wizard has finished\n')
print(f'{Back.BLUE + Style.BRIGHT}<<< SAVING TO PATCHDATA.JSON... PLEASE WAIT >>>')

## This section deals with the overwriting of the config file
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

## Literally the end of the program
time.sleep(4)
print(f'{Back.GREEN + Style.BRIGHT}<<< CONFIG HAS BEEN SAVED >>>')
print('')
time.sleep(2)
print(f"{Fore.BLUE + Style.BRIGHT}To change the patch data, please navigate to the home directory and run 'dmxpatchedit.py'\n")
print(f'{Fore.CYAN}The Program will now exit....')
quit()