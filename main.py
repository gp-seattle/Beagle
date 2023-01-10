from apis.connection.connectMIDI import ConnectMidiButton
from apis.connection.listenMIDI import ListenMidiButton
from apis.menu.About import About
from apis.menu.ClearCache import ClearCache
from apis.menu.Update import UpdateApp
from config import config
import faulthandler
import os
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QScrollArea,
    QVBoxLayout,
    QWidget
)
import sys
from util.customWidgets import AddressBox, LogBox
from util.defaultMidi import MIDIVirtualPort

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.config = config

        self.logBox = LogBox()

        self.midiInput = {}
        self.midiOutput = {}
        self.midiVirtualOutput = {} # Key is port name
        self.midiServer = MIDIVirtualPort(self.midiOutput, self.logBox)

        self.saveCache = True

        self.setWindowTitle("Beagle")

        vlayout = QVBoxLayout()

        vlayout.addWidget(ListenMidiButton(self.config, self.midiInput, self.midiServer, self.logBox))

        vlayout.addWidget(QLabel("Destinations:"))
        
        scrollLayout = QVBoxLayout()
        for idx in range(1, 17):
            hlayout = QHBoxLayout()
            label = QLabel("Channel " + str(idx) + ":")
            label.setFixedWidth(100)
            hlayout.addWidget(label)
            
            address = AddressBox(self.config["output"][idx]["name"] if idx in self.config["output"] else "", self.midiServer.get_output_names())
            hlayout.addWidget(address)
            hlayout.addWidget(address.status)

            hlayout.addWidget(ConnectMidiButton(self.config, self.midiOutput, self.midiVirtualOutput, self.logBox, address, idx, self.config["output"][idx]["virtual"] if idx in self.config["output"] else False))

            scrollLayout.addLayout(hlayout)
        
        scrollWidget = QWidget()
        scrollWidget.setLayout(scrollLayout)
        scrollArea = QScrollArea()
        scrollArea.setWidget(scrollWidget)
        scrollArea.setWidgetResizable(True)
        vlayout.addWidget(scrollArea)

        vlayout.addWidget(QLabel("Log:"))
        vlayout.addWidget(self.logBox)

        widget = QWidget()
        widget.setLayout(vlayout)
        self.setCentralWidget(widget)
        
        menu = self.menuBar().addMenu("&Menu")
        menu.addAction(About(self))
        menu.addAction(ClearCache(self))
        menu.addAction(UpdateApp(self))

    # Save Cache
    def closeEvent(self, a0):
        self.midiServer.close()
        for port in self.midiInput:
            self.midiInput[port].close()

        if self.saveCache:
            # TODO: Implement Cache
            pass

        return super().closeEvent(a0)

faulthandler.enable()
os.chdir(os.path.dirname(__file__))
if not os.path.exists("pyinstaller.sh"): # Not in Main Directory
    os.chdir("../Resources")
app = QApplication(sys.argv)
window = MainWindow()
window.resize(599, 599)
window.show()
app.exec()