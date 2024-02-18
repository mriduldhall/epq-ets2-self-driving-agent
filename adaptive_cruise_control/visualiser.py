import cv2
from time import time, sleep
from car_detectors.screenshot import Screenshot
from lane_detection.detection import Detector as LaneDetector
from car_detectors.yolo.detector import Detector as CarDetector
from speed_detectors.detection import Detector as SpeedDetector


class Visualiser:
    def __init__(self):
        self.screenshot = Screenshot()
        self.car_detector = CarDetector()
        self.lane_detector = LaneDetector()
        self.speed_detector = SpeedDetector()
        self.text_colour = (0, 0, 0)

    def create_full_visualisation(self, video_name, duration=300):
        counter = 0
        writer = None
        total_time = 0
        while counter < duration:
            start_time = time()
            field_of_view = self.screenshot.take_field_of_view_screenshot()
            speed_limit = self.speed_detector.detect_speed_limit()
            speed = self.speed_detector.detect_speed_opencv()
            detected_cars = self.car_detector.detect(field_of_view)
            detected_lanes = self.lane_detector.detect(field_of_view)
            visualisation_image = self.car_detector.visualiser(field_of_view, detected_cars)
            visualisation_image = self.lane_detector.visualiser(visualisation_image, detected_lanes)
            cv2.putText(visualisation_image, f"Speed: {speed} m/h", (10, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, self.text_colour, 1)
            cv2.putText(visualisation_image, f"Speed limit: {speed_limit} m/h", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, self.text_colour, 1)
            if writer is None:
                fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                writer = cv2.VideoWriter(video_name, fourcc, 30, (field_of_view.shape[1], field_of_view.shape[0]), True)
            writer.write(visualisation_image)
            counter += 1
            end_time = time()
            total_time += end_time - start_time
            wait_time = 1 - (end_time - start_time)
            print(f"Time taken: {end_time - start_time}")
            if wait_time > 0:
                sleep(wait_time)
        writer.release()
        print("Average time taken: ", total_time / duration)


if __name__ == '__main__':
    name = "visualisation-5.avi"
    visualiser = Visualiser()
    visualiser.create_full_visualisation("visualisation-1.avi")
