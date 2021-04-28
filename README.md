# Aquaman
`aquaman.py` is a script to run on a Raspberry Pi to read a digital pin and export its value as a prometheus metric.
`aquaman_analogue.py` does the same for analogue pins reads via MCP3008 chips.
It's targetted at moisture detectors but can be reused for other input types.

## Setup
For analogue reads with MCP3008 chip additional setup is required
```
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo pip3 install adafruit-python-shell
sudo python3 raspi-blinka.py
```

## Usage

### Analogue mode
Works with MCP3008 chip.
Argument `--idX=Y` instructs the programme to read channel X and export with identifier Y.
e.g. 
```
./aquaman_analogue.py --id0=my-custom-identifier
```

### Digital mode
```
./aquaman.py --identifier=my-custom-identifier
```

### Help
For main command line arguments use `--helpshort` and for full documentation use `--helpfull`. 
