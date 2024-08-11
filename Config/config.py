from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QSpinBox, QWizard, QWizardPage
from PySide6.QtCore import QFile, QIODevice, Qt
import threading
import time
import serial.tools.list_ports
import sys

global configui
global afpui
global fixtureprofiles

def savefixprof():
    ## Save Stuff to Vars
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

    ## Save to dict
    fixtureprofiles[fixname] = {}
    fixtureprofiles[fixname]['channel_count'] = chancount
    fixtureprofiles[fixname]['pan_limit'] = panlimit
    fixtureprofiles[fixname]['tilt_limit'] = tiltlimit
    fixtureprofiles[fixname]['bulb_wattage'] = bulbwattage
    fixtureprofiles[fixname]['bulb_lumens'] = bulblumen
    fixtureprofiles[fixname]['max_zoom_angle'] = maxzoom
    fixtureprofiles[fixname]['min_zoom_angle'] = minzoom
    fixtureprofiles[fixname]['max_focus_angle'] = maxfocus
    fixtureprofiles[fixname]['min_focus_angle'] = minfocus
    fixtureprofiles[fixname]['pan'] = panchan
    fixtureprofiles[fixname]['fine_pan'] = finepanchan
    fixtureprofiles[fixname]['tilt'] = tiltchan
    fixtureprofiles[fixname]['fine_tilt'] = finetiltchan
    ## Speed Control
    if ptspeedcontrol == True:
        fixtureprofiles[fixname]['pan_tilt_speed_control'] = ptspeedchan
    else:
        fixtureprofiles[fixname]['pan_tilt_speed_control'] = 'none'
    ## RGB Control
    if redcontrol == True:
        fixtureprofiles[fixname]['red'] = redchan
    else:
        fixtureprofiles[fixname]['red'] = 'none'
    if bluecontrol == True:
        fixtureprofiles[fixname]['blue'] = bluechan
    else:
        fixtureprofiles[fixname]['blue'] = 'none'
    if greencontrol == True:
        fixtureprofiles[fixname]['green'] = greenchan
    else:
        fixtureprofiles[fixname]['green'] = 'none'
    ## CMY Control
    if cyancontrol == True:
        fixtureprofiles[fixname]['cyan'] = cyanchan
    else:
        fixtureprofiles[fixname]['cyan'] = 'none'
    if magentacontrol == True:
        fixtureprofiles[fixname]['magenta'] = magentachan
    else:
        fixtureprofiles[fixname]['magenta'] = 'none'
    if yellowcontrol == True:
        fixtureprofiles[fixname]['yellow'] = yellowchan
    else:
        fixtureprofiles[fixname]['yellow'] = 'none'
    ## Colour Wheel Control
    if colourwheelcontrol == True:
        fixtureprofiles[fixname]['colour_wheel'] = colourwheelchan
    else:
        fixtureprofiles[fixname]['colour_wheel'] = 'none'
    ## CTO Control
    if ctocontrol == True:
        fixtureprofiles[fixname]['cto'] = ctochan
    else:
        fixtureprofiles[fixname]['cto'] = 'none'
    ## Zoom Control
    fixtureprofiles[fixname]['zoom'] = zoomchan
    if finezoomcontrol == True:
        fixtureprofiles[fixname]['fine_zoom'] = finezoomchan
    else:
        fixtureprofiles[fixname]['fine_zoom'] = 'none'
    ## Focus Control
    fixtureprofiles[fixname]['focus'] = focuschan
    if finefocuscontrol == True:
        fixtureprofiles[fixname]['fine_focus'] = finefocuschan
    else:
        fixtureprofiles[fixname]['fine_focus'] = 'none'
    ## Gobo Control
    

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

   
