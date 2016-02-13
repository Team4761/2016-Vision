#!/usr/bin/python2.7

"""
Program for taking a bunch of pictures at different distances and 
exposure levels. You can then use the images with GRIP or something to
get a good shutter speed and color range values.

Run: $ python temporary_tuner.py
Use: Enter how far away you are in inches from the high goal and press
     enter. The program will take a few pictures and prompt you again.
     Enter "quit" when you get the prompt to end the program. File names
     will follow the format "frame-DISTANCE-SHUTTERSPEED.jpg".
"""

import cv2
import picamera
import picamera.array
import numpy
import time

lower_bound = numpy.array([0,202,0])
upper_bound = numpy.array([255,255,179])

shutter_speeds = [x * 200 for x in range(1, 6)]

cmd = None

with picamera.PiCamera() as camera:
	with picamera.array.PiRGBArray(camera) as stream:
		cmd = raw_input("Enter distance (or quit): ")
		while cmd != "quit":
			for shutter_speed in shutter_speeds:
				stream.seek(0)
				stream.truncate()
				camera.shutter_speed = shutter_speed
				time.sleep(0.5)
				file_name = "frame-{}-{}.jpg".format(cmd, shutter_speed)
				print "Capping at distance {} and shutterspeed {} (really {}), filename {}".format(cmd, shutter_speed, camera.shutter_speed, file_name)
				camera.capture(stream, format="bgr", use_video_port=True)
				frame = stream.array
				cv2.imwrite(file_name, frame)
			cmd = raw_input("Enter distance (or quit): ")
