import picamera
import picamera.array
import cv2
import imutils
import time
import threading

lock = threading.Lock()
frame = None
resolution = (640, 480)
stream = cv2.VideoCapture(0)


def get_frame():
    ret = None
    lock.acquire()
    ret = frame
    lock.release()
    return ret


def capture_images():
    """
    print "Staring capture thread"
    global frame
    while True:
        print "Attempting capture"
        (grabbed, f) = stream.read()
        if grabbed:
            print "Captured"
            lock.acquire()
            frame = imutils.resize(f, width=resolution[0], height=resolution[1])
            lock.release()
    """
    print "started capturing thread"
    global frame
    with picamera.PiCamera() as camera:
        camera.resolution = resolution
        camera.shutter_speed = 100
        time.sleep(0.5) # Shutter speed is not set instantly. This wait allows time for changes to take effect.
        print "Initialized camera..."
        with picamera.array.PiRGBArray(camera) as stream:
            for foo in camera.capture_continuous(stream, format="bgr", use_video_port=True):
                print "Captured an image"
                stream.seek(0)
                stream.truncate()
                lock.acquire()
                frame = stream.array
                lock.release()
                print "Converted image data to array"
