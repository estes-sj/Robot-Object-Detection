from ctypes import alignment
from hashlib import algorithms_guaranteed
import threading
import time
import jetson.inference
import jetson.utils
import os
import datetime
import argparse
import sys

import numpy as np
import Jetson.GPIO as GPIO

# Input
PIN_RESPONSE = 11	# yellow

# Setup GPIO Pins
GPIO.setmode(GPIO.BCM)

# Outputs
GPIO.setup(PIN_RESPONSE, GPIO.IN)


while True:
    var = GPIO.input(PIN_RESPONSE)
    print(str(var))
