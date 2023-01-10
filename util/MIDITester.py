import sys
import mido

backend = mido.Backend("mido.backends.rtmidi")

print(sys.argv)

if len(sys.argv) > 1:
    output = backend.open_output(sys.argv[1])
    print("Connected to MIDI port " + sys.argv[1])
else:
    output = backend.open_output("Beagle Test", True)
    print("Connected to MIDI port Beagle Test")

try:
    while True:
        channel = input("Channel Number (1-16):")
        output.send(mido.Message(type = "control_change", channel = int(channel) - 1))
except Exception as ex:
    input.close()
    raise ex