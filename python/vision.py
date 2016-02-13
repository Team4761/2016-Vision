#!/usr/bin/python2.7

import argparse
import cv2
import logging
import numpy
import picamera
import picamera.array
import math
from networktables import NetworkTable
import sys
import time

parser = argparse.ArgumentParser(description="4761's 2016 vision program")
parser.add_argument("max_frames", metavar="N", type=int, help="Number of pictures to take")
parser.add_argument("--networktables-ip", metavar="", type=str, default="roborio-4761-frc.local", help="IP address of the desired NetworkTables server")
parser.add_argument("--use-networktables", metavar="", type=bool, default=False, help="Should values be published to NetworkTables?")
parser.add_argument("--write-images", metavar="", type=bool, default=False, help="Should images for debugging be written?")
args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

log.debug("Initialized logger...")

# define range of color in BGR
lower_bound = numpy.array([0,110,0])
upper_bound = numpy.array([255,255,84])

global table
table = None
using_networktables = args.use_networktables

def crop_image(image, topleft_x, topleft_y, width, height):
	return image[topleft_y:topleft_y + height, topleft_x:topleft_x + width]

def write_image(file_name, image_data):
	if args.write_images:
		log.debug("Writing image {}...".format(file_name))
		cv2.imwrite(file_name, image_data)

def get_distance_between(pt1, pt2):
	#sqrt((x2 - x1)^2 + (y2 - y1)^2)
	return math.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)

def init_networktables():
	#TODO: Check to see if NetworkTables is already initialized
	if not using_networktables:
		raise Exception("Attempted to initialize NetworkTables while NetworkTables is disabled!")
	NetworkTable.setIPAddress(args.networktables_ip)
	NetworkTable.setClientMode()
	NetworkTable.initialize()
	global table
	table = NetworkTable.getTable("vision")
	log.info("Initialized NetworkTables")

# Loads dict into networktables
def write_to_networktables(data):
	if table is None:
		log.debug("NetworkTables is not intialized! Initializing...")
		init_networktables()
	try:
		if not table.isConnected():
			log.warning("Not connected to a NetworkTables server (nothing will actually be sent)")
		for key in data.keys():
			table.putNumber(key, data[key])
		log.info("Loaded data into NetworkTable")
	except KeyError:
		log.exception("Something in NetworkTables didn't work, see stacktrace for details")

with picamera.PiCamera() as camera:
	camera.shutter_speed = 200
	time.sleep(0.5) #Shutter speed is not set instantly. This wait allows time for changes to take effect.
	log.info("Initialized camera")
	count = 0
	max_frames = args.max_frames
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
				if len(largest_contour) == 8:
					log.debug("Got perfect 8 contours! :D")
				else:
					log.debug("Got {} contours instead of 8. :\\".format(len(largest_contour)))
			except IndexError:
				log.error("No contours found. Continuing...")
				count += 1
				if count >= max_frames:
					break
				continue
			
			topleft_x, topleft_y, width, height = cv2.boundingRect(largest_contour)
			log.debug("Calculated bounding shapes")
			
			bottom_point = sorted(largest_contour, key=lambda x:x[0][1])[::-1][0]
			bb_distance_from_bottom = camera.resolution[1] - bottom_point[0][1]
			
			t = sorted(largest_contour, key=lambda x: x[0][0])
			
			leftmost = t[0][0]
			rightmost = t[::-1][0][0]
			
			#TODO: Fail gracefully if no valid second point
			#TODO: Fail gracefully if only one point (total) found
			#get second leftmost
			for line in t:
				if get_distance_between(leftmost, line[0]) > 50:
					second_leftmost = line[0]
					break
			
			#get second rightmost
			for line in t[::-1]:
				if get_distance_between(rightmost, line[0]) > 50:
					second_rightmost = line[0]
					break
			
			left_length = get_distance_between(leftmost, second_leftmost)
			right_length = get_distance_between(rightmost, second_rightmost)

			if using_networktables:
				data = {
					"topleft_x": topleft_x,
					"topleft_y": topleft_y,
					"width": width,
					"height": height,
					"horiz_offset": (topleft_x + (width / 2)) - (camera.resolution[0] / 2),
					"distance_guess": 14.722 * 0.99844**bb_distance_from_bottom,
					"left_side_length": left_length,
					"right_side_length": right_length,
				}
				write_to_networktables(data)
			
			count += 1
			if count >= max_frames:
				break
