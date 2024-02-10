from time import time, sleep
from yolo.detection import Detection
from screenshot import Screenshot


if __name__ == '__main__':
    detection = Detection()
    screenshot = Screenshot()
    wait_time = 0
    while True:
        overall_start_time = time()
        start_time = time()
        image = detection.detect(screenshot.take_screenshot())
        end_time = time()
        wait_time = 1 - (end_time - start_time)
        if wait_time > 0:
            sleep(wait_time)
        overall_end_time = time()
        print(f"Frame time: {overall_end_time - overall_start_time}")
