import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from maingui import *

def addfixtureprofile():
    print("test")

class MainWindow(QMainWindow):
    app = QtWidgets.QApplication(sys.argv)
    Wizard = QtWidgets.QWizard()
    ui = Ui_Wizard()
    ui.setupUi(Wizard)
    Wizard.show()
    Wizard.addfixtureprofile.clicked.connect(addfixtureprofile)
    sys.exit(app.exec())
