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

    def use_regular_cruise_control(self, speed, speed_limit):
        difference = speed - speed_limit
        if self.previous_vehicle_distance is not None and self.previous_vehicle_distance < self.minimum_distance:
            return "4"
        elif speed <= speed_limit:
            return "A"
        elif difference > 10:
            return "4"
        elif difference > 6:
            return "3"
        elif difference > 3:
            return "2"
        elif difference >= 2:
            return "1"
        return "N"

    def use_adaptive_cruise_control(self, relative_speed):
        if self.previous_vehicle_distance < self.minimum_distance:
            return "E"
        elif self.previous_vehicle_distance < 50 and 30 > relative_speed > 2.5:
            return "E"
        elif self.previous_vehicle_distance < 75 and 30 > relative_speed > 5:
            return "4"
        return "N"

    def engage(self, command):
        while True:
            start_time = time()
            field_of_view = self.screenshot.take_field_of_view_screenshot()
            detected_vehicles = self.vehicle_detector.detect(field_of_view)
            detected_lane_image = self.lane_detector.detect(field_of_view)
            applicable_vehicle = self.find_applicable_vehicle(detected_vehicles, detected_lane_image)
            relative_speed = self.calculate_relative_speed(applicable_vehicle)
            self.update_previous_distances(applicable_vehicle)
            if relative_speed is None or relative_speed < 0:
                speed_limit = self.speed_detector.detect_speed_limit()
                speed = self.speed_detector.detect_speed_opencv()
                command.set_command(self.use_regular_cruise_control(speed, speed_limit))
            else:
                command.set_command(self.use_adaptive_cruise_control(relative_speed))
            end_time = time()
            time_taken = end_time - start_time
            wait_time = 1 - time_taken
            if wait_time > 0:
                sleep(wait_time)
