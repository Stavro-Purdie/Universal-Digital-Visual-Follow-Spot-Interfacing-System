from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem 
from PySide6.QtCore import QFile, QIODevice, Qt
import serial.tools.list_ports
import sys



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

if configui.currentId != 2:
   print('yay')


## Adapter Tree
adatree = configui.adapterselect
items = []
for port in serial.tools.list_ports.comports():
    if port.device.startswith('/dev/ttyUSB'):               ## Only add USB serial devices 
        item = QTreeWidgetItem([port.device])
        item.setText(1, str(port.description) + " by " + str(port.manufacturer))
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(0, Qt.CheckState.Unchecked)
#       child = QTreeWidgetItem([port.manufacturer])
#       item.addChild(child)
        items.append(item)
adatree.insertTopLevelItems(0, items)
for itemscheck in items:
    if item.checkState(1):
            print (item.text(1),item.checkState(1))
configui.addfixtureprofile.clicked.connect(onafpclick)

sys.exit(app.exec())
