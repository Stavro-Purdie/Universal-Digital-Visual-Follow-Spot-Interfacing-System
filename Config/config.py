from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QSpinBox
from PySide6.QtCore import QFile, QIODevice, Qt
import threading
import time
import serial.tools.list_ports
import sys

global configui

def onafpclick():
    afpui.show()
    fixname = afpui.fixname.text()
    chancount = afpui.chancount.value()
    panlimit = afpui.panlimits.value()
    tiltlimit = afpui.tiltlimits.value
    

    
## Init section
app = QApplication(sys.argv)
loader = QUiLoader()

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


configui.addfixtureprofile.clicked.connect(onafpclick)


app.exec()
adatport = configui.adatpath.text()
chanreq = configui.ChannelReq.value()
adatspeed = configui.speedenter.value()
if adatspeed == True:
    manspeed = True
else:
    manspeed = False


sys.exit

   
