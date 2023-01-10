import sys
import mido

backend = mido.Backend("mido.backends.rtmidi")

port = sys.argv[1] if len(sys.argv) > 1 else "Beagle Test"
print("Sending to MIDI port " + port)

try:
    while True:
        try:
            channel = input("Channel Number (1-16):")
            channel = int(channel.strip()) - 1
            if len(sys.argv) > 1:
                backend.open_output(port).send(mido.Message(type = "control_change", channel = channel))
            else:
                backend.open_output(port, True).send(mido.Message(type = "control_change", channel = channel))
        except KeyboardInterrupt as ex:
            raise ex
        except Exception as ex:
            print("Error: " + str(ex))
except Exception as ex:
    raise ex