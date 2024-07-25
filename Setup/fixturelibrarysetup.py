##Property of Stavro Purdie, 2024
## This file creates the fixture library.
import json
import os
from colorama import init, Fore, Style, Cursor, Back
import time

init(autoreset=True)

print(f'{Fore.BLUE + Style.BRIGHT}Fixture Configuration Utility Starting....\n \n')
time.sleep(3)

confirm = input(f"{Fore.RED + Style.BRIGHT}WARNING! | This program resets your entire fixture profile library. To continue, please type 'YES' otherwise press ENTER for exit >> ")
print('\n')
if confirm == '':
    print(f'{Fore.GREEN}Fixture Profile First Time Configurator Exiting,{Style.BRIGHT} No settings have been changed')
    quit()

def fixturesetup():
    profiles = {}
    print(f'{Style.BRIGHT}FIXTURE PROFILE FIRST TIME CONFIGURATOR')
    print(f"{Fore.RED}Advice for the misled. THIS PROGRAM IS ONLY FOR USE WITH MOVING SPOTS (not just any moving head or old bro's chinese PAR64)\n")
    time.sleep(2)

    fixturecount = int(input(f'{Fore.YELLOW + Style.BRIGHT}Enter how many fixture profiles you want to initially add to the system >> '))
    print('')
    i = 1
    for fixture in range(fixturecount):
        profilename = input(f"{Fore.YELLOW + Style.BRIGHT}Enter name for fixture {i} of {fixturecount} with any whitespaces replaced with '-' >> ")
        chancount = input(f'{Fore.YELLOW + Style.BRIGHT}How many channels does fixture {profilename} use eg 30 >> ')
        print('')

        print(f'{Fore.BLUE + Style.BRIGHT}Movement Parameter Config:')
        pan = input('Enter Pan Channel >> ')
        panfine = input('Enter Fine Pan Channel >> ')
        tilt = input('Enter Tilt Channel >> ')
        tiltfine = input('Enter Fine Tilt Channel >> ')
        ptspeed = input('Enter Pan Tilt Speed Channel >> ')

        print('')
        print(f'{Fore.BLUE + Style.BRIGHT}Colour Parameter Config:')
        print(f"{Style.BRIGHT}Does fixture {profilename} use a Color Wheel or have LED?")
        colsel = input("Enter '1' for Colour Wheel or '2' for LED >> ")
        if colsel == '1':
            print(f'{Fore.GREEN + Style.BRIGHT}Colour Wheel Selected:')
            colwhl = input('Enter Colour Wheel Channel >> ')
        if colsel == '2':
            print(f'{Fore.GREEN + Style.BRIGHT}LED Selected:')
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
        
        print(f'{Fore.BLUE + Style.BRIGHT}Beam Parameter Config:\n')
        zoom = input('Enter Zoom Channel >> ')
        focus = input('Enter Focus Channel >> ')
        frost = input('Enter Frost Channel >> ')
        staticgobo = input('Enter Static Gobo Channel >> ')
        rotgobo = input('Enter Rotating Gobo Channel >> ')

        print(f'{Fore.BLUE + Style.BRIGHT}Dimmer Parameter Config:\n')
        dimmer = input('Enter Dimmer Channel >> ')
        dimmerfine = input('Enter Fine Dimmer Channel >> ')


        print(f'{Fore.BLUE + Style.BRIGHT}Settings Entered for fixture {profilename}:')
        print(f'{Style.BRIGHT}Channel Count:{Style.RESET_ALL} {chancount} Channels')
        print(f'{Style.BRIGHT}Movment Parameters:{Style.RESET_ALL}\n Pan: {pan}\n Fine Pan: {panfine}\n Tilt: {tilt}\n Tilt Fine: {tiltfine}\n Movement Speed Adj: {ptspeed}')
        print(f'{Style.BRIGHT}Colour Parameters:')
        if colsel == '1':
            print(f' Colour Wheel: {colwhl}')
        if colsel == '2':
            print(f'{Style.BRIGHT}LED Colour Channels:')
            if method == '1':
                print(f' Red: {red}\n Green: {green}\n Blue: {blue}')
            if method == '2':
                print(f' Cyan: {cyan}\n Magenta: {magenta}\n Yellow: {yellow}')
        if ctosel == '2':
            print(f' {Style.BRIGHT}CTO:{Style.RESET_ALL} {cto}')
        print(f'{Style.BRIGHT}Beam Parameters:{Style.RESET_ALL} \n Zoom: {zoom}\n Focus: {focus}\n Frost: {frost}\n Static Gobo: {staticgobo}\n Rotating Gobo (No rotate function): {rotgobo}\n')
        print(f'{Style.BRIGHT}Dimmer Parameters:{Style.RESET_ALL} \n Dimmer: {dimmer} \n Fine Dimmer {dimmerfine}\n')

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


    path = 'Config'
    os.chdir(path)
    with open('profiles.json', 'w') as convert_file: 
        convert_file.write(json.dumps(profiles, indent=4))

fixturesetup()

print(f'{Fore.GREEN + Style.BRIGHT}The Fixture Profile First Time Configurator has finished, to add more fixtures to the system in the future please run the addfixture.py program.')