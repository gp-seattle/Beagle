from uuid import uuid4
import mido
import mido.backends.rtmidi # For PyInstaller
from util.constants import MIDI_SERVER_NAME

# MIDI Destination
class MIDIOutput(mido.Backend):
    def __init__(self, channel, port, logBox):
        super().__init__("mido.backends.rtmidi")
        self.channel = channel
        self.port = port
        self.logBox = logBox
        self.output = None
        self.isVirtual = None
    
    def open_output(self, allowVirtual = True):
        try:
            if self.port not in super().get_output_names() and allowVirtual:
                # Virtual Port
                self.output = super().open_output(MIDI_SERVER_NAME + " - " + self.port, True)
                self.isVirtual = True
                print("Created Virutal MIDI Output at " + self.port)
                self.logBox.addLine.emit("START: Sending channel " + str(self.channel) + " to " + MIDI_SERVER_NAME + " - " + self.port)
            else:
                self.output = super().open_output(self.port)
                self.isVirtual = False
                print("Connected to MIDI at " + self.port)
                self.logBox.addLine.emit("START: Sending channel " + str(self.channel) + " to " + self.port)
        except Exception as ex:
            print(ex)
            print("Failed to connect to MIDI at " + self.port)
            self.output = None

        return self.output is not None
    
    def send(self, message):
        if self.output is not None:
            self.output.send(message)
            if self.isVirtual:
                self.logBox.addLine.emit("OUTGOING: " + MIDI_SERVER_NAME + " - " + self.port + " (" + midoMessageToString(message) + ")")
            else:
                self.logBox.addLine.emit("OUTGOING: " + self.port + " (" + midoMessageToString(message) + ")")
        else:
            raise SystemError("Not Connected to MIDI Port")
    
    def connected(self):
        return self.output is not None

# MIDI Listener
class MIDIInput(mido.Backend):
    def __init__(self, midiServer, port, logBox):
        super().__init__("mido.backends.rtmidi")
        self.input = None
        self.midiServer = midiServer
        self.port = port
        self.logBox = logBox

    def open_input(self):
        try:
            self.input = super().open_input(self.port)
            self.input.callback = self.midiServer.callbackFunction
            print("Listening to MIDI Port " + self.port)
            self.logBox.addLine.emit("START: Listening to MIDI port " + self.port)
        except Exception as ex:
            print(ex)
            print("Failed to listen to MIDI at " + self.port)
            self.input = None

        return self.input is not None
    
    def callbackFunction(self, message):
        self.logBox.addLine.emit("INCOMING: " + self.port + " (" + midoMessageToString(message) + ")")
        self.midiServer.callbackChild(message)
    
    def connected(self):
        return self.input is not None
    
    def close(self):
        if self.input is not None:
            self.input.close()
            print("Stopped listening to MIDI Port " + self.port)
            self.logBox.addLine.emit("STOP: Listening to MIDI port " + self.port)
            self.input = None

# MIDI Virtual Port
class MIDIVirtualPort(mido.Backend):
    def __init__(self, midiOutput, logBox):
        super().__init__("mido.backends.rtmidi")
        self.midiOutput = midiOutput
        self.logBox = logBox

        self.input = super().open_input(MIDI_SERVER_NAME, True)
        self.input.callback = self.callbackFunction
        print("Created MIDI IO Port " + MIDI_SERVER_NAME)
        self.logBox.addLine.emit("START: Listening to MIDI port " + MIDI_SERVER_NAME)
    
    def callbackFunction(self, message):
        self.logBox.addLine.emit("INCOMING: " + MIDI_SERVER_NAME + " (" + midoMessageToString(message) + ")")
        self.callbackChild(message)

    def callbackChild(self, message):
        if (message.channel + 1) in self.midiOutput and self.midiOutput[message.channel + 1].connected():
            self.midiOutput[message.channel + 1].send(message)

    def get_input_names(self):
        names = []
        for name in set(super().get_input_names()):
            if MIDI_SERVER_NAME + " - " not in name:
                names.append(name)

        return names
    
    def get_output_names(self):
        names = []
        for name in set(super().get_output_names()):
            if name != MIDI_SERVER_NAME:
                names.append(name)

        return names
    
    def close(self):
        if self.input is not None:
            self.input.close()
            print("Stopped listening to MIDI Port " + MIDI_SERVER_NAME)
            self.logBox.addLine.emit("STOP: Listening to MIDI port " + MIDI_SERVER_NAME)

def midoMessageToString(message):
    components = str(message).split(" ")
    for idx, component in enumerate(components):
        if "channel=" in component:
            # Increase channel number by 1
            parts = component.split("=")
            val = int(parts[1]) + 1
            parts[1] = str(val)
            components[idx] = "=".join(parts)
    return " ".join(components)