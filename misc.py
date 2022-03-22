# Misc functions

import config
import datetime
import detect

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