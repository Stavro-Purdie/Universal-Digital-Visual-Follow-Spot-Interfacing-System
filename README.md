# Universal-Digital-Visual-Follow-Spot-Interfacing-System
This project aims to create a visually appealing way to control moving spotlights as followspots with multiple webcams, raspberry pis and RS485 based DMX adapters (DMXking, ENTTEC)

The project is currently in a Pre-Alpha phase.
The Keyboard function works, Fixture profiles have not been integrated yet.


In order to run the program first clone the repo:
    `git clone https://github.com/Stavro-Purdie/Universal-Digital-Visual-Follow-Spot-Interfacing-System.git`

Then navigate to the 'First Time Setup' directory:
    Linux: `cd 'Universal*/First Time Setup'`

Then connect your adapter to the computer, run `adaptersetup.py`:
    Linux: `python3 adaptersetup.py`

After this you will need to create a fixture library, run `fixturelibrarysetup.py`:
    Linux: `python3 fixturelibrarysetup.py`

Now the system is fully setup. To run return to the main directory:
    Linux: `cd ..`

And run `dmxkeyboard.py`:
    Linux: `python3 dmxkeyboard.py`

To add another fixture, run `addfixture.py`
    Linux: `python3 addfixture.py`

If your adapter serial port changes, rerun the adapter setup script in `/First Time Setup`

