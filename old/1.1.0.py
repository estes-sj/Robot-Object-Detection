#Authors: Samuel Estes and Trevor Weygandt
#Resources: https://rawgit.com/dusty-nv/jetson-inference/dev/docs/html/python/jetson.inference.html#detectNet

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
import atexit
from art import *

import numpy as np
import Jetson.GPIO as GPIO


sudoPassword = 'Rah2022'
command = 'xrandr --output HDMI-0 --mode 1920x1080'
p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
command = 'sudo systemctl restart nvargus-daemon'
p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
GPIO.cleanup()

#
# object detection setup
#
net = jetson.inference.detectNet(argv=['--threshold=0.70','--model=/home/ece/jetson-inference/python/training/detection/ssd/models/capstone/ssd-mobilenet.onnx', 
'--labels=/home/ece/jetson-inference/python/training/detection/ssd/models/capstone/labels.txt', '--input-blob=input_0', '--output-cvg=scores', 
'--output-bbox=boxes']) # custom training model

# Pin Definitions
# Outputs
PIN_LEFT = 17		# white pin: 11
PIN_RIGHT = 27		# grey  pin: 13
PIN_LAUNCH = 22		# purple pin: 15
PIN_ARM = 10		# blue	pin: 19
PIN_CONTROL = 9		# green	pin: 21
# Input
PIN_RESPONSE = 11	# yellow	pin: 23

# Flags
# 0 = Center, 1 = Left of Center, 2 = Right of Center
ALIGNMENT = 0x0
global ALIGNED
global LOADED
global DETECT_TREE
global DETECT_NET
global RESPONSE
state = 0x0
RESUME = 0

# State Machine
IDLE_TREE = 0x0
ALIGN_TREE = 0x1
IDLE_NET = 0x2
ALIGN_NET = 0x3
STALL = 0x4

# Alignment Flags
LOADED = 0
ALIGNED = 0
DETECT_TREE = 0
DETECT_NET = 0
RESPONSE = 0

# Alignment Coordinates
TREE_COORD = 850
NET_COORD = 450


