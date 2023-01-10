from util.defaultMidi import MIDIOutput
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)

class ConnectMidiButton(QPushButton):
    def __init__(self, config, midiOutput, address, idx):
        super().__init__("Connect")
        self.config = config
        self.midiOutput = midiOutput
        self.address = address
        self.idx = idx
        self.init(True)

        self.currentAddress = address.currentText()
        self.isConnect = True
        self.updateButton(self.currentAddress)
        self.address.currentTextChanged.connect(self.updateButton)

        self.pressed.connect(self.connect)
        self.setFixedWidth(80)

    def updateButton(self, name):
        self.address.onChange(name) # Parent Function
        self.setEnabled(name != "")

        if name == self.currentAddress and self.currentAddress != "" and self.midiOutput[self.idx].connected():
            self.isConnect = False
            self.setText("Clear")
        else:
            self.isConnect = True
            self.setText("Connect")
    
    def connect(self):
        if self.isConnect:
            if (self.init()):
                dlg = QMessageBox(self)
                dlg.setWindowTitle("MIDI Connection")
                dlg.setText("Connected to " + self.currentAddress + " port")
                dlg.exec()
            else:
                dlg = QMessageBox(self)
                dlg.setWindowTitle("MIDI Connection")
                dlg.setText("Unable to connect to " + self.currentAddress + " port")
                dlg.exec()
        else:
            self.midiOutput[self.idx] = MIDIOutput(None)
            self.address.setCurrentIndex(-1)
            self.address.invalid()
        
        self.currentAddress = self.address.currentText()
        self.updateButton(self.currentAddress)
        self.setDown(False)

    def init(self, init = False):
        self.midiOutput[self.idx] = MIDIOutput(self.address.currentText())

        if init and self.address.currentText() == "":
            self.address.invalid()
            return False
        elif (self.midiOutput[self.idx].open_output()):
            self.address.connected()
            return True
        else:
            self.address.invalid()
            return False