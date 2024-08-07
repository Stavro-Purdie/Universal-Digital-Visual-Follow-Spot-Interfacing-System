import os
import time
from colorama import init, Fore, Style, Cursor, Back
import subprocess

init(autoreset=True)

print(f'{Style.BRIGHT}Welcome to the setup script for the Universal Digital Visual Follow Spot Interfacing System (UDVFSIS)')
time.sleep(2)

print(f"{Fore.RED + Style.BRIGHT}This software is in EARLY ALPHA, Please report any bugs to the github page\n")
print(f'{Fore.BLUE + Style.BRIGHT}Starting the Adapter Configurator...')
time.sleep(2)
try:
    print(f'{Fore.GREEN + Style.BRIGHT}Adapter Configurator Started')
    subprocess.call('sudo python3 Setup/adaptersetup.py', shell=True)

except:
    print(f'{Fore.RED + Style.BRIGHT}[XX] SCRIPT ERROR HAS OCCURRED\n')
    time.sleep(2)
    print(f'    [--] Please ensure that you are running this program as a {Style.BRIGHT}ROOT user')
    print(f'    [--] {Style.BRIGHT}If this program has been modified, please reinstall\n')
    time.sleep(2)
    print(f'{Fore.RED}The program will now exit as an unrecoverable exception has occured. {Style.BRIGHT}ALL DATA HAS BEEN SAVED')
    quit()

print(f'{Fore.GREEN + Style.BRIGHT}Adapter Configurator Completed Successfully')
time.sleep(1)

print(f'{Fore.BLUE + Style.BRIGHT}Starting the Fixture Library First Time Configurator...')
time.sleep(4)

try:
    print(f'{Fore.GREEN + Style.BRIGHT}Fixture Library First Time Configurator Started')
    subprocess.call('sudo python3 Setup/fixturelibrarysetup.py', shell=True)
except:
    print(f'{Fore.RED + Style.BRIGHT}[XX] SCRIPT ERROR HAS OCCURRED\n')
    time.sleep(2)
    print(f'    [--] Please ensure that you are running this program as a {Style.BRIGHT}ROOT user')
    print(f'    [--] {Style.BRIGHT}If this program has been modified, please reinstall\n')
    time.sleep(2)
    print(f'{Fore.RED}The program will now exit as an unrecoverable exception has occured. {Style.BRIGHT}ALL DATA HAS BEEN SAVED')
    quit()

print(f'{Fore.BLUE + Style.BRIGHT}DMX Virtual Patch Configuraton Wizard....')
time.sleep(4)

try:
    print(f'{Fore.GREEN + Style.BRIGHT}DMX Virtual Patch Configuraton Wizard Started')
    subprocess.call('sudo python3 Setup/dmxpatchsetup.py', shell=True)
except:
    print(f'{Fore.RED + Style.BRIGHT}[XX] SCRIPT ERROR HAS OCCURRED\n')
    time.sleep(2)
    print(f'    [--] Please ensure that you are running this program as a {Style.BRIGHT}ROOT user')
    print(f'    [--] {Style.BRIGHT}If this program has been modified, please reinstall\n')
    time.sleep(2)
    print(f'{Fore.RED}The program will now exit as an unrecoverable exception has occured. {Style.BRIGHT}ALL DATA HAS BEEN SAVED')
    quit()

print(f'{Fore.GREEN + Style.BRIGHT}The First Time Setup Script has completed successfully')
print(f"    [--] {Style.BRIGHT}If you need to change adapter settings please navigate to 'Setup/' and run 'adaptersetup.py'")
print(f"    [--] {Style.BRIGHT}If you need to add fixtures to the Fixture Library, please run 'addfixture.py'")
print(f"    [--] {Style.BRIGHT}If you need to change the patch panel, please run the 'dmxpatchedit.py' program")
print(f"    [--] {Style.BRIGHT}If you need to factory reset the program, Rerun this script")
time.sleep(5)
print(f'{Fore.BLUE + Style.BRIGHT}The Program will now exit')
quit()