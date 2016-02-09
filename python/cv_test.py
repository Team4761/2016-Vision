import cv2
import numpy as np
import time

frame = cv2.imread("RealFullField/3.jpg")

# Convert BGR to HSV
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# define range of blue color in HSV
lower_bound = np.array([0,30,105])
upper_bound = np.array([104,255,255])

# Threshold the HSV image to get only blue colors
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

tl_x, tl_y, width, height = cv2.boundingRect(largest_contour)
center, radius = cv2.minEnclosingCircle(largest_contour)
