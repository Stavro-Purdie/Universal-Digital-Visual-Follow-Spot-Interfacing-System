from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QSpinBox, QWizard, QWizardPage
from PySide6.QtCore import QFile, QIODevice, Qt
import time
import serial.tools.list_ports
import sys
import json
import os
import configparser

global configui
global afpui
global fixtureprofiles
global fixturepatch
global adatvalues

## Functions
# This function saves all the new fixture profiles to the dictionary
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
    fixtureprofiles[fixname]['beam'] = {}
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
    fixtureprofiles[fixname]['dimmer'] = {}
    fixtureprofiles[fixname]['dimmer'] = dimmerchan
    if finedimmercontrol == True:
        fixtureprofiles[fixname]['fine_dimmer'] = finedimmerchan
    else:
        fixtureprofiles[fixname]['fine_dimmer'] = 'none'
    print("Save to dict COMPLETE")
    
    ## Update Fixture Tree View in configui
    ## Generate data
    def add_children(item, value):
        if isinstance(value, dict):
            for key, val in value.items():
                child = QTreeWidgetItem([key])
                item.addChild(child)
                add_children(child, val)
        else:
            child = QTreeWidgetItem([str(value)])
            item.addChild(child)

    ## Push data to Tree View
    fixtureprofiletree = configui.fixtureprofiletree
    profile = []

    for key, values in fixtureprofiles.items():
        item = QTreeWidgetItem([key])
#        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
#        item.setCheckState(0, Qt.Unchecked)
        add_children(item, values)  # Add the nested dictionary structure
        profile.append(item)

    fixtureprofiletree.insertTopLevelItems(0, profile)

## Run Add Fixture Profile UI
def afpuirun():
    afpui.show()
    afpui.button(QWizard.FinishButton).clicked.connect(savefixprof)   ## When finish button pressed

## Run Fixture Patch UI
def patchfixrun():
    fixpatch.show()
    ## On item Changed
    def on_item_changed(item, column):
        parent = item.parent()
        if parent is None:
            fixtureprofiles[item.text(0)] = item.text(column)
        else:
            keys = []
            while parent is not None:
                keys.append(parent.text(0))
                parent = parent.parent()
            keys.reverse()
            d = fixtureprofiles
            for key in keys:
                d = d[key]
            d[item.text(0)] = item.text(column)
    ## Create Profile Tree View
    def add_children(item, value):
        if isinstance(value, dict):
            for key, val in value.items():
                child = QTreeWidgetItem([key])
                item.addChild(child)
                add_children(child, val)
        else:
            child = QTreeWidgetItem([str(value)])
            item.addChild(child)

    fixpatchtree = fixpatch.fixturepatchtree
    profile = []

    for key, values in fixtureprofiles.items():
        item = QTreeWidgetItem([key])
        item.setFlags(item.flags() | Qt.ItemIsEditable)  # Allow text to be edited
#        add_children(item, values)  # Add the nested dictionary structure
        profile.append(item)
            
    fixpatchtree.insertTopLevelItems(0, profile)
    fixtureprofiletree.itemChanged.connect(on_item_changed)
            

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

## Add Fixture Patch UI
fixpatchfile = QFile("fixturepatch.ui")
if not fixpatchfile.open(QIODevice.ReadOnly):
    print(f'Cannot open addfixtureprofile.ui: {afpuifile.errorString()}')
    sys.exit(-1)
fixpatch = loader.load(fixpatchfile)
fixpatchfile.close()
if not fixpatch:
    print(loader.errorString)
    sys.exit

## Load previous adapter config file
try:
    config = configparser.ConfigParser()                        ## INIT section: create a configparser object & read file
    config.read('adapterconfig.ini') 

    dmxchanmax = config.get('dmxconfig', 'dmx_channel_count')   ## READ section: access all of the config settings
    serialport = config.get('dmxconfig', 'adapter_serial_port')
    adatspeed = config.get('dmxconfig', 'user_adapter_speed')
    autoadatspeed = config.get('dmxconfig', 'max_dmx_adapter_speed')

    adatvalues = {                                           ## Export our config values in a nice dictionary for easy upgradibility
        'dmxchanmax': dmxchanmax,   
        'serialport': serialport,
        'adatspeed': adatspeed,
        'autoadatspeed': autoadatspeed,
    }
    print("Adapter Settings found and loaded")
except:
    print("Adapter Config file not found, this is normal on new installs")

## Load previous fixture profiles (if there are any)
try:
    with open('profiles.json', 'r') as file:         
        fixtureprofiles = json.load(file)
    print("Fixture profile database found and loaded")
except:
    print("No Fixture Profile Database found, This is normal on new installs")

## Load previous patch (if exists)
try:
    with open('patchdata.json', 'r') as file:
        fixturepatch = json.load(file)
    print("Patch data found and loaded")
except:
    print("No Patch Database found, this is normal on new installs")

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
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        item.setCheckState(0, Qt.Unchecked)
adatree.insertTopLevelItems(0, items)

## Create Profile Tree View
def add_children(item, value):
    if isinstance(value, dict):
        for key, val in value.items():
            child = QTreeWidgetItem([key])
            item.addChild(child)
            add_children(child, val)
    else:
        child = QTreeWidgetItem([str(value)])
        item.addChild(child)

fixtureprofiletree = configui.fixtureprofiletree
profile = []

for key, values in fixtureprofiles.items():
    item = QTreeWidgetItem([key])
#    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
#    item.setCheckState(0, Qt.Unchecked)
    add_children(item, values)  # Add the nested dictionary structure
    profile.append(item)
    
fixtureprofiletree.insertTopLevelItems(0, profile)

configui.addfixtureprofile.clicked.connect(afpuirun)
configui.patchfixtures.clicked.connect(patchfixrun)

app.exec()
## Get adat values
adatport = configui.adatpath.text()
chanreq = configui.ChannelReq.value()
adatspeed = configui.speedenter.value()
if adatspeed == True:
    manspeed = True
else:
    manspeed = False
    autoadatspeed = int(1000000 / (140 + (44 * chanreq)))

## Save adat values to file
adatvalues = {
    'dmxchanmax': chanreq,
    'serialport': adatport,
    'adatspeed': adatspeed,
    'autoadatspeed': autoadatspeed,
}
with open('adapterconfig.ini', 'w') as configfile:
    config.write(adatvalues)

## Save fixture profile values to file
print("Saving profiles to 'profiles.json'....")
with open('profiles.json', 'w') as profilefile: 
    profilefile.write(json.dumps(fixtureprofiles, indent=4))
print('Profiles saved to profiles.json')


sys.exit

   
