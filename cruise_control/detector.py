from time import time, sleep
from car_detectors.screenshot import Screenshot
from speed_detectors.detection import Detector as SpeedDetector


class Detector:
    def __init__(self):
        self.speed_detector = SpeedDetector()
        self.screenshot = Screenshot()

    def engage(self, command):
        while True:
            start_time = time()
            speed_limit = self.speed_detector.detect_speed_limit()
            speed = self.speed_detector.detect_speed_opencv()
            if int(speed) <= speed_limit:
                command.set_command("A")
            else:
                command.set_command("N")
            end_time = time()
            wait_time = 1 - (end_time - start_time)
            if wait_time > 0:
                sleep(wait_time)
