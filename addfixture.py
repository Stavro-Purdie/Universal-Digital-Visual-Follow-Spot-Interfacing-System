## Property of Stavro Purdie, 2024
## This program adds a fixture to the Fixture Library.
import json
import os
import time
from colorama import init, Fore, Style, Cursor, Back
init(autoreset=True)

## Main function (pretty much the whole program)
def fixturesetup():
    ## Load existing profiles.json file, however if this fails, leave a couple tips.
    try:
        os.chdir('Config')
        with open('profiles.json', 'r') as file:         
            profiles = json.load(file)
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

    ## Just a litte PSA
    print(f'{Style.BRIGHT}FIXTURE PROFILE CONFIGURATION WIZARD')
    print(f"{Fore.RED}Advice for the misled. THIS PROGRAM IS ONLY FOR USE WITH MOVING SPOTS (not just any moving head or old bro's chinese PAR64)\n") 
    time.sleep(2)

    ## A Basic question
    fixturecount = int(input(f'{Fore.YELLOW + Style.BRIGHT}Enter how many fixture profiles you want to add to the system >> '))
    i = 1
    for fixture in range(fixturecount):
        ## Some basic fixture parameters
        profilename = input(f"{Fore.YELLOW + Style.BRIGHT}Enter name for fixture {i} of {fixturecount} with any whitespaces replaced with '-' >> ")
        chancount = input(f'{Fore.YELLOW + Style.BRIGHT}Enter how many channels fixture {profilename} uses eg 30 >> ')
        print('')

        ## The business side of the program, ask the user for the profile values
        print(f'{Fore.BLUE + Style.BRIGHT}Movement Parameter Config:')
        pan = input('Enter Pan Channel >> ')
        panfine = input('Enter Fine Pan Channel >> ')
        tilt = input('Enter Tilt Channel >> ')
        tiltfine = input('Enter Fine Tilt Channel >> ')
        ptspeed = input('Enter Pan Tilt Speed Channel >> ')

        print('')
        print(f'{Fore.BLUE + Style.BRIGHT}Colour Parameter Config:')
        print(f"{Style.BRIGHT}Does fixture {profilename} use a Color Wheel or have LED Colour Changing?")
        colsel = input("Enter '1' for Colour Wheel or '2' for LED Colour Changing >> ")
        if colsel == '1':
            print(f'{Fore.GREEN + Style.BRIGHT}Colour Wheel Selected:')
            colwhl = input('Enter Colour Wheel Channel >> ')
        if colsel == '2':
            print(f'{Fore.GREEN + Style.BRIGHT}LED Colour Changing Selected:')
            print(f'{Style.BRIGHT}Does fixture {profilename} use RGB or CMY Colour Systems?')
            method = input("Enter '1' for RGB, '2' for CMY >> ")
            if method == '1':
                print(f'{Fore.GREEN + Style.BRIGHT}RGB Selected')
                red = input('Enter Red Channel >> ')
                green = input('Enter Green Channel >> ')
                blue = input('Enter Blue Channel >> ')
            if method == '2':
                print(f'{Fore.GREEN + Style.BRIGHT}CMY Selected:')
                cyan = input('Enter Cyan Channel >> ')
                magenta = input('Enter Magenta Channel >> ')
                yellow = input('Enter Yellow Channel >>')
        print(f'{Style.BRIGHT}Does the fixture have CTO (Colour Temp) Control?')
        ctosel = input("Enter '1' for NO, '2' for YES >> ")
        if ctosel == '2':
            print(f'{Fore.GREEN + Style.BRIGHT}CTO selected:')
            cto = input('Enter CTO Channel >> ')
        
        print('')
        print(f'{Fore.BLUE + Style.BRIGHT}Beam Parameter Config:')
        zoom = input('Enter Zoom Channel >> ')
        focus = input('Enter Focus Channel >> ')
        frost = input('Enter Frost Channel >> ')
        staticgobo = input('Enter Static Gobo Channel >> ')
        rotgobo = input('Enter Rotating Gobo Channel >> ')

        print('')
        print(f'{Fore.BLUE + Style.BRIGHT}Dimmer Parameter Config:')
        dimmer = input('Enter Dimmer Channel >> ')
        dimmerfine = input('Enter Fine Dimmer Channel >> ')

        ## Present the user with a nice looking sum of all the fixture profiles entered
        print(f'{Fore.BLUE + Style.BRIGHT}Settings Entered for fixture {profilename}:')
        print(f'{Style.BRIGHT}Channel Count:{Style.RESET_ALL} {chancount} Channels')
        print(f'{Style.BRIGHT}Movment Parameters:{Style.RESET_ALL}\n Pan: {pan}\n Fine Pan: {panfine}\n Tilt: {tilt}\n Tilt Fine: {tiltfine}\n Movement Speed Adj: {ptspeed}')
        print(f'{Style.BRIGHT}Colour Parameters:')
        if colsel == '1':
            print(f'Colour Wheel: {colwhl}')
        if colsel == '2':
            print(f'{Style.BRIGHT}LED Colour Channels:')
            if method == '1':
                print(f'Red: {red}\n Green: {green}\n Blue{blue}')
            if method == '2':
                print(f'Cyan: {cyan}\n Magenta: {magenta}\n Yellow: {yellow}')
        if ctosel == '2':
            print(f'CTO: {cto}')
        print(f'{Style.BRIGHT}Beam Parameters:{Style.RESET_ALL} \n Zoom: {zoom}\n Focus: {focus}\n Frost: {frost}\n Static Gobo: {staticgobo}\n Rotating Gobo (No rotate function): {rotgobo}\n')
        print(f'{Style.BRIGHT}Dimmer Parameters:{Style.RESET_ALL} \n Dimmer: {dimmer} \n Fine Dimmer {dimmerfine}\n')

        ## Place all of these new values into a nested dictionary
        profiles[profilename] = {}
        profiles[profilename]['channel_count'] = chancount
        profiles[profilename]['movement'] = {}
        profiles[profilename]['movement']['pan'] = pan
        profiles[profilename]['movement']['pan_fine'] = panfine
        profiles[profilename]['movement']['tilt'] = tilt
        profiles[profilename]['movement']['tilt_fine'] = tiltfine
        profiles[profilename]['movement']['pan_tilt_speed'] = ptspeed
        if colsel == '1':
            profiles[profilename]['colour'] = {}
            profiles[profilename]['colour']['conventional'] = {}
            profiles[profilename]['colour']['conventional']['colour_wheel'] = colwhl
        if colsel == '2':
            if method == '1':
                profiles[profilename]['colour'] = {}
                profiles[profilename]['colour']['led'] = {}
                profiles[profilename]['colour']['led']['rgb'] = {}
                profiles[profilename]['colour']['led']['rgb']['red'] = red
                profiles[profilename]['colour']['led']['rgb']['green'] = green
                profiles[profilename]['colour']['led']['rgb']['blue'] = blue
            if method == '2':
                profiles[profilename]['colour'] = {}
                profiles[profilename]['colour']['led'] = {}
                profiles[profilename]['colour']['led']['cmy'] = {}
                profiles[profilename]['colour']['led']['cmy']['cyan'] = cyan
                profiles[profilename]['colour']['led']['cmy']['magenta'] = magenta
                profiles[profilename]['colour']['led']['cmy']['yellow'] = yellow
        if ctosel == '2':
            profiles[profilename]['colour']['cto'] = cto
        profiles[profilename]['beam'] = {}
        profiles[profilename]['beam']['zoom'] = zoom
        profiles[profilename]['beam']['focus'] = focus
        profiles[profilename]['beam']['frost'] = frost
        profiles[profilename]['beam']['static_gobo'] = staticgobo
        profiles[profilename]['beam']['rotating_gobo'] = rotgobo
        profiles[profilename]['dimmer'] = {}
        profiles[profilename]['dimmer']['dimmer'] = dimmer
        profiles[profilename]['dimmer']['dimmer_fine'] = dimmerfine

    ## This overwrites the nested dictionary to profiles.json for easy manual editing
    print(f"{Fore.BLUE + Style.BRIGHT}Saving profiles to 'profiles.json'....")
    with open('profiles.json', 'w') as convert_file: 
        convert_file.write(json.dumps(profiles, indent=4))
        
    print(f'{Fore.GREEN + Style.BRIGHT}The Fixture Profile Configuration Wizard has finished, to add more fixtures to the system in the future, rerun this program.')

fixturesetup()