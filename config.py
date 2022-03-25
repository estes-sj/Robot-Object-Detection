# Config File for all flags 

#
# Pin Definitions
#
# Outputs
PIN_LEFT = 26		# white pin: 37
PIN_RIGHT = 27		# grey  pin: 13
PIN_LAUNCH = 22		# purple pin: 15
PIN_ARM = 10		# blue	pin: 19
PIN_CONTROL = 9		# green	pin: 21
PIN_GREEN = 17      # dark green pin: 11

# Input
PIN_RESPONSE = 11	# yellow	pin: 23
PIN_REBOOT = 20     # red pin: 38
#
# State Machine
#
IDLE_TREE = 0x0
ALIGN_TREE = 0x1
IDLE_NET = 0x2
ALIGN_NET = 0x3
STALL = 0x4

#
# Alignment Flags
#
LOADED = 0
ALIGNED = 0
DETECT_TREE = 0
DETECT_NET = 0
RESPONSE = 0

#
# Alignment Coordinates
#
TREE_COORD = 875
NET_COORD = 425