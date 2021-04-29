#!/usr/bin/python3

from absl import app, flags, logging
import RPi.GPIO as GPIO
import prometheus_client as prom
import time

FLAGS = flags.FLAGS
flags.DEFINE_string("identifier", None, "Identifier used in metric labels")
flags.mark_flag_as_required("identifier")
flags.DEFINE_integer("bcm_channel", 17, "BCM channel to read")
flags.DEFINE_integer("bounce_ms", 300, "Debouncing delay")

GPIO.setmode(GPIO.BCM)
gauge = prom.Gauge(
    "moisture_bool", "Whether moisture has been detected or not", ["instance"]
)


def measure(channel, identifier):
    if GPIO.input(channel):
        gauge.labels(identifier).set(0)
        logging.debug("LED off")
    else:
        gauge.labels(identifier).set(1)
        logging.debug("LED on")


def debounce_measure(channel, bounce_ms, identifier):
    # If the sensor is bouncing we want to read the value when it stops bouncing.
    # This sleep means we read after the GPIO debounce delay so we get the stable value once
    # the sensor has stopped bouncing.  If the sensor is still bouncing this callback
    # will be called again.
    time.sleep(0.001 * bounce_ms)
    measure(channel, identifier)


def main(argv):
    del argv

    callback = lambda channel: debounce_measure(
        channel, FLAGS.bounce_ms, FLAGS.identifier
    )

    # Set up pin reads
    bcm_channel = FLAGS.bcm_channel
    GPIO.setup(bcm_channel, GPIO.IN)

    # measure initial values
    measure(bcm_channel, FLAGS.identifier)

    # measure on pin change
    GPIO.add_event_detect(
        bcm_channel, GPIO.BOTH, callback=callback, bouncetime=FLAGS.bounce_ms
    )

    logging.info("Starting http server...")
    prom.start_http_server(8080)
    logging.info("Started http server on port 8080")
    while True:
        time.sleep(0.1)


if __name__ == "__main__":
    app.run(main)
