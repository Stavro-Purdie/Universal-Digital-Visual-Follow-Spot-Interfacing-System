##Property of Stavro Purdie, 2024
import json
import os

confirm = input("WARNING! | This program resets your entire fixture config file. To continue, please type 'YES' otherwise press ENTER for exit >> ")
if confirm == '':
    print('Fixture Profile First Time Configurator Exiting, No settings have been changed')
    quit()

def fixturesetup():
    profiles = {}
    print('FIXTURE PROFILE FIRST TIME CONFIGURATOR')
    print("Advice for the misled. THIS PROGRAM IS ONLY FOR USE WITH MOVING SPOTS (not just any moving head or old bro's chinese PAR64)")

    fixturecount = int(input('Enter how many fixture profiles you want to initially add to the system >> '))
    i = 1
    for fixture in range(fixturecount):
        profilename = input(f"Enter name for fixture {i} of {fixturecount} with any whitespaces replaced with '-' >> ")

        print('Movement Parameter Config:\n')
        pan = input('Enter Pan Channel >> ')
        panfine = input('Enter Fine Pan Channel >> ')
        tilt = input('Enter Tilt Channel >> ')
        tiltfine = input('Enter Fine Tilt Channel >> ')
        ptspeed = input('Enter Pan Tilt Speed Channel >> ')

        print('Colour Parameter Config:\n')
        print(f"Does fixture {profilename} use a Color Wheel or have LED Colour Changing?")
        colsel = input("Enter '1' for Colour Wheel or '2' for LED Colour Changing >> ")
        if colsel == '1':
            print('Colour Wheel Selected:')
            colwhl = input('Enter Colour Wheel Channel >> ')
        if colsel == '2':
            print('LED Colour Changing Selected:')
            print(f'Does fixture {profilename} use RGB or CMY Colour Systems?')
            method = input("Enter '1' for RGB, '2' for CMY >> ")
            if method == '1':
                print('RGB Selected')
                red = input('Enter Red Channel >> ')
                green = input('Enter Green Channel >> ')
                blue = input('Enter Blue Channel >> ')
            if method == '2':
                print('CMY Selected:')
                cyan = input('Enter Cyan Channel >> ')
                magenta = input('Enter Magenta Channel >> ')
                yellow = input('Enter Yellow Channel >>')
        print('Does the fixture have CTO (Colour Temp) Control?')
        ctosel = input("Enter '1' for NO, '2' for YES >> ")
        if ctosel == '2':
            cto = input('Enter CTO Channel >> ')
        
        print('Beam Parameter Config:\n')
        zoom = input('Enter Zoom Channel >> ')
        focus = input('Enter Focus Channel >> ')
        frost = input('Enter Frost Channel >> ')
        staticgobo = input('Enter Static Gobo Channel >> ')
        rotgobo = input('Enter Rotating Gobo Channel >> ')

        print('Dimmer Parameter Config:\n')
        dimmer = input('Enter Dimmer Channel >> ')
        dimmerfine = input('Enter Fine Dimmer Channel >> ')


        print(f'Settings Entered for fixture {profilename}:')
        print(f'Movment Parameters:\n Pan: {pan}\n Fine Pan: {panfine}\n Tilt: {tilt}\n Tilt Fine: {tiltfine}\n Movement Speed Adj: {ptspeed}')
        print(f'Colour Parameters:')
        if colsel == '1':
            print(f' Colour Wheel: {colwhl}')
        if colsel == '2':
            print('LED Colour Channels:')
            if method == '1':
                print(f' Red: {red}\n Green: {green}\n Blue: {blue}')
            if method == '2':
                print(f' Cyan: {cyan}\n Magenta: {magenta}\n Yellow: {yellow}')
        if ctosel == '2':
            print(f' CTO: {cto}')
        print(f'Beam Parameters: \n Zoom: {zoom}\n Focus: {focus}\n Frost: {frost}\n Static Gobo: {staticgobo}\n Rotating Gobo (No rotate function): {rotgobo}\n')
        print(f'Dimmer Parameters: \n Dimmer: {dimmer} \n Fine Dimmer {dimmerfine}\n')

        profiles[profilename] = {}
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

if __name__ == "__main__":
    fixturesetup()

print('The Fixture Profile First Time Configurator has finished, to add more fixtures to the system in the future please run the addfixture.py program.')