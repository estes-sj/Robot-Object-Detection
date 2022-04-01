# File for aligning robot with object

import config
import gpio

def alignment(object1, objectCenter):
    coord = 0
    print("Center = " + str(object1))
    print("Object Center = " + str(objectCenter))

    # Choose which coordinate to align with
    if (object1 == "Tree"):
        coord = config.TREE_COORD
        command = config.PIN_ARM
    elif (object1 == "Net"):
        coord = config.NET_COORD
        command = config.PIN_LAUNCH

    # If Aligned throw brake flag
    if ((coord < objectCenter + config.ALIGN_WIDTH) & (coord > objectCenter - config.ALIGN_WIDTH)):
        config.ALIGNED = 1
        gpio.set_high(config.PIN_CONTROL)
        gpio.set_low(config.PIN_LEFT)
        gpio.set_low(config.PIN_RIGHT)
        gpio.set_high(command)

        if (object1 == "Tree"):
            config.LOADED = 1
        elif (object1 == "Net"):
            config.LOADED = 0


    else:
        config.ALIGNED = 0
        gpio.set_low(config.PIN_CONTROL)
        gpio.set_low(config.PIN_LEFT)
        gpio.set_low(config.PIN_RIGHT)
        gpio.set_low(command)