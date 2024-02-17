from time import time, sleep
from yolo.detector import Detector
from screenshot import Screenshot


if __name__ == '__main__':
    detector = Detector()
    screenshot = Screenshot()
    wait_time = 0
    while True:
        overall_start_time = time()
        start_time = time()
        image = detector.detect(screenshot.take_field_of_view_screenshot())
        end_time = time()
        wait_time = 1 - (end_time - start_time)
        if wait_time > 0:
            sleep(wait_time)
        overall_end_time = time()
        print(f"Frame time: {overall_end_time - overall_start_time}")
