## Property of Stavro Purdie, 2024
## This program is set up to control a fixture of the user's choosing with the keyboard.
import configparser
from DMXEnttecPro import Controller
import time
import json
import keyboard
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
print(f'{Back.RED + Style.BRIGHT}<<< THIS PROGRAM IS IN ALPHA, PLEASE REPORT BUGS TO GITHUB >>>')
print('\n')
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
    quit()
print(f'{Fore.GREEN + Style.BRIGHT}DMX Subsystem Started Successfully')
time.sleep(5)

## The business end of the program, This is the bit that controls the lights
def on_press():
    global pan
    global panfine
    global tilt
    global tiltfine
    global ptspeed
    global conventional
    global red
    global green
    global blue
    global cyan
    global magenta
    global yellow
    global cto
    global zoom
    global focus
    global frost
    global static_gobo
    global rotating_gobo
    global dimmer
    global dimmer_fine

    while True:
        if numpad == 'y' or 'Y':
            if keyboard.is_pressed("8"):
                tiltfine += 16                          #0.128 degrees per 16 bits 0.008 degrees per bit
                if tiltfine > 255:                     #If tiltfine maxed out
                    tilt += 1                           #Add one to tilt (2.1 degrees per bit)
                    tiltfine = 0                  #Reset tiltfine (dmx starts at 0 and ends at 255, total of 256 bits)
                if tilt > 255 and tiltfine > 255:     #If fixture fully maxxed out, keep at 255
                    tilt = 255
                    tiltfine = 255
                time.sleep(0.01)                        #Delay helps with the key issue 
                dmx.set_channel(movementchannels['tilt_fine'], tiltfine)        #send off 1 frame per var
                dmx.set_channel(movementchannels['tilt'], tilt)                 
                
            elif keyboard.is_pressed("2"):
                tiltfine -= 16
                if tiltfine < 0:
                    tilt -= 1
                    tiltfine = 255
                if tilt < 0 and tiltfine < 0:
                    tilt = 0
                    tiltfine = 0
                time.sleep(0.01)
                dmx.set_channel(movementchannels['tilt_fine'], tiltfine)
                dmx.set_channel(movementchannels['tilt'], tilt)

            elif keyboard.is_pressed("6"):
                panfine += 16
                if panfine > 255:
                    pan += 1
                    panfine = 0
                if pan > 255 and tiltfine > 255:
                    pan = 255
                    tilt = 255
                time.sleep(0.01)
                dmx.set_channel(movementchannels['pan_fine'], panfine)
                dmx.set_channel(movementchannels['pan'], pan)

            elif keyboard.is_pressed("4"):
                panfine -= 16
                if panfine < 0:
                    pan -= 1
                    panfine = 255
                if pan < 0 and panfine < 0:
                    pan = 0
                    panfine = 0
                time.sleep(0.01)
                dmx.set_channel(movementchannels['pan_fine'], panfine)
                dmx.set_channel(movementchannels['pan'], pan)
        else:
            if keyboard.is_pressed("up"):
                tiltfine += 16                          #0.128 degrees per 16 bits 0.008 degrees per bit
                if tiltfine > 255:                     #If tiltfine maxed out
                    tilt += 1                           #Add one to tilt (2.1 degrees per bit)
                    tiltfine = 0                  #Reset tiltfine (dmx starts at 0 and ends at 255, total of 256 bits)
                if tilt > 255 and tiltfine > 255:     #If fixture fully maxxed out, keep at 255
                    tilt = 255
                    tiltfine = 255
                time.sleep(0.01)                        #Delay helps with the key issue 
                dmx.set_channel(movementchannels['tilt_fine'], tiltfine)        #send off 1 frame per var
                dmx.set_channel(movementchannels['tilt'], tilt)

            elif keyboard.is_pressed("down"):
                tiltfine -= 16
                if tiltfine < 0:
                    tilt -= 1
                    tiltfine = 255
                if tilt < 0 and tiltfine < 0:
                    tilt = 0
                    tiltfine = 0
                time.sleep(0.01)
                dmx.set_channel(movementchannels['tilt_fine'], tiltfine)
                dmx.set_channel(movementchannels['tilt'], tilt)

            elif keyboard.is_pressed("right"):
                panfine += 16
                if panfine > 255:
                    pan += 1
                    panfine = 0
                if pan > 255 and tiltfine > 255:
                    pan = 255
                    tilt = 255
                time.sleep(0.01)
                dmx.set_channel(movementchannels['pan_fine'], panfine)
                dmx.set_channel(movementchannels['pan'], pan)

            elif keyboard.is_pressed("left"):
                panfine -= 16
                if panfine < 0:
                    pan -= 1
                    panfine = 255
                if pan < 0 and panfine < 0:
                    pan = 0
                    panfine = 0
                time.sleep(0.01)
                dmx.set_channel(movementchannels['pan_fine'], panfine)
                dmx.set_channel(movementchannels['pan'], pan)
        
        if keyboard.is_pressed("c"):
            time.sleep(0.1)
            print(f'{Back.BLUE + Style.BRIGHT}<<< Colour Selected >>>')
            ## Conventional Section
            if isconventional == True:
                while True:
                    if keyboard.is_pressed("w"):
                        time.sleep(0.1)
                        print(f'{Back.BLUE + Style.BRIGHT}<<< Colour Wheel Selected, Press Arrow Up/Down to change, Press Enter to exit to Colour Menu >>>')
                        while True:
                            if keyboard.is_pressed("up"):
                                conventional += 1
                                if conventional > 255:
                                    conventional = 255
                                time.sleep(0.05)
                                dmx.set_channel(colourchannels['colour_wheel'], conventional)
                            if keyboard.is_pressed("down"):
                                conventional -= 1
                                if conventional < 0:
                                    conventional = 0
                                time.sleep(0.05)
                                dmx.set_channel(colourchannels['colour_wheel'], conventional)
                            if keyboard.is_pressed("enter"):
                                time.sleep(0.5)
                                print(f'{Back.BLUE + Style.BRIGHT}<<< Exiting to colour menu >>>')
                                print(f'{Back.BLUE + Style.BRIGHT}<<< Colour Selected >>>')
                                break
                    if keyboard.is_pressed("enter"):
                        time.sleep(0.5)
                        print(f'{Back.BLUE + Style.BRIGHT}<<< Back to Main control menu >>>')
                        break
            ##RGB Section
            if isrgb == True:
                while True:
                    ## Red Section
                    if keyboard.is_pressed("r"):
                        time.sleep(0.1)
                        print(f'{Back.BLUE + Style.BRIGHT}<<< Red Selected, Press Arrow Up/Down to change, Press Enter to exit to Colour Menu >>>')
                        while True:
                            if keyboard.is_pressed("up"):
                                red += 1
                                if red > 255:
                                    red = 255
                                time.sleep(0.025)
                                dmx.set_channel(colourchannels['red'], red)
                            if keyboard.is_pressed("down"):
                                red -= 1
                                if red < 0:
                                    red = 0
                                time.sleep(0.025)
                                dmx.set_channel(colourchannels['red'], red)
                            if keyboard.is_pressed("enter"):
                                time.sleep(0.5)
                                print(f'{Back.BLUE + Style.BRIGHT}<<< Exiting to colour menu >>>')
                                print(f'{Back.BLUE + Style.BRIGHT}<<< Colour Selected >>>')
                                break
                    ## Green Section
                    if keyboard.is_pressed("g"):
                        time.sleep(0.1)
                        print(f'{Back.BLUE + Style.BRIGHT}<<< Green Selected, Press Arrow Up/Down to change, Press Enter to exit to Colour Menu >>>')
                        while True:
                            if keyboard.is_pressed("up"):
                                green += 1
                                if green > 255:
                                    green = 255
                                time.sleep(0.025)
                                dmx.set_channel(colourchannels['green'], green)
                            if keyboard.is_pressed("down"):
                                green -= 1
                                if green < 0:
                                    green = 0
                                time.sleep(0.025)
                                dmx.set_channel(colourchannels['green'], green)
                            if keyboard.is_pressed("enter"):
                                time.sleep(0.5)
                                print(f'{Back.BLUE + Style.BRIGHT}<<< Exiting to colour menu >>>')
                                print(f'{Back.BLUE + Style.BRIGHT}<<< Colour Selected >>>')
                                break
                    ## Blue Section
                    if keyboard.is_pressed("b"):
                        time.sleep(0.1)
                        print(f'{Back.BLUE + Style.BRIGHT}<<< Blue Selected, Press Arrow Up/Down to change, Press Enter to exit to Colour Menu >>>')
                        while True:
                            if keyboard.is_pressed("up"):
                                blue += 1
                                if blue > 255:
                                    blue = 255
                                time.sleep(0.025)
                                dmx.set_channel(colourchannels['blue'], blue)
                            if keyboard.is_pressed("down"):
                                blue -= 1
                                if blue < 0:
                                    blue = 0
                                time.sleep(0.025)
                                dmx.set_channel(colourchannels['blue'], blue)
                            if keyboard.is_pressed("enter"):
                                time.sleep(0.5)
                                print(f'{Back.BLUE + Style.BRIGHT}<<< Exiting to colour menu >>>')
                                print(f'{Back.BLUE + Style.BRIGHT}<<< Colour Selected >>>')
                                break
            ##CMY Section
            if iscmy == True:
                while True:
                    ## Cyan Section
                    if keyboard.is_pressed("c"):
                        time.sleep(0.1)
                        print(f'{Back.BLUE + Style.BRIGHT}<<< Cyan Selected, Press Arrow Up/Down to change, Press Enter to exit to Colour Menu >>>')
                        while True:
                            if keyboard.is_pressed("up"):
                                cyan += 1
                                if cyan > 255:
                                    cyan = 255
                                time.sleep(0.025)
                                dmx.set_channel(colourchannels['cyan'], cyan)
                            if keyboard.is_pressed("down"):
                                cyan -= 1
                                if cyan < 0:
                                    cyan = 0
                                time.sleep(0.025)
                                dmx.set_channel(colourchannels['cyan'], cyan)
                            if keyboard.is_pressed("enter"):
                                time.sleep(0.5)
                                print(f'{Back.BLUE + Style.BRIGHT}<<< Exiting to colour menu >>>')
                                print(f'{Back.BLUE + Style.BRIGHT}<<< Colour Selected >>>')
                                break
                    ## Magenta Section
                    if keyboard.is_pressed("m"):
                        time.sleep(0.1)
                        print(f'{Back.BLUE + Style.BRIGHT}<<< Magenta Selected, Press Arrow Up/Down to change, Press Enter to exit to Colour Menu >>>')
                        while True:
                            if keyboard.is_pressed("up"):
                                magenta += 1
                                if magenta > 255:
                                    magenta = 255
                                time.sleep(0.025)
                                dmx.set_channel(colourchannels['magenta'], magenta)
                            if keyboard.is_pressed("down"):
                                magenta -= 1
                                if magenta < 0:
                                    magenta = 0
                                time.sleep(0.025)
                                dmx.set_channel(colourchannels['magenta'], magenta)
                            if keyboard.is_pressed("enter"):
                                time.sleep(0.5)
                                print(f'{Back.BLUE + Style.BRIGHT}<<< Exiting to colour menu >>>')
                                print(f'{Back.BLUE + Style.BRIGHT}<<< Colour Selected >>>')
                                break
                    ## Yellow Section
                    if keyboard.is_pressed("y"):
                        time.sleep(0.1)
                        print(f'{Back.BLUE + Style.BRIGHT}<<< Yellow Selected, Press Arrow Up/Down to change, Press Enter to exit to Colour Menu >>>')
                        while True:
                            if keyboard.is_pressed("up"):
                                yellow += 1
                                if yellow > 255:
                                    yellow = 255
                                time.sleep(0.025)
                                dmx.set_channel(colourchannels['yellow'], yellow)
                            if keyboard.is_pressed("down"):
                                yellow -= 1
                                if yellow < 0:
                                    yellow = 0
                                time.sleep(0.025)
                                dmx.set_channel(colourchannels['yellow'], yellow)
                            if keyboard.is_pressed("enter"):
                                time.sleep(0.5)
                                print(f'{Back.BLUE + Style.BRIGHT}<<< Exiting to colour menu >>>')
                                print(f'{Back.BLUE + Style.BRIGHT}<<< Colour Selected >>>')
                                break
            if iscto == True:
                while True:
                    if keyboard.is_pressed("t"):
                        time.sleep(0.1)
                        print(f'{Back.BLUE + Style.BRIGHT}<<< Colour Temperature (CTO) Selected, Press Arrow Up/Down to change, Press Enter to exit to Colour Menu >>> ')
                        while True:
                            if keyboard.is_pressed("up"):
                                cto += 1
                                if cto > 255:
                                    cto = 255
                                time.sleep(0.025)
                                dmx.set_channel(colourchannels['cto'], cto)
                            if keyboard.is_pressed("down"):
                                cto -= 1
                                if cto < 0:
                                    cto = 0
                                time.sleep(0.025)
                                dmx.set_channel(colourchannels['cto'], cto)
                            if keyboard.is_pressed("enter"):
                                time.sleep(0.5)
                                print(f'{Back.BLUE + Style.BRIGHT}<<< Exiting to colour menu >>>')
                                print(f'{Back.BLUE + Style.BRIGHT}<<< Colour Selected >>>')
                                break
        if keyboard.is_pressed("z"):
            time.sleep(0.1)
            print(f'{Back.BLUE + Style.BRIGHT}<<< Zoom Selected, Press Arrow Up/Down to change, Press Enter to exit to main menu >>>')
            while True:
                if keyboard.is_pressed("up"):
                    zoom += 1
                    if zoom > 255:
                        zoom = 255
                    time.sleep(0.025)
                    dmx.set_channel(beamchannels['zoom'], zoom)
                if keyboard.is_pressed("down"):
                    zoom -= 1
                    if zoom < 0:
                        zoom = 0
                    time.sleep(0.025)
                    dmx.set_channel(colourchannels['zoom'], zoom)
                if keyboard.is_pressed("enter"):
                    time.sleep(0.5)
                    print(f'{Back.BLUE + Style.BRIGHT}<<< Exiting to main menu >>>')
                    break

        if keyboard.is_pressed("f"):
            time.sleep(0.1)
            print(f'{Back.BLUE + Style.BRIGHT}<<< Focus Selected, Press Arrow Up/Down to change, Press Enter to exit to main menu >>>')
            while True:
                if keyboard.is_pressed("up"):
                    focus += 1
                    if focus > 255:
                        focus = 255
                    time.sleep(0.025)
                    dmx.set_channel(beamchannels['focus'], focus)
                if keyboard.is_pressed("down"):
                    focus -= 1
                    if focus < 0:
                        focus = 0
                    time.sleep(0.025)
                    dmx.set_channel(colourchannels['focus'], focus)
                if keyboard.is_pressed("enter"):
                    time.sleep(0.5)
                    print(f'{Back.BLUE + Style.BRIGHT}<<< Exiting to main menu >>>')
                    break

        if keyboard.is_pressed("b"):
            time.sleep(0.1)
            print(f'{Back.BLUE + Style.BRIGHT}<<< Beam Selected >>>')
            while True:
                if keyboard.is_pressed("f"):
                    time.sleep(0.1)
                    print(f'{Back.BLUE + Style.BRIGHT}<<< Frost Selected, Press Arrow Up/Down to change, Press Enter to exit to Colour Menu >>>')
                    while True:
                        if keyboard.is_pressed("up"):
                            frost += 1
                            if frost > 255:
                                frost = 255
                            time.sleep(0.05)
                            dmx.set_channel(beamchannels['frost'], frost)
                        if keyboard.is_pressed("down"):
                            frost -= 1
                            if frost < 0:
                                frost = 0
                            time.sleep(0.05)
                            dmx.set_channel(beamchannels['frost'], frost)
                        if keyboard.is_pressed("enter"):
                            time.sleep(0.5)
                            print(f'{Back.BLUE + Style.BRIGHT}<<< Exiting to beam menu >>>')
                            print(f'{Back.BLUE + Style.BRIGHT}<<< Beam Selected >>>')
                            break
                if keyboard.is_pressed("s"):
                    time.sleep(0.1)
                    print(f'{Back.BLUE + Style.BRIGHT}<<< Static Gobo Selected, Press Arrow Up/Down to change, Press Enter to exit to Colour Menu >>>')
                    while True:
                        if keyboard.is_pressed("up"):
                            static_gobo += 1
                            if static_gobo > 255:
                                static_gobo = 255
                            time.sleep(0.05)
                            dmx.set_channel(beamchannels['static_gobo'], static_gobo)
                        if keyboard.is_pressed("down"):
                            static_gobo -= 1
                            if static_gobo < 0:
                                static_gobo = 0
                            time.sleep(0.05)
                            dmx.set_channel(beamchannels['static_gobo'], static_gobo)
                        if keyboard.is_pressed("enter"):
                            time.sleep(0.5)
                            print(f'{Back.BLUE + Style.BRIGHT}<<< Exiting to beam menu >>>')
                            print(f'{Back.BLUE + Style.BRIGHT}<<< Beam Selected >>>')
                            break
                
                if keyboard.is_pressed("enter"):
                    time.sleep(0.5)
                    print(f'{Back.BLUE + Style.BRIGHT}<<< Back to Main control menu >>>')
                    break


