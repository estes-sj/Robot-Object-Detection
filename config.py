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
IDLE = 0x5

#
# Alignment Flags
#
LOADED = 0
ALIGNED = 0
DETECT_TREE = 0
DETECT_NET = 0
RESPONSE = 0

#
# Alignment Coordinates (Pixels)
#
ALIGN_WIDTH = 15        # Multiply by 2 to get width of box
TREE_COORD = 850        # Robot Right = Subtract,  Robot Left = Add
NET_COORD = 420         # Robot Right = Add, Robot Left = Subtract

#
# Number of Iterations
#
CURRENT_RUNS = 0
MAX_RUNS = 4