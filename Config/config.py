import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import QFile, QIODevice
import serial.tools.list_ports



def onafpclick():
    afpui.show()

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
adatree = configui.adapterselect
serialports = {}
for port in serial.tools.list_ports.comports():
    serialports[port.name] = {}
    serialports[port.name]['description'] = port.description
    serialports[port.name]['manufacturer'] = port.manufacturer
    serialports[port.name]['hwid'] = port.hwid

for serialport, descriptions in serialports:
    item = QTreeWidgetItem([serialport])
    for description in descriptions:
        
configui.addfixtureprofile.clicked.connect(onafpclick)
sys.exit(app.exec())