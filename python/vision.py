#!/usr/bin/python2.7

import cv2
import logging
import numpy
import picamera
import picamera.array
from networktables import NetworkTable
import time

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

log.debug("Initialized logger...")

# define range of color in BGR
lower_bound = numpy.array([0,60,0])
upper_bound = numpy.array([100,205,95])

table = None
using_networktables = False

def _init_networktables():
	if not using_networktables:
		raise Exception("Attempted to initialize NetworkTables while NetworkTables is disabled!")
	NetworkTable.setIPAddress("roborio-4761-frc.local")
	NetworkTable.setClientMode()
	NetworkTable.initialize()
	table = NetworkTable.getTable("vision")
	log.info("Initialized NetworkTables")

def write_to_networktables(data):
	if table is None:
		init_networktables()
	try:
		if not table.isConnected():
			log.warning("Not connected to a server. Hmmm... (not actually writing anything)")
		table.putNumber("r_tl_x", data["r_tl_x"])
		table.putNumber("r_tl_y", data["r_tl_y"])
		table.putNumber("r_width", data["r_width"])
		table.putNumber("r_height", data["r_height"])
		table.putNumber("c_center_x", data["c_center_x"])
		table.putNumber("c_center_y", data["c_center_y"])
		table.putNumber("c_radius", data["c_radius"])
		log.info("Loaded data into NetworkTables")
	except KeyError:
		log.exception("Something in NetworkTables didn't work, see stacktrace for details")

def get_length(contour_poly):
	return cv2.arcLength(contour_poly, True)

with picamera.PiCamera() as camera:
	camera.framerate = 16
	camera.shutter_speed = 400
	log.info("Initialized camera")
	count = 0
	max_frames = 10
	with picamera.array.PiRGBArray(camera) as stream:
		for foo in camera.capture_continuous(stream, format="bgr", use_video_port=True):
			log.info("Captured image. Starting to process...")
			
			stream.seek(0)
			stream.truncate()
			frame = stream.array
			log.debug("Converted data to array")
			#cv2.imwrite("Original{}.jpg".format(count), frame)
			
			# Threshold the BGR image
			mask = cv2.inRange(frame, lower_bound, upper_bound)
			log.debug("Performed thresholding operation")
			#cv2.imwrite("Mask.jpg", mask)
			
			ret, thresh = cv2.threshold(mask, 127, 255, 0)
			contours, hierarchy = cv2.findContours(thresh, 3, 2)
			log.debug("Discovered contours")
			
			#Remember, if someone offers you functional programming just say NO! and run away
			#These two lines find the largest contour by perimeter in the image
			contours_poly = [cv2.approxPolyDP(contour, 3, True) for contour in contours]
			largest_contour = sorted(contours_poly, key=lambda cp: -cv2.arcLength(cp, True))[0]
			
			r_tl_x, r_tl_y, r_width, r_height = cv2.boundingRect(largest_contour)
			c_center, c_radius = cv2.minEnclosingCircle(largest_contour)
			log.debug("Calculated bounding shapes")
			
			cv2.rectangle(frame, (r_tl_x, r_tl_y), (r_tl_x + r_width, r_tl_y + r_height), (0,255,0), 3)
			#cv2.imwrite("modded{}.jpg".format(count), frame)
			
			if using_networktables:
				data = {}
				data["r_tl_x"] = r_tl_x
				data["r_tl_y"] = r_tl_y
				data["r_width"] = r_width
				data["r_height"] = r_height
				data["c_center_x"] = c_center[0]
				data["c_center_y"] = c_center[1]
				data["c_radius"] = c_radius
				write_to_networktables(data)
			
			count += 1
			if count >= max_frames:
				break
