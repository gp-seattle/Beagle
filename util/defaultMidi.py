from uuid import uuid4
import mido
import mido.backends.rtmidi # For PyInstaller
from util.constants import MIDI_SERVER_NAME

# MIDI Destination
class MIDIOutput(mido.Backend):
    def __init__(self, port):
        super().__init__("mido.backends.rtmidi")
        self.port = port
        self.output = None
    
    def open_output(self):
        try:
            self.output = super().open_output(self.port)
            print("Connected to MIDI at " + self.port)
        except Exception as ex:
            print(ex)
            print("Failed to connect to MIDI at " + self.port)
            self.output = None

        return self.output is not None
    
    def send(self, message):
        if self.output is not None:
            self.output.send(message)
        else:
            raise SystemError("Not Connected to MIDI Port")
    
    def connected(self):
        return self.output is not None

# MIDI Listener
class MIDIInput(mido.Backend):
    def __init__(self, midiServer, port):
        super().__init__("mido.backends.rtmidi")
        self.input = None
        self.midiServer = midiServer
        self.port = port

    def open_input(self):
        try:
            self.input = super().open_input(self.port)
            self.input.callback = self.midiServer.callbackFunction
            print("Listening to MIDI Port " + self.port)
        except Exception as ex:
            print(ex)
            print("Failed to listen to MIDI at " + self.port)
            self.input = None

        return self.input is not None
    
    def connected(self):
        return self.input is not None
    
    def close(self):
        if self.input is not None:
            self.input.close()
            print("Stopped listening to MIDI Port " + self.port)
            self.input = None

# MIDI Virtual Port
class MIDIVirtualPort(mido.Backend):
    def __init__(self, midiOutput):
        super().__init__("mido.backends.rtmidi")
        self.midiOutput = midiOutput

        self.ioPort = super().open_ioport(MIDI_SERVER_NAME, True)
        self.ioPort.input.callback = self.callbackFunction
        print("Created MIDI IO Port " + MIDI_SERVER_NAME)
    
    def callbackFunction(self, message):
        if (message.channel + 1) in self.midiOutput and self.midiOutput[message.channel + 1].connected():
            if self.midiOutput[message.channel + 1].port == MIDI_SERVER_NAME:
                self.ioPort.output.send(message)
            else:
                self.midiOutput[message.channel + 1].send(message)

    def get_input_names(self):
        return set(super().get_input_names())
    
    def get_output_names(self):
        return set(super().get_output_names())
    
    def close(self):
        if self.ioPort is not None:
            self.ioPort.close()
            print("Stopped listening to MIDI Port " + MIDI_SERVER_NAME)