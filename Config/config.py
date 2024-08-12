from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QSpinBox, QWizard, QWizardPage
from PySide6.QtCore import QFile, QIODevice, Qt
import time
import serial.tools.list_ports
import sys
import json
import os

global configui
global afpui
global fixtureprofiles

def savefixprof():
    ## Save Stuff to Vars
    print("Saving to Vars")
    fixname = afpui.fixname.text()
    chancount = afpui.chancount.value()
    panlimit = afpui.panlimits.value()
    tiltlimit = afpui.tiltlimits.value()
    panchan = afpui.panchan.value()
    finepanchan = afpui.finepanchan.value()
    tiltchan = afpui.tiltchan.value()
    finetiltchan = afpui.finetiltchan.value()
    ptspeedchan = afpui.ptspeedchan.value()
    if ptspeedchan == True:
        ptspeedcontrol = True
    else:
        ptspeedcontrol = False
    redchan = afpui.redchan.value()
    if redchan == True:
        redcontrol = True
    else:
        redcontrol = False
    greenchan = afpui.greenchan.value()
    if greenchan == True:
        greencontrol = True
    else:
        greencontrol = False
    bluechan = afpui.bluechan.value()
    if bluechan == True:
        bluecontrol = True
    else:
        bluecontrol = False
    cyanchan = afpui.cyanchan.value()
    if cyanchan == True:
        cyancontrol = True
    else:
        cyancontrol = False
    magentachan = afpui.magentachan.value()
    if magentachan == True:
        magentacontrol = True
    else:
        magentacontrol = False
    yellowchan = afpui.yellowchan.value()
    if yellowchan == True:
        yellowcontrol = True
    else:
        yellowcontrol = False
    colourwheelchan = afpui.colourwheelchan.value()
    if colourwheelchan == True:
        colourwheelcontrol = True
    else:
        colourwheelcontrol = False
    ctochan = afpui.ctochan.value()
    if ctochan == True:
        ctocontrol = True
    else:
        ctocontrol = False
    zoomchan = afpui.zoomchan.value()
    finezoomchan = afpui.zoomfinechan.value()
    if finezoomchan == True:
        finezoomcontrol = True
    else:
        finezoomcontrol = False
    focuschan = afpui.focuschan.value()
    finefocuschan = afpui.focusfinechan.value()
    if finefocuschan == True:
        finefocuscontrol = True
    else:
        finefocuscontrol = False
    staticgobochan = afpui.staticgobochan.value()
    rotgobochan = afpui.rotgobochan.value()
    dimmerchan = afpui.dimmerchan.value()
    finedimmerchan = afpui.finedimmerchan.value()
    if finedimmerchan == True:
        finedimmercontrol = True
    else:
        finedimmercontrol = False
    panlimit = afpui.panlimit.value()
    tiltlimit = afpui.tiltlimit.value()
    bulbwattage = afpui.bulbwattage.value()
    bulblumen = afpui.bulblumen.value()
    maxzoom = afpui.maxzoom.value()
    minzoom = afpui.minzoom.value()
    maxfocus = afpui.maxfocus.value()
    minfocus = afpui.minfocus.value()
    print("Saving to Var COMPLETE")

    ## Save to dict
    ## Real world parameters
    print("Save to dict")
    fixtureprofiles[fixname] = {}
    fixtureprofiles[fixname]['channel_count'] = chancount
    fixtureprofiles[fixname]['physical_params'] = {}
    fixtureprofiles[fixname]['physical_params']['pan_limit'] = panlimit
    fixtureprofiles[fixname]['physical_params']['tilt_limit'] = tiltlimit
    fixtureprofiles[fixname]['physical_params']['bulb_wattage'] = bulbwattage
    fixtureprofiles[fixname]['physical_params']['bulb_lumens'] = bulblumen
    fixtureprofiles[fixname]['physical_params']['max_zoom_angle'] = maxzoom
    fixtureprofiles[fixname]['physical_params']['min_zoom_angle'] = minzoom
    fixtureprofiles[fixname]['physical_params']['max_focus_angle'] = maxfocus
    fixtureprofiles[fixname]['physical_params']['min_focus_angle'] = minfocus
    ## Movement Control
    fixtureprofiles[fixname]['movement'] = {}
    fixtureprofiles[fixname]['movement']['pan'] = panchan
    fixtureprofiles[fixname]['movement']['fine_pan'] = finepanchan
    fixtureprofiles[fixname]['movement']['tilt'] = tiltchan
    fixtureprofiles[fixname]['movement']['fine_tilt'] = finetiltchan
    ## Speed Control
    if ptspeedcontrol == True:
        fixtureprofiles[fixname]['movement']['pan_tilt_speed_control'] = ptspeedchan
    else:
        fixtureprofiles[fixname]['movement']['pan_tilt_speed_control'] = 'none'
    ## RGB Control
    fixtureprofiles[fixname]['colour'] = {}
    fixtureprofiles[fixname]['colour']['rgb'] = {}
    fixtureprofiles[fixname]['colour']['cmy'] = {}
    if redcontrol == True:
        fixtureprofiles[fixname]['colour']['rgb']['red'] = redchan
    else:
        fixtureprofiles[fixname]['colour']['rgb']['red'] = 'none'
    if bluecontrol == True:
        fixtureprofiles[fixname]['colour']['rgb']['blue'] = bluechan
    else:
        fixtureprofiles[fixname]['colour']['rgb']['blue'] = 'none'
    if greencontrol == True:
        fixtureprofiles[fixname]['colour']['rgb']['green'] = greenchan
    else:
        fixtureprofiles[fixname]['colour']['rgb']['green'] = 'none'
    ## CMY Control
    if cyancontrol == True:
        fixtureprofiles[fixname]['colour']['cmy']['cyan'] = cyanchan
    else:
        fixtureprofiles[fixname]['colour']['cmy']['cyan'] = 'none'
    if magentacontrol == True:
        fixtureprofiles[fixname]['colour']['cmy']['magenta'] = magentachan
    else:
        fixtureprofiles[fixname]['colour']['cmy']['magenta'] = 'none'
    if yellowcontrol == True:
        fixtureprofiles[fixname]['colour']['cmy']['yellow'] = yellowchan
    else:
        fixtureprofiles[fixname]['colour']['cmy']['yellow'] = 'none'
    ## Colour Wheel Control
    if colourwheelcontrol == True:
        fixtureprofiles[fixname]['colour']['colour_wheel'] = colourwheelchan
    else:
        fixtureprofiles[fixname]['colour']['colour_wheel'] = 'none'
    ## CTO Control
    if ctocontrol == True:
        fixtureprofiles[fixname]['colour']['cto'] = ctochan
    else:
        fixtureprofiles[fixname]['colour']['cto'] = 'none'
    ## Zoom Control
    fixtureprofiles[fixname]['beam']
    fixtureprofiles[fixname]['beam']['zoom'] = zoomchan
    if finezoomcontrol == True:
        fixtureprofiles[fixname]['beam']['fine_zoom'] = finezoomchan
    else:
        fixtureprofiles[fixname]['beam']['fine_zoom'] = 'none'
    ## Focus Control
    fixtureprofiles[fixname]['beam']['focus'] = focuschan
    if finefocuscontrol == True:
        fixtureprofiles[fixname]['beam']['fine_focus'] = finefocuschan
    else:
        fixtureprofiles[fixname]['beam']['fine_focus'] = 'none'
    ## Gobo Control
    fixtureprofiles[fixname]['beam']['static_gobo'] =  staticgobochan
    fixtureprofiles[fixname]['beam']['rot_gobo'] = rotgobochan
    ## Dimmer
    fixtureprofiles[fixname]['dimmer'] = dimmerchan
    if finedimmercontrol == True:
        fixtureprofiles[fixname]['fine_dimmer'] = finedimmerchan
    else:
        fixtureprofiles[fixname]['fine_dimmer'] = 'none'
    print("Save to dict COMPLETE")