def dmxcontrol():
    ## Make needed variables global because ceebs passing them through normally                                                  
    global fixturename
    global fixturestartchan
    global fixtureprofilename
    global profiles
    global savedfixturechan
    global numpad
    global movementchannels
    global colourchannels
    global beamchannels
    global dimmerchannels

    ## Bools
    global isconventional
    global isrgb
    global iscmy
    global iscto

    ## Saved channel values

        

## This below bit sets up all the channels from the fixture profile
## First we import movement stuff
    movementchannels = {
        'pan':       int(profiles[fixtureprofilename]['movement']['pan']) + fixturestartchan,
        'pan_fine':  int(profiles[fixtureprofilename]['movement']['pan_fine']) + fixturestartchan,
        'tilt':      int(profiles[fixtureprofilename]['movement']['tilt']) + fixturestartchan,
        'tilt_fine': int(profiles[fixtureprofilename]['movement']['tilt_fine']) + fixturestartchan,
#        'pt_speed':  int(profiles[fixtureprofilename]['movement']['pan_tilt_speed']) + fixturestartchan,
        }

## Then we import the colour data (this is fixture dependent hence the if statements)
    try:
        if 'conventional' in profiles[fixtureprofilename]['colour']:
            isconventional = True
            colourchannels = {
                'colour_wheel': int(profiles[fixtureprofilename]['colour']['conventional']['colour_wheel']) + fixturestartchan
            }
        else:
            isconventional = False
    except:
        isconventional = False

    try:
        if 'rgb' in profiles[fixtureprofilename]['colour']['led']:
            isrgb = True
            colourchannels = {
                'red':   int(profiles[fixtureprofilename]['colour']['led']['rgb']['red']) + fixturestartchan,
                'green': int(profiles[fixtureprofilename]['colour']['led']['rgb']['green']) + fixturestartchan,
                'blue':  int(profiles[fixtureprofilename]['colour']['led']['rgb']['blue']) + fixturestartchan,
            }
        else:
            isrgb = False
    except:
        isrgb = False

    try:
        if 'cmy' in profiles[fixtureprofilename]['colour']['led']:
            iscmy = True
            colourchannels = {
                'cyan':    int(profiles[fixtureprofilename]['colour']['led']['cmy']['cyan']) + fixturestartchan,
                'magenta': int(profiles[fixtureprofilename]['colour']['led']['cmy']['magenta']) + fixturestartchan,
                'yellow':  int(profiles[fixtureprofilename]['colour']['led']['cmy']['yellow']) + fixturestartchan,
            }
        else:
            iscmy = False
    except:
        iscmy = False

    try:
        if 'cto' in profiles[fixtureprofilename]['colour']:
            iscto = True
            colourchannels['cto'] = int(profiles[fixtureprofilename]['colour']['cto']) + fixturestartchan,
        else:
            iscto = False
    except:
        iscto = False

