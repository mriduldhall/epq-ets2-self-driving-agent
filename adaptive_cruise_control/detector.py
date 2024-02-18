from time import time, sleep
from car_detectors.screenshot import Screenshot
from speed_detectors.detection import Detector as SpeedDetector


class Detector:
    def __init__(self):
        self.speed_detector = SpeedDetector()
        self.screenshot = Screenshot()

    @staticmethod
    def find_applicable_vehicle(detected_vehicles, detected_lane_image):
        applicable_vehicles = []
        closest_vehicle = []
        for vehicle in detected_vehicles:
            y_position = vehicle[0][1] + vehicle[0][3]
            if y_position >= len(detected_lane_image):
                y_position = len(detected_lane_image) - 1
            x_position = vehicle[0][0] + (vehicle[0][2] / 2)
            column = detected_lane_image[y_position]
            left_lane = None
            right_lane = None
            pixel = 0
            while pixel < len(column) and left_lane is None:
                if column[pixel].any():
                    left_lane = pixel
                pixel += 1
            pixel = len(column) - 1
            while pixel >= 0 and right_lane is None:
                if column[pixel].any():
                    right_lane = pixel
                pixel -= 1
            if left_lane is not None and right_lane is not None and left_lane <= x_position <= right_lane:
                applicable_vehicles.append(vehicle)
                if len(closest_vehicle) == 0 or vehicle[1] < closest_vehicle[0][1]:
                    closest_vehicle = [vehicle]
        return closest_vehicle

    def engage(self, command):
        while True:
            start_time = time()
            speed_limit = self.speed_detector.detect_speed_limit()
            speed = self.speed_detector.detect_speed_opencv()
            difference = speed - speed_limit
            if speed <= speed_limit:
                command.set_command("A")
            elif difference > 10:
                command.set_command("4")
            elif difference > 6:
                command.set_command("3")
            elif difference > 3:
                command.set_command("2")
            elif difference >= 2:
                command.set_command("1")
            else:
                command.set_command("N")
            end_time = time()
            wait_time = 1 - (end_time - start_time)
            if wait_time > 0:
                sleep(wait_time)
