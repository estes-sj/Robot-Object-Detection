# Computer Vision Object Detection

import config
import misc
import align
import gpio
import os
from ctypes import alignment
from hashlib import algorithms_guaranteed
import jetson.inference
import jetson.utils
from time import sleep

import numpy as np

def detection():
    #
    # object detection setup
    #
    sudoPassword = 'Rah2022'
    command = 'sudo systemctl restart nvargus-daemon'

    net = jetson.inference.detectNet(argv=['--threshold=0.8','--model=/home/ece/jetson-inference/python/training/detection/ssd/models/capstone/ssd-mobilenet.onnx', 
    '--labels=/home/ece/jetson-inference/python/training/detection/ssd/models/capstone/labels.txt', '--input-blob=input_0', '--output-cvg=scores', 
    '--output-bbox=boxes']) # custom training model

    # State machine setup
    state = config.IDLE_TREE
    nextState = config.IDLE_TREE
    config.CURRENT_RUNS = 0
    print(str(state))

    while True:
        try:
            # open streams for camera 0
            camera_0 = jetson.utils.videoSource("csi://0")      # '/dev/video0' for V4L2
            display_0 = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file
            print(misc.getTime() + "Camera 0 started...\n")
            break
        except:
            os.system('echo %s|sudo -S %s' % (sudoPassword, command))
            print(misc.getTime() + "Camera 0 failed to start...restarting")
            sleep(3)
            print(misc.getTime() + "Done!\n")



    while display_0.IsStreaming():
        img_0 = camera_0.Capture()
        detections_0 = net.Detect(img_0)
        display_0.Render(img_0)
        display_0.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

        # print the detections
        print(misc.getTime() + "----------CAMERA 0------------")
        print(misc.getTime() + "detected {:d} objects in image".format(len(detections_0)))


        # interact with detections on cam 0
        for detection in detections_0:
            # print(detection)
            class_name = net.GetClassDesc(detection.ClassID)
            print(class_name + " Detected!")
            
            # Response from Arduino
            RESUME = gpio.read_pin(config.PIN_RESPONSE)
                        

            state = nextState

            
            # State machine states
            # Look for tree
            if (state == config.IDLE_TREE):
                print("--IDLE TREE--")
                # When tree is detected begin aligning
                if (config.DETECT_TREE == 1):
                    nextState = config.ALIGN_TREE
            # Align with tree
            elif (state == config.ALIGN_TREE):
                print("--ALIGN TREE--")
                # Once beads loaded begin looking for the net
                if (config.ALIGNED == 1):
                    nextState = config.STALL
                    config.DETECT_TREE = 0
            # Look for net
            elif (state == config.IDLE_NET):		# needs to be changed back to elif
                print("--IDLE NET--")
                # When net is detected begin aligning
                if (config.DETECT_NET == 1):
                    nextState = config.ALIGN_NET
            # Align with net
            elif (state == config.ALIGN_NET):
                print("--ALIGN NET--")
                # When beads are no longer loaded (fired) begin looking for tree
                if (config.ALIGNED == 1):
                    # nextState = config.IDLE_TREE
                    nextState = config.STALL
                    config.DETECT_NET = 0

            # Stall state
            elif (state == config.STALL):
                print("--STALL--")

                # If given resume command and the beads are loaded begin looking for net
                if (RESUME == 1 and config.LOADED == 1):
                    config.ALIGNED = 0
                    nextState = config.IDLE_NET
                    # Add Iteration
                    config.CURRENT_RUNS += 1
                # If given resume command and the beads have been launched begin looking for tree
                elif (RESUME == 1 and config.LOADED == 0):
                    config.ALIGNED = 0
                    nextState = config.IDLE_TREE
                    # Add Iteration
                    config.CURRENT_RUNS += 1


            #
            # State machine implementation
            # Find Tree
            if (state == config.IDLE_TREE):
                config.ALIGNED = 0
                # Set all Control Pins LOW
                gpio.set_low(config.PIN_CONTROL)
                gpio.set_low(config.PIN_ARM)
                gpio.set_low(config.PIN_LAUNCH)
                # Check if tree
                if (class_name == "Tree"):
                    config.DETECT_TREE = 1
                    config.DETECT_NET = 0

            # Align with tree
            elif (state == config.ALIGN_TREE):
                # Check if tree
                if (class_name == "Tree"):
                    # Align
                    center = misc.getCenter(detection)
                    imgCenter = misc.getImgCenter(display_0)
                    align.alignment(class_name, int(center[0]))


            # Find net
            elif (state == config.IDLE_NET):
                config.ALIGNED =0
                # Set all Control Pins LOW
                gpio.set_low(config.PIN_CONTROL)
                gpio.set_low(config.PIN_ARM)
                gpio.set_low(config.PIN_LAUNCH)
                # Check if net
                if (class_name == "Net"):
                    print(class_name)
                    config.DETECT_TREE = 0
                    config.DETECT_NET = 1

            # Align with net
            elif (state == config.ALIGN_NET):
                # Check if net
                if (class_name == "Net"):
                    # Align
                    center = misc.getCenter(detection)
                    imgCenter = misc.getImgCenter(display_0)
                    align.alignment(class_name, int(center[0]))

            # Stall State
            elif (state == config.STALL):
                print("Class = " + str(class_name) + " Coord = " + str(center))
                pass

        # Status LEDs
        gpio.set_high(config.PIN_GREEN)

        REBOOT = gpio.read_pin(config.PIN_REBOOT)

        # Pin to reboot
        if (REBOOT == 1):
            sudoPassword = 'Rah2022'
            command = 'sudo reboot now'
            os.system('echo %s|sudo -S %s' % (sudoPassword, command))