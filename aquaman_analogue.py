#!/usr/bin/python3

from absl import app, flags, logging
import prometheus_client as prom
import busio
import digitalio
import board
import time
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


FLAGS = flags.FLAGS
flags.DEFINE_string("id0", None, "Identifier used in metric labels for channel 0")
flags.DEFINE_string("id1", None, "Identifier used in metric labels for channel 1")
flags.DEFINE_string("id2", None, "Identifier used in metric labels for channel 2")
flags.DEFINE_string("id3", None, "Identifier used in metric labels for channel 3")
flags.DEFINE_string("id4", None, "Identifier used in metric labels for channel 4")
flags.DEFINE_string("id5", None, "Identifier used in metric labels for channel 5")
flags.DEFINE_string("id6", None, "Identifier used in metric labels for channel 6")
flags.DEFINE_string("id7", None, "Identifier used in metric labels for channel 7")
flags.DEFINE_integer("poll_ms", 1000, "Frequency of polls of sensors")

id_getter = {
	MCP.P0: lambda: FLAGS.id0,
	MCP.P1: lambda: FLAGS.id1,
	MCP.P2: lambda: FLAGS.id2,
	MCP.P3: lambda: FLAGS.id3,
	MCP.P4: lambda: FLAGS.id4,
	MCP.P5: lambda: FLAGS.id5,
	MCP.P6: lambda: FLAGS.id6,
	MCP.P7: lambda: FLAGS.id7,
}

VOLTAGE_MIN = 0.5  # When moisture is 100%
VOLTAGE_MAX = 3.3  # When moisture is 0%

class MoistureMeter():
	def __init__(self, identifier, chan, gauge):
		self.identifier = identifier
		self.chan = chan
		self.gauge = gauge

	def measure(self):
		logging.debug(self.identifier + ' ADC Voltage: ' + str(self.chan.voltage) + 'V')
		perc = (VOLTAGE_MAX - self.chan.voltage) / (VOLTAGE_MAX - VOLTAGE_MIN)
		logging.debug(self.identifier + ' moisture: ' + "{:.0%}".format(perc))
		if perc < 0 or perc > 1:
			logging.warning(self.identifier + ' voltage out of range :' + str(self.chan.voltage))
		self.gauge.labels(self.identifier).set(perc)


def main(argv):
	del argv

	# Setup up board
	spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
	cs = digitalio.DigitalInOut(board.CE0)
	mcp = MCP.MCP3008(spi, cs)

	# Setup up metrics
	gauge = prom.Gauge('moisture_percent', 'Moisture percentage', ['sensor_id'])
	logging.info("Starting http server...")
	prom.start_http_server(8080)
	logging.info("Started http server on port 8080")

	meters = []
	for pin, getter in id_getter.items():
		id = getter()
		if id:
			logging.info("Measuring pin " + str(pin) + " with id " + id)
			meter = MoistureMeter(id, AnalogIn(mcp, pin), gauge)
			meters.append(meter)
		else:
			logging.info("Not measuring pin " + str(pin))

	if not meters:
		logging.error("no pins are being measured")
		return

	while True:
		for m in meters:
			m.measure()
		logging.debug("Sleeping for " + str(FLAGS.poll_ms) + "ms")
		time.sleep(0.001 * FLAGS.poll_ms)

if __name__ == '__main__':
	app.run(main)
