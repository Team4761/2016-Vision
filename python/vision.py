#!/usr/bin/python

import cv2
import numpy
import picamera

from networktables import NetworkTable

# define range of color in HSV
lower_bound = numpy.array([0,30,105])
upper_bound = numpy.array([104,255,255])

# networktables setup
NetworkTable.setIPAddress("roborio-4761-frc.local")
NetworkTable.setClientMode()
NetworkTable.initialize()

table = NetworkTable.getTable("vision")

with picamera.PiCamera() as camera:
	#camera.resolution = (w, h)
	#camera.shutter_speed = Who knows?
	with picamera.array.PiRGBArray(camera) as stream:
		camera.capture(stream, format="bgr")
		frame = stream.array

		# Convert BGR to HSV
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		# Threshold the HSV image
		mask = cv2.inRange(hsv, lower_bound, upper_bound)

		ret, thresh = cv2.threshold(mask, 127, 255, 0)
		contours, hierarchy = cv2.findContours(thresh, 3, 2)

		largest_contour = None
		largest_contour_length = None

		for contour in contours:
			contour_poly = cv2.approxPolyDP(contour, 3, True)
			current_contour_length = cv2.arcLength(contour_poly, True)
			if current_contour_length > largest_contour_length:
				largest_contour = contour_poly
				largest_contour_length = current_contour_length

		r_tl_x, r_tl_y, r_width, r_height = cv2.boundingRect(largest_contour)
		c_center, c_radius = cv2.minEnclosingCircle(largest_contour)
		
		try:
			table.putNumber("r_tl_x", r_tl_x)
			table.putNumber("r_tl_y", r_tl_y)
			table.putNumber("r_width", r_width)
			table.putNumber("r_height", r_height)
			table.putNumber("c_center", c_center)
			table.putNumber("c_radius", c_radius)
		except KeyError:
			print "something didn't work with networktables :|"
