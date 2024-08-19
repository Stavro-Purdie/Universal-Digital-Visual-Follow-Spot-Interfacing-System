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
    fixmanufacturer = afpui.fixmanu.text()
    chancount = afpui.chancount.value()
    panchan = afpui.panchan.value()
    finepanchan = afpui.finepanchan.value()
    tiltchan = afpui.tiltchan.value()
    finetiltchan = afpui.finetiltchan.value()
    ptspeedchan = afpui.ptspeedchan.value()
    if ptspeedchan > 0:
        ptspeedcontrol = True
    else:
        ptspeedcontrol = False
    redchan = afpui.redchan.value()
    if redchan > 0:
        redcontrol = True
    else:
        redcontrol = False
    greenchan = afpui.greenchan.value()
    if greenchan > 0:
        greencontrol = True
    else:
        greencontrol = False
    bluechan = afpui.bluechan.value()
    if bluechan > 0:
        bluecontrol = True
    else:
        bluecontrol = False
    cyanchan = afpui.cyanchan.value()
    if cyanchan > 0:
        cyancontrol = True
    else:
        cyancontrol = False
    magentachan = afpui.magentachan.value()
    if magentachan > 0:
        magentacontrol = True
    else:
        magentacontrol = False
    yellowchan = afpui.yellowchan.value()
    if yellowchan > 0:
        yellowcontrol = True
    else:
        yellowcontrol = False
    colourwheelchan = afpui.colourwheelchan.value()
    if colourwheelchan > 0:
        colourwheelcontrol = True
    else:
        colourwheelcontrol = False
    ctochan = afpui.ctochan.value()
    if ctochan > 0:
        ctocontrol = True
    else:
        ctocontrol = False
    zoomchan = afpui.zoomchan.value()
    finezoomchan = afpui.zoomfinechan.value()
    if finezoomchan > 0:
        finezoomcontrol = True
    else:
        finezoomcontrol = False
    focuschan = afpui.focuschan.value()
    finefocuschan = afpui.focusfinechan.value()
    if finefocuschan > 0:
        finefocuscontrol = True
    else:
        finefocuscontrol = False
    staticgobochan = afpui.staticgobochan.value()
    rotgobochan = afpui.rotgobochan.value()
    dimmerchan = afpui.dimmerchan.value()
    finedimmerchan = afpui.finedimmerchan.value()
    if finedimmerchan > 0:
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
    fixtureprofiles[fixname]['manufacturer'] = fixmanufacturer
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
    if bluecontrol is True:
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
    global fixturepatch, fixturealias
    fixturepatch = {}
    fixturealias = {}
    fixpatch.show()

    ## Driver code for tree
    def add_children(item, value):
        if isinstance(value, dict):
            for key, val in value.items():
                child = QTreeWidgetItem([key, str(val) if not isinstance(val, dict) else ""])
                child.setFlags(child.flags() | Qt.ItemIsEditable)
                item.addChild(child)
                add_children(child, val)
        else:
            child = QTreeWidgetItem(["", str(value)])
            child.setFlags(child.flags() | Qt.ItemIsEditable)
            item.addChild(child)

    ## Function to handle changes and save to a separate dictionary
    def on_startchan_changed(item, column):
        if column == 1:  # Only handle changes in the second column
            keys = []
            parent = item.parent()
            
            # Traverse up to the root to get the full path
            while parent is not None:
                keys.append(parent.text(0))
                parent = parent.parent()
            
            keys.reverse()
            key_path = " -> ".join(keys) if keys else item.text(0)
            
            # Process the edited value: filter out commas and split by spaces
            values = item.text(column).replace(',', ' ').split()

            # Ensure the key path is correct
            base_key = key_path if key_path else item.text(0)

            # Remove existing entries for this key path
            keys_to_remove = [key for key in fixturepatch if key.startswith(base_key)]
            for key in keys_to_remove:
                del fixturepatch[key]
            
            # Save each number as a separate entry in the dictionary
            fixturepatch[base_key] = {}
            for i, value in enumerate(values):
                fixturepatch[base_key][i] = value

    # Populate the tree with initial fixture profiles
    profile = []
    for key, values in fixtureprofiles.items():
        item = QTreeWidgetItem([key, ""])
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        add_children(item, values)
        profile.append(item)

    fixturepatchtree = fixpatch.fixturepatchtree
    fixturepatchtree.insertTopLevelItems(0, profile)

    # Connect the itemChanged signal to the on_startchan_changed function
    fixturepatchtree.itemChanged.connect(on_startchan_changed)

    ## Function to handle changes in the alias tree and save to another dictionary
    def on_alias_changed(item, column):
        if column == 1:  # Only handle changes in the second column
            spot_name = item.text(0)
            if not spot_name.startswith("spot"):
                return  # Ensure we are only dealing with spot entries
            
            # Get the URI and Name from the child items
            uri = item.child(0).text(1) if item.child(0) else ""
            name = item.child(1).text(1) if item.child(1) else ""
            
            # Save the edited values in the fixturealias dictionary
            fixturealias[spot_name] = {"URI": uri, "Name": name}

    ## Populate the alias tree with fixture patch spots
    fixalias = []
    fixnum = 0
    for key in fixturepatch.keys():
        fixnum += 1
        spot_item = QTreeWidgetItem([f'spot{fixnum}', ""])
        spot_item.setFlags(spot_item.flags() | Qt.ItemIsEditable)

        # Add URI and Name fields as children of each spot
        uri_item = QTreeWidgetItem(["URI", ""])
        uri_item.setFlags(uri_item.flags() | Qt.ItemIsEditable)
        spot_item.addChild(uri_item)

        name_item = QTreeWidgetItem(["Name", ""])
        name_item.setFlags(name_item.flags() | Qt.ItemIsEditable)
        spot_item.addChild(name_item)

        fixalias.append(spot_item)

    singlefixpatchtree = fixpatch.singlefixpatchtree
    singlefixpatchtree.insertTopLevelItems(0, fixalias)

    ## Connect the itemChanged signal to the on_alias_changed function
    singlefixpatchtree.itemChanged.connect(on_alias_changed)

            
