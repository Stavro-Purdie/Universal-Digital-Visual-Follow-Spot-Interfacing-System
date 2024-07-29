## Property of Stavro Purdie, 2024
## This program is set up to control a fixture of the user's choosing with the keyboard.
import configparser
from DMXEnttecPro import Controller
import time
import json
from pynput.keyboard import *
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
    if numpad == 'Yes' or 'Y':
        if str(key) == "'8'":                                                   #If Up Arrow Key Pressed...
            tilt += 1                                                     #Add 1 to the channel val
            dmx.set_channel(movementchannels['tilt'], tilt)                                #Run DMX Frame Through DMX Subsystem
        if str(key) == "'2'":
            tilt -= 1
            dmx.set_channel(movementchannels['tilt'], tilt)
        if str(key) == "'6'":
            pan += 1
            dmx.set_channel(movementchannels['pan'], pan)
        if str(key) == "'4'":
            pan -= 1
            dmx.set_channel(movementchannels['pan'], pan)
    else:
        if key == Key.up:
            tilt += 1
            dmx.set_channel(movementchannels['tilt'], tilt)
        if key == Key.down:
            tilt -= 1
            dmx.set_channel(movementchannels['tilt'], tilt)
        if key == Key.right:
            pan += 1
            dmx.set_channel(movementchannels['pan'], pan)
        if key == Key.left:
            pan -= 1
            dmx.set_channel(movementchannels['pan'], pan)

    if isconventional == True:
        if str(key) == "'c'" or "'C'":
            print(f'{Style.BRIGHT}Colour Selected:')
            if key == Key.enter:
                print(f'{Fore.BLUE}RETURNING TO THE MAIN CONTROL SURFACE...')
            if str(key) == "'w'" or "'W'":
                print(f'{Back.BLUE, Style.BRIGHT}<<< Colour Wheel Selected [Arrow Up/Down] >>>')
                if key == Key.enter:
                    print(f'{Fore.BLUE}RETURNING TO THE MAIN CONTROL SURFACE...')
                if key == Key.up:
                    conventional += 1
                    dmx.set_channel(colourchannels['colour_wheel'], conventional)
                if key == Key.down:
                    conventional -= 1
                    dmx.set_channel(colourchannels['colour_wheel'], conventional)

    if isrgb == True:
        if str(key) == "'c'" or "'C'":
            print(f'{Style.BRIGHT}Colour Selected:')
            if key == Key.enter:
                print(f'{Fore.BLUE}RETURNING TO THE MAIN CONTROL SURFACE...')
            if str(key) == "'r'" or "'R'":
                print(f'{Back.BLUE, Style.BRIGHT}<<< Red Selected [Arrow Up/Down] >>>')
                if key == Key.enter:
                    print(f'{Fore.BLUE}RETURNING TO THE MAIN CONTROL SURFACE...')
                if key == Key.up:
                    red += 1
                    dmx.set_channel(colourchannels['red'], red)
                if key == Key.down:
                    red -= 1
                    dmx.set_channel(colourchannels['red'], red)
            if str(key) == "'g'" or "'G'":
                print(f'{Back.BLUE, Style.BRIGHT}<<< Green Selected [Arrow Up/Down] >>>')
                if key == Key.enter:
                    print(f'{Fore.BLUE}RETURNING TO THE MAIN CONTROL SURFACE...')
                if key == Key.up:
                    green += 1
                    dmx.set_channel(colourchannels['green'], green)
                if key == Key.down:
                    green -= 1
                    dmx.set_channel(colourchannels['green'], green)
            if str(key) == "'b'" or "'B'":
                print(f'{Back.BLUE, Style.BRIGHT}<<< Blue Selected [Arrow Up/Down] >>>')
                if key == Key.enter:
                    print(f'{Fore.BLUE}RETURNING TO THE MAIN CONTROL SURFACE...')
                if key == Key.up:
                    blue += 1
                    dmx.set_channel(colourchannels['blue'], blue)
                if key == Key.down:
                    blue -= 1
                    dmx.set_channel(colourchannels['blue'], blue)
    
    if iscmy == True:
        if str(key) == "'c'" or "'C'":
            print(f'{Style.BRIGHT}Colour Selected:')
            if key == Key.enter:
                print(f'{Fore.BLUE}RETURNING TO THE MAIN CONTROL SURFACE...')
            if str(key) == "'c'" or "'C'":
                print(f'{Back.BLUE, Style.BRIGHT}<<< Cyan Selected [Arrow Up/Down] >>>')
                if key == Key.enter:
                    print(f'{Fore.BLUE}RETURNING TO THE MAIN CONTROL SURFACE...')
                if key == Key.up:
                    cyan += 1
                    dmx.set_channel(colourchannels['cyan'], cyan)
                if key == Key.down:
                    cyan -= 1
                    dmx.set_channel(colourchannels['cyan'], cyan)
            if str(key) == "'m'" or "'M'":
                print(f'{Back.BLUE, Style.BRIGHT}<<< Magenta Selected [Arrow Up/Down] >>>')
                if key == Key.enter:
                    print(f'{Fore.BLUE}RETURNING TO THE MAIN CONTROL SURFACE...')
                if key == Key.up:
                    magenta += 1
                    dmx.set_channel(colourchannels['magenta'], magenta)
                if key == Key.down:
                    magenta -= 1
                    dmx.set_channel(colourchannels['magenta'], magenta)
            if str(key) == "'y'" or "'Y'":
                print(f'{Back.BLUE, Style.BRIGHT}<<< Yellow Selected [Arrow Up/Down] >>>')
                if key == Key.enter:
                    print(f'{Fore.BLUE}RETURNING TO THE MAIN CONTROL SURFACE...')
                if key == Key.up:
                    yellow += 1
                    dmx.set_channel(colourchannels['yellow'], yellow)
                if key == Key.down:
                    yellow -= 1
                    dmx.set_channel(colourchannels['yellow'], yellow)
    
    if iscto == True:
        if str(key) == "'c'" or "'C'":
            print(f'{Style.BRIGHT}Colour Selected:')
            if key == Key.enter:
                print(f'{Fore.BLUE}RETURNING TO THE MAIN CONTROL SURFACE...')
            if str(key) == "'t'" or "'T'":
                print(f'{Back.BLUE, Style.BRIGHT}<<< Colour Temperature Selected [Arrow Up/Down] >>>')
                if key == Key.enter:
                    print(f'{Fore.BLUE}RETURNING TO THE MAIN CONTROL SURFACE...')
                if key == Key.up:
                    cto += 1
                    dmx.set_channel(colourchannels['cto'], cto)
                if key == Key.down:
                    cto -= 1
                    dmx.set_channel(colourchannels['cto'], cto)
    
    if str(key) == "'z'" or "'Z'":
        print(f'{Back.BLUE, Style.BRIGHT}<<< Zoom Selected [Arrow Up/Down] >>>')
        if key == Key.enter:
            print(f'{Fore.BLUE}RETURNING TO THE MAIN CONTROL SURFACE...')
        if key == Key.up:
            zoom += 1
            dmx.set_channel(beamchannels['zoom'], zoom)
        if key == Key.down:
            zoom -= 1
            dmx.set_channel(beamchannels['zoom'], zoom)
    
    if str(key) == "'f'" or "'F'":
        print(f'{Back.BLUE, Style.BRIGHT}<<< Focus Selected [Arrow Up/Down] >>>')
        if key == Key.enter:
            print(f'{Fore.BLUE}RETURNING TO THE MAIN CONTROL SURFACE...')
        if key == Key.up:
            focus += 1
            dmx.set_channel(beamchannels['focus'], focus)
        if key == Key.down:
            focus -= 1
            dmx.set_channel(beamchannels['focus'], focus)
    
    if str(key) == "'b'" or "'B'":
        print(f'{Style.BRIGHT}Beam Selected')
        if key == Key.enter:
            print(f'{Fore.BLUE}RETURNING TO THE MAIN CONTROL SURFACE...')
        if str(key) == "'f'" or "'F'":
            print(f'{Back.BLUE, Style.BRIGHT}<<< Frost Selected [Arrow Up/Down] >>>')
            if key == Key.enter:
                print(f'{Fore.BLUE}RETURNING TO THE MAIN CONTROL SURFACE...')
            if key == Key.up:
                frost += 1
                dmx.set_channel(beamchannels['frost'], frost)
            if key == Key.down:
                frost -= 1
                dmx.set_channel(beamchannels['frost'], frost)
        if str(key) == "'s'" or "'S'":
            print(f'{Back.BLUE, Style.BRIGHT}<<< Static Gobo Selected [Arrow Up/Down] >>>')
            if key == Key.enter:
                print(f'{Fore.BLUE}RETURNING TO THE MAIN CONTROL SURFACE...')
            if key == Key.up:
                static_gobo += 1
                dmx.set_channel(beamchannels['static_gobo'], static_gobo)
            if str(key) == Key.down:
                static_gobo -= 1
                dmx.set_channel(beamchannels['static_gobo'], static_gobo)
        if str(key) == "'r'" or "'R'":
            print(f'{Back.BLUE, Style.BRIGHT}<<< Rotating Gobo Selected [Arrow Up/Down] >>>')
            if key == Key.enter:
                print(f'{Fore.BLUE}RETURNING TO THE MAIN CONTROL SURFACE...')
            if str(key) == Key.up:
                rotating_gobo += 1
                dmx.set_channel(beamchannels['rotating_gobo'], rotating_gobo)
            if str(key) == Key.down:
                rotating_gobo -= 1
                dmx.set_channel(beamchannels['rotating_gobo'], rotating_gobo)

    if str(key) == "'='" or "'+'":
        dimmer += 1
        dmx.set_channel(dimmerchannels['dimmer'], dimmer)
    if str(key) == "'-'" or "'_'":
        dimmer -= 1
        dmx.set_channel(dimmerchannels['dimmer'], dimmer)
    
    if key == Key.esc:
        print(f'{Fore.GREEN}Saving Channel Values...')
        print(f'{Fore.BLUE}Returning you to the Channel Selector...')
        print()
        Listener.stop()
        return

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


    with Listener(on_press=on_press) as listener:
        listener.join()


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

    pan = 0
    panfine = 0
    tilt = 0
    tiltfine = 0
    ptspeed = 0
    conventional = 0
    red = 0
    green = 0
    blue = 0
    cyan = 0
    magenta = 0
    yellow = 0
    cto = 0
    zoom = 0
    focus = 0
    frost = 0
    static_gobo = 0
    rotating_gobo = 0
    dimmer = 0
    dimmer_fine = 0

    
    dmxcontrol()
