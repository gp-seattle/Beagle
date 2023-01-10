# Beagle

Simple MIDI IO manager, to manage MIDI traffic flow.

## Input

A `Beagle` MIDI virtual port is created by this application. Send midi signals to this port to be able to forward ongoing traffic.

Alternatively, specify ports to explicitly listen to using the Listen button at the top of the application.

## Output

For each of the 16 valid MIDI channels, specify what the target output port is. Input messages will then be routed to these target output ports.

A virtual output port will be created if the specified port doesn't exist. The virtual port will be prefixed by `Beagle - `.

## Dependencies:

- [python](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [pyinstaller](https://pypi.org/project/pyinstaller/)
- [mido](https://mido.readthedocs.io/en/latest/installing.html)
- [PyQt6](https://pypi.org/project/PyQt6/)

### For Mac run the following commands:

Install Homebrew: https://brew.sh

Then after completing the post completion steps of homebrew:

```
brew install git
brew install python
python3 -m ensurepip --upgrade
sudo -H pip3 install --prefix=/usr/local pyinstaller
pip3 install -r requirements.txt
```