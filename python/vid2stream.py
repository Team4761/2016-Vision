import io
import time
import picamera

with picamera.PiCamera() as camera:
	stream = io.BytesIO()
	count = 0
	start_time = time.time()
	for foo in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
		stream.truncate()
		stream.seek(0)
		print(time.time() - start_time)
		count += 1
		if count == 10:
			break