def afpuirun():
    afpui.show()
    afpui.button(QWizard.FinishButton).clicked.connect(savefixprof)


            

## Init section
app = QApplication(sys.argv)
loader = QUiLoader()
fixtureprofiles = {}

## Main config UI
configuifile = QFile("Config.ui")
if not configuifile.open(QIODevice.ReadOnly):
    print(f"Cannot open Config.ui: {configuifile.errorString()}")
    sys.exit(-1)
configui = loader.load(configuifile)
configuifile.close()
if not configui:
    print(loader.errorString())
    sys.exit(-1)

## Add Fixture Profile UI
afpuifile = QFile("addfixtureprofile.ui")
if not afpuifile.open(QIODevice.ReadOnly):
    print(f'Cannot open addfixtureprofile.ui: {afpuifile.errorString()}')
    sys.exit(-1)
afpui = loader.load(afpuifile)
afpuifile.close()
if not afpui:
    print(loader.errorString)
    sys.exit

## Load previous fixture profiles (if there are any)
try:
    with open('profiles.json', 'r') as file:         
        fixtureprofiles = json.load(file)
    print("Fixture profile database found and loaded")
except:
    print("No Fixture Profile Database found, This is normal on new installs")


## Main Routine
configui.show()                                         ## Show configui


## Adapter Tree
adatree = configui.adapterselect
items = []
for port in serial.tools.list_ports.comports():
    if port.device.startswith('/dev/ttyUSB'):               ## Only add USB serial devices 
        item = QTreeWidgetItem([port.device])
        item.setText(1, str(port.description) + " by " + str(port.manufacturer))
        items.append(item)    
adatree.insertTopLevelItems(0, items)

configui.addfixtureprofile.clicked.connect(afpuirun)


app.exec()
adatport = configui.adatpath.text()
chanreq = configui.ChannelReq.value()
adatspeed = configui.speedenter.value()
if adatspeed == True:
    manspeed = True
else:
    manspeed = False


sys.exit

   