## Then we import the beam data
    beamchannels = {
        'zoom': int(profiles[fixtureprofilename]['beam']['zoom']) + fixturestartchan,
        'focus': int(profiles[fixtureprofilename]['beam']['focus']) + fixturestartchan,
        'frost': int(profiles[fixtureprofilename]['beam']['frost']) + fixturestartchan,
        'static_gobo': int(profiles[fixtureprofilename]['beam']['static_gobo']) + fixturestartchan,
        'rotating_gobo': int(profiles[fixtureprofilename]['beam']['rotating_gobo']) + fixturestartchan,
    }

## Lastly we import dimmer data
    dimmerchannels = {
        'dimmer': int(profiles[fixtureprofilename]['dimmer']['dimmer']) + fixturestartchan,
        'dimmer_fine': int(profiles[fixtureprofilename]['dimmer']['dimmer_fine']) + fixturestartchan,
    }

## List controllable channels
    print(f'{Back.WHITE + Style.BRIGHT}Index of Controllable Channels:')
    print(f'{Fore.BLUE + Style.BRIGHT}Movement Channels:')
    print('     [1->] Pan\n     [2->] Tilt\n     [3->] Movement Speed\n')
    print(f'{Fore.BLUE + Style.BRIGHT}Colour Channels:')
    if isconventional == True:
        print('     [4->] Colour Wheel')
    else:
        print(f'    [4->]{Fore.RED} Colour Wheel')
    if isrgb == True:
        print('     [5->] Red\n     [6->] Green\n     [7->] Blue')
    else:
        print(f'     [5->]{Fore.RED} Red{Fore.RESET}\n     [6->]{Fore.RED} Green{Fore.RESET}\n     [7->]{Fore.RED} Blue')
    if iscmy == True:
        print('     [8->] Cyan\n     [9->] Magenta\n     [10->] Yellow')
    else:
        print(f'     [8->] {Fore.RED}Cyan{Fore.RESET}\n     [9->] {Fore.RED}Magenta{Fore.RESET}\n     [10->] {Fore.RED}Yellow')
    if iscto == True:
        print('     [11->] CTO')
    else:
        print(f'     [11->] {Fore.RED}CTO')
    print(f'\n{Fore.BLUE + Style.BRIGHT}Beam Channels:')
    print('     [12->] Zoom\n     [13->] Focus\n     [14->] Frost\n     [15->] Static Gobo\n     [16->] Rotating Gobo\n')
    print(f'\n{Fore.BLUE + Style.BRIGHT}Dimmer Channels:')
    print('     [17->] Dimmer')

