from .camera import get_frame, resolution
from .network import vision_table
import cv2
import numpy
import time

lower_bound = numpy.array([0,42,0])
upper_bound = numpy.array([255,191,35])


def process_frames():
    while True:
        frame = get_frame()
        if frame is not None:
            # Threshold the BGR image
            mask = cv2.inRange(frame, lower_bound, upper_bound)
            print "Performed thresholding operation"

            ret, thresh = cv2.threshold(mask, 127, 255, 0)
            contours, hierarchy = cv2.findContours(thresh, 3, 2)
            print "Discovered contours"

            try:
                contours_poly = [cv2.approxPolyDP(contour, 3, True) for contour in contours]
                largest_contour = sorted(contours_poly, key=lambda cp: -cv2.arcLength(cp, True))[0]
                if len(largest_contour) == 8:
                    print "Got perfect 8 contours! :D"
                else:
                    print "Got {} contours instead of 8. :\\".format(len(largest_contour))
            except IndexError:
                print "No contours found. Ending processing for this frame..."
                vision_table.write_dict({"can_see_target": 0})
                continue

            topleft_x, topleft_y, width, height = cv2.boundingRect(largest_contour)
            print "Calculated bounding shapes"

            bottom_point = sorted(largest_contour, key=lambda x:x[0][1])[::-1][0]
            bb_distance_from_bottom = resolution[1] - bottom_point[0][1]

            print "Distance from bottom (px): {}".format(bb_distance_from_bottom)

            not_valid = True
            # Check that area of bounding box is more that 3600 pixels (60x60)
            # TODO: Is this reasonable?
            if not width * height < 3600:
                not_valid = False

            if not_valid:
                print "No reasonable shapes found. Ending processing for this frame..."
                vision_table.write_dict({"can_see_target": 0})
                continue

            distance = 10.648 * 0.99857**bb_distance_from_bottom
            print "Distance to target: {} feet".format(distance)
            offsets = get_offsets(topleft_x, width, resolution)
            data = {
                "topleft_x": topleft_x,
                "topleft_y": topleft_y,
                "width": width,
                "height": height,
                "horiz_offset": offsets["angle_offset"],
                "pixel_offset": offsets["pixel_offset"],
                "bp_dist_from_bottom": bb_distance_from_bottom,
                "distance_guess": distance,
                "heartbeat": 1,
                "can_see_target": 1,
            }
            vision_table.write_dict(data)
        else:
            print "Frame is null (this probably means the camera hasn't started capturing yet."
            time.sleep(1)


def get_offsets(topleft_x, bb_width, resolution):
    middle = topleft_x + (bb_width / 2)
    pixel_offset = middle - resolution[0] / 2
    angle_offset = pixel_offset * (23.0 / (resolution[0] / 2))
    ret = {
        "pixel_offset": pixel_offset,
        "angle_offset": angle_offset,
    }
    return ret