## This program runs the config GUI
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QIODevice
import serial.tools.list_ports
import sys


def runaddfixtureprofile():
    addfixtureprofile.show()

## Init GUI files....
app = QApplication(sys.argv)
loader = QUiLoader()

## Main config UI....
mainconfiguifile = QFile("Config.ui")
configui = loader.load(mainconfiguifile)
mainconfiguifile.close()
if not configui:
    print(configui.errorString())
    sys.exit(-1)

## Add Fixture Profile UI....
addfixtureprofilefile = QFile("addfixtureprofile.ui")
addfixtureprofile = loader.load(addfixtureprofilefile)
addfixtureprofilefile.close()
if not addfixtureprofile:
    print(addfixtureprofile.errorString())
    sys.exit(-1)

## Fixture Patch UI....
fixturepatchfile = QFile("fixturepatch.ui")
fixturepatch = loader.load(fixturepatchfile)
fixturepatchfile.close()
if not fixturepatchfile:
    print(fixturepatchfile.errorString())
    sys.exit(-1)

## Fire up the GUI and show it
configui.show()

## Adapter Selection Init (Get all adapters)

serialports = {}
for port in serial.tools.list_ports.comports():
    serialports[port.name] = {}
    serialports[port.name]['description'] = port.description
    serialports[port.name]['manufacturer'] = port.manufacturer
    serialports[port.name]['hwid'] = port.hwid

## Add adapters to tree

adattree = configui.adapterselect

## If add fixture button pressed, run addfixtureprofile()
configui.addfixtureprofile.clicked.connect(runaddfixtureprofile)

sys.exit(app.exec())