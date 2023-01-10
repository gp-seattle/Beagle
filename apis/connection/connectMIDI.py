from util.constants import MIDI_SERVER_NAME
from util.defaultMidi import MIDIOutput
from PyQt6.QtWidgets import (
    QMessageBox,
    QPushButton,
)

class ConnectMidiButton(QPushButton):
    def __init__(self, config, midiOutput, midiVirtualOutput, logBox, address, idx, initAllowVirtual):
        super().__init__("Connect")
        self.config = config
        self.midiOutput = midiOutput
        self.midiVirtualOutput = midiVirtualOutput
        self.logBox = logBox
        self.address = address
        self.idx = idx
        self.init(True, initAllowVirtual)

        self.currentAddress = address.currentText()
        self.isConnect = True
        self.updateButton(self.currentAddress)
        self.address.currentTextChanged.connect(self.updateButton)

        self.pressed.connect(self.connect)
        self.setFixedWidth(80)

    def updateButton(self, name):
        self.address.onChange(name) # Parent Function
        self.setEnabled(name != "")

        if name == self.currentAddress and self.currentAddress != "":
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
                dlg.setText(
                    "Created virtual port '" + MIDI_SERVER_NAME + " - " + self.address.currentText() + "' port"
                    if self.midiOutput[self.idx].isVirtual
                    else "Connected to '" + self.address.currentText() + "' port"
                )
                dlg.exec()
            else:
                dlg = QMessageBox(self)
                dlg.setWindowTitle("MIDI Connection")
                dlg.setText("Unable to connect to '" + self.address.currentText() + "' port")
                dlg.exec()
        else:
            self.midiOutput[self.idx] = MIDIOutput(self.idx, None, None)
            self.address.setCurrentIndex(-1)
            self.address.invalid()

            dlg = QMessageBox(self)
            dlg.setWindowTitle("MIDI Connection")
            dlg.setText("Stopped sending messages to '" + self.address.currentText() + "' port")
            dlg.exec()
        
        self.currentAddress = self.address.currentText()
        self.updateButton(self.currentAddress)
        self.setDown(False)

    def init(self, init = False, allowVirtual = True):
        if self.address.currentText() in self.midiVirtualOutput:
            self.midiOutput[self.idx] = self.midiVirtualOutput[self.address.currentText()]
            self.address.connected()
            return True

        self.midiOutput[self.idx] = MIDIOutput(self.idx, self.address.currentText(), self.logBox)

        if init and self.address.currentText() == "":
            self.address.invalid()
            return False
        elif (self.midiOutput[self.idx].open_output(allowVirtual)):
            self.address.connected()

            if self.midiOutput[self.idx].isVirtual:
                self.midiVirtualOutput[self.address.currentText()] = self.midiOutput[self.idx]

            return True
        else:
            self.address.invalid()
            return False