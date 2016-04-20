import time

class FpsTracker(object):
    def __init__(self):
        self.total_frames = 0

    def start(self):
        self._start_time = time.time()

    def update(self):
        self.total_frames += 1

    def get(self):
        return self.total_frames / (time.time() - self._start_time)