## Print Keybinds based off keyboard used
    print(f'\n{Fore.BLUE + Style.BRIGHT}Helpful Keybinds:')
    print(f'{Fore.BLUE}Movement:')
    if numpad == 'Yes' or 'Y':
        print(f'     [--] {Style.BRIGHT}Tilt: {Style.RESET_ALL}Numpad Up/Down [NUM8/NUM2]')
        print(f'     [--] {Style.BRIGHT}Pan: {Style.RESET_ALL}Numpad Left/Right [NUM4/NUM6]')
        print(f'     [--] {Style.BRIGHT}PT Speed: {Style.RESET_ALL}Numpad +/-')
    else:
        print(f'     [--] {Style.BRIGHT}Tilt: {Style.RESET_ALL}Arrow Up/Down')
        print(f'     [--] {Style.BRIGHT}Pan: {Style.RESET_ALL}Arrow Left/Right')
    print(f'{Fore.BLUE}Colour:')
    if isconventional == True:
        print(f'     [--] {Style.BRIGHT}Colour Wheel: {Style.RESET_ALL}[C]olour, [W]heel, Arrow Up/Down')
    if isrgb == True:
        print(f'     [--] {Style.BRIGHT}Red: {Style.RESET_ALL}[C]olour, [R]ed, Arrow Up/Down')
        print(f'     [--] {Style.BRIGHT}Green: {Style.RESET_ALL}[C]olour, [G]reen, Arrow Up/Down')
        print(f'     [--] {Style.BRIGHT}Blue: {Style.RESET_ALL}[C]olour, [B]lue, Arrow Up/Down')
    if iscmy == True:
        print(f'     [--] {Style.BRIGHT}Cyan: {Style.RESET_ALL}[C]olour, [C]yan, Arrow Up/Down')
        print(f'     [--] {Style.BRIGHT}Magenta: {Style.RESET_ALL}[C]olour, [M]Magenta, Arrow Up/Down')
        print(f'     [--] {Style.BRIGHT}Yellow: {Style.RESET_ALL}[C]olour, [Y]Yellow, Arrow Up/Down')
    if iscto == True:
        print(f'     [--] {Style.BRIGHT}Colour Temp: {Style.RESET_ALL}[C]olour, [T]emp, Arrow Up/Down')
    print(f'{Fore.BLUE}Beam:')
    print(f'     [--] {Style.BRIGHT}Zoom: {Style.RESET_ALL}[Z]oom, Arrow Up/Down')
    print(f'     [--] {Style.BRIGHT}Focus: {Style.RESET_ALL}[F]ocus, Arrow Up/Down')
    print(f'     [--] {Style.BRIGHT}Frost: {Style.RESET_ALL}[B]eam, [F]rost, Arrow Up/Down')
    print(f'     [--] {Style.BRIGHT}Static Gobo: {Style.RESET_ALL}[B]eam, [S]tatic Gobo, Arrow Up/Down')
    print(f'     [--] {Style.BRIGHT}Rotating Gobo: {Style.RESET_ALL}[B]eam, [R]otating Gobo, Arrow Up/Down')
    print(f'{Fore.BLUE}Dimmer:')
    print(f'     [--] {Style.BRIGHT}Dimmer: {Style.RESET_ALL}[+/-] (On Keyboard by Backspace)')


    on_press()


channel_values = {}
fixtureindex = {}
savedfixturechan = {}
flag = True
numpad = input('Do You have a NUMPAD? [Y]es or [N]o >> ')
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
    fixturestartchan = int(fixtureindex[fixturenum]['startingchannel'])
    fixtureprofilename = fixtureindex[fixturenum]['profilename']
    print(f'\n {Fore.BLUE + Style.BRIGHT}You Have Selected {fixturename}')

    pan = -1
    panfine = -1
    tilt = -1
    tiltfine = -1
    ptspeed = -1
    conventional = -1
    red = -1
    green = -1
    blue = -1
    cyan = -1
    magenta = -1
    yellow = -1
    cto = -1
    zoom = -1
    focus = -1
    frost = -1
    static_gobo = -1
    rotating_gobo = -1
    dimmer = -1
    dimmer_fine = -1

    
    dmxcontrol()
