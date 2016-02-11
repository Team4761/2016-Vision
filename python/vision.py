#!/usr/bin/python2.7

import cv2
import io
import logging
import numpy
import picamera
import picamera.array
from networktables import NetworkTable
import time

logging.basicConfig(level=logging.CRITICAL)
log = logging.getLogger()

log.debug("Initialized logger...")

# define range of color in HSV
lower_bound = numpy.array([0,30,105])
upper_bound = numpy.array([104,255,255])

# networktables setup
NetworkTable.setIPAddress("roborio-4761-frc.local")
NetworkTable.setClientMode()
NetworkTable.initialize()
table = NetworkTable.getTable("vision")
log.info("Initialized NetworkTables")

with picamera.PiCamera() as camera:
	camera.framerate = 16
	camera.shutter_speed = 7000
	log.info("Initialized camera")
	count = 0
	max = 10
	stream = io.BytesIO()
	start = time.time()
	for foo in camera.capture_continuous(stream, format="jpeg", use_video_port=True):
		log.info(str(time.time() - start) + "Captured image. Starting to process...")
		
		stream.truncate()
		stream.seek(0)
		data = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)
		frame = cv2.imdecode(data, 1)
		log.debug(str(time.time() - start) + "Converted data to array")
		
		# Convert BGR to HSV
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		log.debug(str(time.time() - start) + "Converted BGR data to HSV")
		
		# Threshold the HSV image
		mask = cv2.inRange(hsv, lower_bound, upper_bound)
		log.debug(str(time.time() - start) + "Performed thresholding operation")
		
		ret, thresh = cv2.threshold(mask, 127, 255, 0)
		contours, hierarchy = cv2.findContours(thresh, 3, 2)
		log.debug(str(time.time() - start) + "Discovered contours")
		
		largest_contour = None
		largest_contour_length = None

		for contour in contours:
			contour_poly = cv2.approxPolyDP(contour, 3, True)
			current_contour_length = cv2.arcLength(contour_poly, True)
			if current_contour_length > largest_contour_length:
				largest_contour = contour_poly
				largest_contour_length = current_contour_length
		log.debug(str(time.time() - start) + "Filtered contours")
		
		r_tl_x, r_tl_y, r_width, r_height = cv2.boundingRect(largest_contour)
		c_center, c_radius = cv2.minEnclosingCircle(largest_contour)
		log.debug(str(time.time() - start) + "Calculated bounding shapes")

		try:
			if not table.isConnected():
				log.warning("Not connected to a server. Hmmm... (not actually writing anything)")
			table.putNumber("r_tl_x", r_tl_x)
			table.putNumber("r_tl_y", r_tl_y)
			table.putNumber("r_width", r_width)
			table.putNumber("r_height", r_height)
			table.putNumber("c_center_x", c_center[0])
			table.putNumber("c_center_y", c_center[1])
			table.putNumber("c_radius", c_radius)
			log.info("Loaded data into NetworkTables")
		except KeyError:
			log.exception("Something in NetworkTables didn't work, see stacktrace for details")

		count += 1
		if count >= max:
			break
