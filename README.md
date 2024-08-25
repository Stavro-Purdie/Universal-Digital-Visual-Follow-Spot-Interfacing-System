# Universal-Digital-Visual-Follow-Spot-Interfacing-System
This project aims to create a visually appealing way to control moving spotlights as followspots with multiple webcams, raspberry pis, RS485 based DMX adapters (DMXking, ENTTEC) and a main processing server (With a NVIDIA GPU)
The project will do this through:
 --> User Interaction >> Either using full manual or ML assisted tracking (Select the person you want to track)
 --> IR Tracking >> Through the use of IR tags
 --> Real time machine learning >> Using photos of the performer aswell as real time tracking
 
The project is currently in a Pre-Alpha phase, the code is always changing sometimes for the worst.
The Keyboard function works, with patching and fixture profiles HOWEVER they are about to be superseded (Check out GUI Branch).

THIS PROGRAM IS DESIGNED TO ONLY BE RAN ON LINUX

In order to run the program first clone the repo:
    `git clone https://github.com/Stavro-Purdie/Universal-Digital-Visual-Follow-Spot-Interfacing-System.git`

Then install all python pre-requesites:
    Linux: `pip3 -r install requirements.txt`

Then navigate to the 'First Time Setup' directory:
    Linux: `cd 'Universal*/Config'`

Then connect your adapter to the computer, run `config.py`:
    Linux: `python3 config.py`


Now the system is fully setup. To run return to the main directory:
    Linux: `cd ..`

If you want to trial the GUI, you will need to clone the MAIN-GUI Branch, It works with cameras etc, however it cannot control/output any DMX
