## This program runs the config GUI
import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QIODevice

def runaddfixtureprofile():
    pass

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

## Fire up the GUI and show it
configui.show()

## If add fixture button pressed, run addfixtureprofile()
configui.addfixtureprofile.clicked.connect(runaddfixtureprofile)

sys.exit(app.exec())