# Setup GPIO Pins
def GPIOsetup():
	GPIO.setmode(GPIO.BCM)

	# Outputs
	GPIO.setup(PIN_LEFT, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(PIN_RIGHT, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(PIN_LAUNCH, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(PIN_ARM, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(PIN_CONTROL, GPIO.OUT, initial=GPIO.LOW)

	# Input
	GPIO.setup(PIN_RESPONSE, GPIO.IN)	

# Alignment Function
def align(object, objectCenter):
	global ALIGNED
	global LOADED
	global DETECT_TREE
	global DETECT_NET
	global RESPONSE

	coord = object
	print("Center = " + str(object))
	print("Object Center = " + str(objectCenter))

	# Choose which coordinate to align with
	if (object == "Tree"):
		coord = TREE_COORD
		command = PIN_ARM
	elif (object == "Net"):
		coord = NET_COORD
		command = PIN_LAUNCH

	# If Aligned throw brake flag
	if ((coord < objectCenter + 20) & (coord > objectCenter - 20)):
		ALIGNMENT = 0x0
		ALIGNED = 1
		GPIO.output(PIN_CONTROL, GPIO.HIGH)
		GPIO.output(PIN_LEFT, GPIO.LOW)
		GPIO.output(PIN_RIGHT, GPIO.LOW)
		GPIO.output(command, GPIO.HIGH)
		if (object == "Tree"):
			LOADED = 1
		elif (object == "Net"):
			LOADED = 0

	else:
		ALIGNMENT = 0x0
		ALIGNED = 0
		GPIO.output(PIN_CONTROL, GPIO.LOW)
		GPIO.output(PIN_LEFT, GPIO.LOW)
		GPIO.output(PIN_RIGHT, GPIO.LOW)
		GPIO.output(command, GPIO.LOW)

	# Visual Debug
	net.Allignment(ALIGNMENT)

#
# main
#
def main():
	global ALIGNED
	global LOADED
	global DETECT_TREE
	global DETECT_NET
	global RESPONSE	

	# Initialize GPIO
	GPIOsetup()

	# State machine setup
	state = IDLE_TREE
	nextState = IDLE_TREE
	print(str(state))

	while True:
		try:
			# open streams for camera 0
			camera_0 = jetson.utils.videoSource("csi://0")      # '/dev/video0' for V4L2
			display_0 = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file
			print(getTime() + "Camera 0 started...\n")
			break
		except:
			p = os.system('echo %s|sudo -S %s' % (sudoPassword, command))
			print(getTime() + "Camera 0 failed to start...restarting")
			time.sleep(3)
			print(getTime() + "Done!\n")


	while display_0.IsStreaming(): #and display_1.IsStreaming():
		img_0 = camera_0.Capture()
		detections_0 = net.Detect(img_0)
		display_0.Render(img_0)
		display_0.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

		# print the detections
		print(getTime() + "----------CAMERA 0------------")
		print(getTime() + "detected {:d} objects in image".format(len(detections_0)))


		# interact with detections on cam 0
		for detection in detections_0:
			# print(detection)
			class_name = net.GetClassDesc(detection.ClassID)
			print(class_name + " Detected!")
			
			# Response from Arduino
			RESUME = GPIO.input(PIN_RESPONSE)
	
			state = nextState
			print(str(ALIGNED))

			# State machine states
			# Look for tree
			if (state == IDLE_TREE):
				print("--IDLE TREE--")
				# When tree is detected begin aligning
				if (DETECT_TREE == 1):
					nextState = ALIGN_TREE
			# Align with tree
			elif (state == ALIGN_TREE):
				print("--ALIGN TREE--")
				# Once beads loaded begin looking for the net
				if (ALIGNED == 1):
					nextState = STALL
					DETECT_TREE = 0
			# Look for net
			elif (state == IDLE_NET):		# needs to be changed back to elif
				print("--IDLE NET--")
				# When net is detected begin aligning
				if (DETECT_NET == 1):
					nextState = ALIGN_NET
			# Align with net
			elif (state == ALIGN_NET):
				print("--ALIGN NET--")
				# When beads are no longer loaded (fired) begin looking for tree
				if (ALIGNED == 1):
					# nextState = IDLE_TREE
					nextState = STALL
					DETECT_NET = 0

			# Stall state
			elif (state == STALL):
				print("--STALL--")
				# If given resume command and the beads are loaded begin looking for net
				if (RESUME == 1 and LOADED == 1):
					ALIGNED = 0
					nextState = IDLE_NET
				# If given resume command and the beads have been launched begin looking for tree
				elif (RESUME == 1 and LOADED == 0):
					ALIGNED = 0
					nextState = IDLE_TREE

			# State machine implementation
			# Find Tree
			if (state == IDLE_TREE):
				ALIGNED = 0
				# Set all Control Pins LOW
				GPIO.output(PIN_CONTROL, GPIO.LOW)
				GPIO.output(PIN_ARM, GPIO.LOW)
				GPIO.output(PIN_LAUNCH, GPIO.LOW)
				# Check if tree
				if (class_name == "Tree"):
					DETECT_TREE = 1
					DETECT_NET = 0

			# Align with tree
			elif (state == ALIGN_TREE):
				# Check if tree
				if (class_name == "Tree"):
					# Align
					center = getCenter(detection)
					imgCenter = getImgCenter(display_0)
					align(class_name, int(center[0]))

				ALIGNMENT = 0x0

			# Find net
			elif (state == IDLE_NET):
				ALIGNED =0
				# Set all Control Pins LOW
				GPIO.output(PIN_CONTROL, GPIO.LOW)
				GPIO.output(PIN_ARM, GPIO.LOW)
				GPIO.output(PIN_LAUNCH, GPIO.LOW)
				# Check if net
				if (class_name == "Net"):
					print(class_name)
					DETECT_TREE = 0
					DETECT_NET = 1

			# Align with net
			elif (state == ALIGN_NET):
				# Check if net
				if (class_name == "Net"):
					# Align
					center = getCenter(detection)
					imgCenter = getImgCenter(display_0)
					align(class_name, int(center[0]))

				ALIGNMENT = 0x0

			# Stall State
			elif (state == STALL):
				print("Class = " + str(class_name) + " Coord = " + str(center))
				pass


# Get Overlay Width
def getWidth(detection):
	width = detection.Right - detection.Left
	print("Width = " + str(width) )
	return width

# Get Overlay Height
def getHeight(detection):
	height = detection.Bottom - detection.Top
	print("Height = " + str(height)) 
	return height

# Get Overlay Center
def getCenter(detection):
	center = [(detection.Right + detection.Left)/2, (detection.Bottom + detection.Top/2)]
	#print("Center = (" + str(center[0]) + ", " + str(center[1]) + ")")
	return center

# Get Image Center
def getImgCenter(display_0):
	width = display_0.GetWidth()
	height = display_0.GetHeight()
	imgCenter = [width/2, height/2]
	#print("Image Center = (" + str(imgCenter[0]) + ", " + str(imgCenter[1]) + ")" )
	return imgCenter

# Get Coordinates of Center of Box
def boxCoord(detection):
	width = getWidth(detection)
	left = detection.Left
	coord_x = left + width/2
	return coord_x

def getTime():
	# Get current date and time
	dt = datetime.datetime.now()
	# Format datetime string
	x = dt.strftime("[%Y-%m-%d %H:%M:%S]	")
	return str(x)

def exit_handler():
	GPIO.cleanup()
	print("""
░░░█             █ ▀
░░░░▓█       ▄▄▀▀█
░░░░▒░█    ▄█▒░░▄░█
░░░░░░░▀▄ ▄▀▒▀▀▀▄▄▀  DO
░░░░░░░░░█▒░░░░▄▀    IT
▒▒▒░░░░▄▀▒░░░░▄▀     FOR
▓▓▓▓▒░█▒░░░░░█▄      JERRY
█████▀▒░░░░░█░▀▄
█████▒▒░░░▒█░░░▀▄
███▓▓▒▒▒▀▀▀█▄░░░░█
▓██▓▒▒▒▒▒▒▒▒▒█░░░░█
▓▓█▓▒▒▒▒▒▒▓▒▒█░░░░░█
░▒▒▀▀▄▄▄▄█▄▄▀░░░░░░░█""")

	print("Last State = " + str(state))

# Run main
if __name__ == '__main__':
	main()
	atexit.register(exit_handler)


