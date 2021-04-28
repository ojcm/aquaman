# Aquaman
Aquaman is a script to run on a Raspberry Pi to read a digital pin and export its value as a prometheus metric.
It's targetted at moisture detectors but can be reused for other input types.

## Setup
For analogue reads with MCP3008 chip additional setup is required
```
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo pip3 install adafruit-python-shell
sudo python3 raspi-blinka.py
```

## Usage
```
./aquaman.py --identifier=my-custom-identifier
```

For main command line arguments use:
```
./aquaman.py --helpshort
```

For full documentation use
```
./aquaman.py --helpfull
``` 