## UI IMPORT SECTION
## Init section
app = QApplication(sys.argv)
loader = QUiLoader()
fixtureprofiles = {}
fixturepatch = {}

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

## Add End-Of-Config Window
eocdatafile = QFile('EOCdata.ui')
if not eocdatafile.open(QIODevice.ReadOnly):
    print(f'Cannot open EOCdata.ui: {fixpatchfile.errorString()}')
    sys.exit(-1)
eocdata = loader.load(eocdatafile)
eocdatafile.close()
if not eocdata:
    print(loader.errorString)
    sys.exit

## DATA IMPORT SECTION
## Load previous adapter config file
try:
    with open('adapterconfig.json', 'r') as file:
        adatvalues = json.load(file)
    print('Adapter Config file found and loaded')
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


## ADAPTER SECTION
#Tree Select
adatport = None
configui.adapterportview.setText(adatport)

def on_item_changed(item, column):
    global adatport
    if item.flags() & Qt.ItemIsUserCheckable:
        parent = item.parent()
        if parent is None:
            if item.checkState(0) == Qt.Checked:
                adatport = item.text(0)
                print(f'Port: {adatport} Selected')
                configui.adapterportview.setText(adatport)
#                fixtureprofiles[item.text(0)] = True
            else:
                print("Adapter Unchecked")
#                fixtureprofiles[item.text(0)] = False

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

adatree.itemChanged.connect(on_item_changed)         ## On item changed, run funct

# Adapter AutoSpeed QLCDnumber 
adatchannel = 512
adatspeed = 44
estadatspeed = int(1000000 / (140 + (44 * adatchannel)))
configui.chanreqdisp.display(adatchannel)
configui.adatspeeddisp.display(adatspeed)

def on_spinbox_value_changed(value):
    global estadatspeed
    global adatchannel
    # This function will be called whenever the spinbox value changes
    adatchannel = int(value)
    # Est adat speed
    estadatspeed = int(1000000 / (140 + (44 * adatchannel)))
    configui.recadatspeed.display(estadatspeed)
    configui.adatspeeddisp.display(estadatspeed)
    configui.chanreqdisp.display(adatchannel)


adatchannelspinbox = configui.ChannelReq
adatchannelspinbox.valueChanged.connect(on_spinbox_value_changed)

# Adapter Speed Values (This section deals with the logic behind using the autoadatspeed or the man adat speed)
configui.adatspeeddisp.display(estadatspeed)

def on_manspeed_value_changed(manspeedenter):
    global adatspeed
    adatspeed = manspeedenter
    print(f"Manually set Adapter Speed {adatspeed}")
    configui.adatspeeddisp.display(adatspeed)

def on_manspeed_changed(value):
    global adatspeed
    if value == 2:
        manspeed = True
        print("Non-Reccommended option Manual Speed Enabled")
        manspeedenter = configui.manspeedenter
        manspeedenter.valueChanged.connect(on_manspeed_value_changed)
    else:
        manspeed = False
        adatspeed = estadatspeed
        print("Reccommended Autoassigned Speed Value Enabled")
        configui.adatspeeddisp.display(estadatspeed)

    
manspeedcheck = configui.setspeedman
manspeedcheck.stateChanged.connect(on_manspeed_changed)


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
## Get and save adat values to file
adatvalues = {'dmx_channel_count': adatchannel, 
              'adapter_serial_port': adatport, 
              'user_adapter_speed': adatspeed,
              'max_dmx_adapter_speed': estadatspeed}

print("Saving profiles to 'adapterconfig.json'....")
with open('adapterconfig.json', 'w') as configfile:
    configfile.write(json.dumps(adatvalues, indent=4))
print("Adapter settings saved to 'adapterconfig.json'")

## Save fixture profile values to file
print("Saving profiles to 'profiles.json'....")
with open('profiles.json', 'w') as profilefile: 
    profilefile.write(json.dumps(fixtureprofiles, indent=4))
print('Profiles saved to profiles.json')

## Save patch to file
print("Saving Patch to 'patchdata.json'....")
with open('patchdata.json', 'w') as patchfile:
    patchfile.write(json.dumps(fixturepatch, indent=4))
print("Patchdata saved to 'patchdata.json'")

def eocui():
    eocdata.show()
    showadatpath = eocdata.showadatpath
    showadatpath.setText(adatport)
    showadatchan = eocdata.showadatchan
    showadatchan.display(adatchannel)
    showadatspeed = eocdata.showadatspeed
    showadatspeed.display(adatspeed)
    i = 0
    showfixturecount = eocdata.showfixcount
    showfixturecount.display(i)

eocui()

sys.exit

   
