#!/usr/bin/python3

import busio
import digitalio
import board
import time
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

VOLTAGE_MIN = 0.8  # When moisture is 100%
VOLTAGE_MAX = 3.3  # When moisture is 0%

class MoistureMeter():
	def __init__(self, identifier, chan):
		self.identifier = identifier
		self.chan = chan

	def measure(self):
		# print('Raw ADC Value: ', chan.value)
		# print('ADC Voltage: ' + str(chan.voltage) + 'V')
		perc = (VOLTAGE_MAX - self.chan.voltage) / (VOLTAGE_MAX - VOLTAGE_MIN)
		print(self.identifier + ': ' + "{:.0%}".format(perc))

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

cs = digitalio.DigitalInOut(board.CE0)

mcp = MCP.MCP3008(spi, cs)

chan1 = AnalogIn(mcp, MCP.P0)
chan2 = AnalogIn(mcp, MCP.P1)
chan3 = AnalogIn(mcp, MCP.P2)

meter1 = MoistureMeter('pepper-0', chan1)
meter2 = MoistureMeter('pepper-1', chan2)
meter3 = MoistureMeter('pepper-2', chan3)

while True:
	meter1.measure()
	meter2.measure()
	meter3.measure()
	time.sleep(2)

