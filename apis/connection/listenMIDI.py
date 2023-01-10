from datetime import date, timedelta
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)
from util.constants import MIDI_SERVER_NAME
from util.customWidgets import AddressBox
from util.defaultMidi import MIDIInput

class ListenMidiButton(QPushButton):
    def __init__(self, config, midiInput, midiServer):
        super().__init__("Specify MIDI ports to listen to")
        self.midiInput = midiInput
        self.midiServer = midiServer
        self.pressed.connect(self.clicked)

        for port in config["input"]:
            self.midiInput[port] = MIDIInput(self.midiServer, port)
            self.midiInput[port].open_input()

    def clicked(self):
        MidiInputDialog(self.midiInput, self.midiServer).exec()
        self.setDown(False)

class MidiInputDialog(QDialog):
    def __init__(self, midiInput, midiServer):
        super().__init__()

        vlayout = QVBoxLayout()
        
        scrollLayout = QVBoxLayout()
        for port in midiInput:
            hlayout = QHBoxLayout()

            address = AddressBox(port, midiServer.get_input_names() - set([MIDI_SERVER_NAME]))
            hlayout.addWidget(address)
            hlayout.addWidget(address.status)

            if midiInput[port].connected():
                address.connected()
            else:
                address.invalid()

            hlayout.addWidget(ConnectRemoveButton(midiInput, midiServer, address))

            scrollLayout.addLayout(hlayout)
        
        scrollWidget = QWidget()
        scrollWidget.setLayout(scrollLayout)
        scrollArea = QScrollArea()
        scrollArea.setWidget(scrollWidget)
        scrollArea.setWidgetResizable(True)

        vlayout.addWidget(AddLine(scrollLayout, midiInput, midiServer))
        vlayout.addWidget(scrollArea)

        self.setLayout(vlayout)
        self.setMinimumSize(599, 380)

class ConnectRemoveButton(QPushButton):
    def __init__(self, midiInput, midiServer, address):
        super().__init__("Connect")
        self.midiInput = midiInput
        self.midiServer = midiServer
        self.address = address
        
        self.currentAddress = address.currentText()
        self.isConnect = True
        self.updateButton(self.currentAddress)
        self.address.currentTextChanged.connect(self.updateButton)

        self.pressed.connect(self.onPressed)
        self.setFixedWidth(80)
    
    def updateButton(self, name):
        self.address.onChange(name) # Parent Function
        self.setEnabled(name != "" and name != MIDI_SERVER_NAME and not (name in self.midiInput and name != self.currentAddress))

        if name == self.currentAddress and self.currentAddress != "":
            self.isConnect = False
            self.setText("Remove")
        else:
            self.isConnect = True
            self.setText("Connect")
    
    def onPressed(self):
        if self.currentAddress != "":
            # Disconnect First
            self.midiInput[self.currentAddress].close()
            del self.midiInput[self.currentAddress]

        if self.isConnect:
            self.midiInput[self.address.currentText()] = MIDIInput(self.midiServer, self.address.currentText())

            if (self.midiInput[self.address.currentText()].open_input()):
                self.address.connected()

                dlg = QMessageBox(self)
                dlg.setWindowTitle("MIDI Connection")
                dlg.setText("Listening to " + self.address.currentText() + " port")
                dlg.exec()
            else:
                self.address.invalid()

                dlg = QMessageBox(self)
                dlg.setWindowTitle("MIDI Connection")
                dlg.setText("Unable to listen to " + self.address.currentText() + " port")
                dlg.exec()
        else:
            self.address.setCurrentIndex(-1)
            self.address.invalid()

            dlg = QMessageBox(self)
            dlg.setWindowTitle("MIDI Connection")
            dlg.setText("Stopped Listening to " + self.currentAddress + " port")
            dlg.exec()

        self.currentAddress = self.address.currentText()
        self.updateButton(self.currentAddress)
        self.setDown(False)

class AddLine(QPushButton):
    def __init__(self, scrollLayout, midiInput, midiServer):
        super().__init__("Add Line")
        self.scrollLayout = scrollLayout
        self.midiInput = midiInput
        self.midiServer = midiServer
        self.pressed.connect(self.clicked)

    def clicked(self):
        hlayout = QHBoxLayout()

        address = AddressBox("", self.midiServer.get_input_names() - set([MIDI_SERVER_NAME]))
        hlayout.addWidget(address)
        hlayout.addWidget(address.status)
        address.invalid()

        hlayout.addWidget(ConnectRemoveButton(self.midiInput, self.midiServer, address))

        self.scrollLayout.addLayout(hlayout)

        self.setDown(False)