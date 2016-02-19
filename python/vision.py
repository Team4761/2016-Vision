#!/usr/bin/python2.7

import cv2
import logging
import numpy
import picamera
import picamera.array
import math
from networktables import NetworkTable
import sys
import time

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

log.debug("Initialized logger...")

# define range of color in BGR
lower_bound = numpy.array([0,110,0])
upper_bound = numpy.array([255,255,84])

global table
table = None
using_networktables = True #For debugging

def _init_networktables():
	if not using_networktables:
		raise Exception("Attempted to initialize NetworkTables while NetworkTables is disabled!")
	NetworkTable.setIPAddress("roborio-4761-frc.local")
	NetworkTable.setClientMode()
	NetworkTable.initialize()
	global table
	table = NetworkTable.getTable("vision")
	log.info("Initialized NetworkTables")

# Loads dict into networktables
def write_to_networktables(data):
	if table is None:
		_init_networktables()
	try:
		if not table.isConnected():
			log.warning("Not connected to a NetworkTables server (nothing will actually be sent)")
		for key in data.keys():
			table.putNumber(key, data[key])
		log.info("Loaded data into NetworkTable")
	except KeyError:
		log.exception("Something in NetworkTables didn't work, see stacktrace for details")

with picamera.PiCamera() as camera:
	#camera.framerate = 16
	camera.shutter_speed = 200
	log.info("Initialized camera")
	count = 0
	max_frames = int(sys.argv[1])
	time.sleep(0.5) #Shutter speed is not set instantly. This allows changes to take effect.
	with picamera.array.PiRGBArray(camera) as stream:
		for foo in camera.capture_continuous(stream, format="bgr", use_video_port=True):
			log.info("Captured image. Starting to process...")
			
			stream.seek(0)
			stream.truncate()
			frame = stream.array
			log.debug("Converted data to array")
			
			# Threshold the BGR image
			mask = cv2.inRange(frame, lower_bound, upper_bound)
			log.debug("Performed thresholding operation")
			
			ret, thresh = cv2.threshold(mask, 127, 255, 0)
			contours, hierarchy = cv2.findContours(thresh, 3, 2)
			log.debug("Discovered contours")
			
			try:
				#Remember, if someone offers you functional programming just say NO! and run away
				#These two lines find the largest contour by perimeter in the image
				contours_poly = [cv2.approxPolyDP(contour, 3, True) for contour in contours]
				largest_contour = sorted(contours_poly, key=lambda cp: -cv2.arcLength(cp, True))[0]
			except IndexError:
				log.error("No contours found. Continuing...")
				count += 1
				if count >= max_frames:
					break
				continue
			
			topleft_x, topleft_y, width, height = cv2.boundingRect(largest_contour)
			log.debug("Calculated bounding shapes")
			
			t = sorted(largest_contour, key=lambda x: x[0][0])
			leftmost = t[0][0]
			second_leftmost = t[1][0]
			rightmost = t[::-1][0][0]
			second_rightmost = t[::-1][1][0]
			
			left_length = math.sqrt((leftmost[0] - second_leftmost[0])**2 + (leftmost[1] - second_leftmost[1])**2)
			right_length = math.sqrt((rightmost[0] - second_rightmost[0])**2 + (rightmost[1] - second_rightmost[1])**2)
			
			#cv2.rectangle(frame, (topleft_x, topleft_y), (topleft_x + width, topleft_y + height), (255,255,255), 3)
			#cv2.imwrite("modded{}.jpg".format(count), frame)
			#log.info("Wrote image!")
			
			if using_networktables:
				data = {
					"topleft_x": topleft_x,
					"topleft_y": topleft_y,
					"width": width,
					"height": height,
					"horiz_offset": (topleft_x + (width / 2)) - (camera.resolution[0] / 2),
					"distance_guess": -0.28478 * height + 43.143,
					"left_side_length": left_length,
					"right_side_length": right_length,
				}
				write_to_networktables(data)
			
			count += 1
			if count >= max_frames:
				break
