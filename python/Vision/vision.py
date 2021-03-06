import threading

from lib.camera import capture_images
from lib.processing import process_frames


def start_threads():
    processing_thread = threading.Thread(target=process_frames)
    processing_thread.daemon = True
    processing_thread.start()

if __name__ == "__main__":
    start_threads()
    capture_images()
