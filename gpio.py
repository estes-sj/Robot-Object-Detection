# Fiile for setting up and interacting with GPIO pins

import Jetson.GPIO as GPIO
import config

# setup GPIO
def setup():
    GPIO.setmode(GPIO.BCM)

    # Outputs
    GPIO.setup(config.PIN_LEFT, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(config.PIN_RIGHT, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(config.PIN_LAUNCH, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(config.PIN_ARM, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(config.PIN_CONTROL, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(config.PIN_GREEN, GPIO.OUT, initial=GPIO.LOW)

    # Input
    GPIO.setup(config.PIN_RESPONSE, GPIO.IN)
    GPIO.setup(config.PIN_REBOOT, GPIO.IN)

# Set a pin HIGH
def set_high(PIN):
    GPIO.output(PIN, GPIO.HIGH)

# Set a pin LOW
def set_low(PIN):
    GPIO.output(PIN, GPIO.LOW)

# Read value from pin
def read_pin(PIN):
    val = GPIO.input(PIN)
    return val

# GPIO cleanup
def cleanup():
    GPIO.cleanup()