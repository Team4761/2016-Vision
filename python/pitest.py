import cv2
import logging
import networktables
import picamera
import picamera.array
import sys

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

write = True
try:
	with picamera.PiCamera() as camera:
		#camera.resolution = (320, 240)
		for x in range(1, 11):
			log.info("picture number {}".format(x))
			with picamera.array.PiRGBArray(camera) as stream:
				log.info("Capturing image...")
				camera.capture(stream, format="bgr")
				log.info("Converting stream to array...")
				image = stream.array
				log.info("Blurring...")
				blurred_image = cv2.blur(image, (20, 20))
				if write == True:
					cv2.imwrite("image.jpg", blurred_image)
					write = False

except picamera.exc.PiCameraError as e:
	log.exception("Could not connect to camera. See stack trace for more info.")
