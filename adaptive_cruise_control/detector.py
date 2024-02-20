from time import time, sleep
from car_detectors.screenshot import Screenshot
from lane_detection.detection import Detector as LaneDetector
from speed_detectors.detection import Detector as SpeedDetector
from car_detectors.yolo.detector import Detector as VehicleDetector


class Detector:
    def __init__(self):
        self.speed_detector = SpeedDetector()
        self.vehicle_detector = VehicleDetector()
        self.lane_detector = LaneDetector()
        self.screenshot = Screenshot()
        self.previous_vehicle_distance = None
        self.second_previous_vehicle_distance = None
        self.minimum_distance = 25

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

    def calculate_relative_speed(self, vehicle, time_difference=1):
        if len(vehicle) == 0:
            return None
        vehicle = vehicle[0]
        if self.previous_vehicle_distance is None and self.second_previous_vehicle_distance is None:
            return None
        if self.previous_vehicle_distance is None:
            distance_change = self.second_previous_vehicle_distance - float(vehicle[1])
            return distance_change / (2 * time_difference)
        distance_change = self.previous_vehicle_distance - float(vehicle[1])
        return distance_change / time_difference

    def update_previous_distances(self, vehicle):
        if len(vehicle) == 0:
            distance = None
        else:
            distance = float(vehicle[0][1])
        self.second_previous_vehicle_distance = self.previous_vehicle_distance
        self.previous_vehicle_distance = distance

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
