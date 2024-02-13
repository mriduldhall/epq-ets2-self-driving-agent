import cv2
import numpy as np
from car_detectors.screenshot import Screenshot


class Detector:
    def __init__(self):
        self.screenshot = Screenshot()

    @staticmethod
    def check_similarity(image_one, image_two):
        return image_one.shape == image_two.shape and not (np.bitwise_xor(image_one, image_two).any())

    def detect_speed_limit(self):
        image = self.screenshot.take_speed_limit_screenshot()
        if self.check_similarity(image, cv2.imread('speed_limits/60.png')):
            return 60
        if self.check_similarity(image, cv2.imread('speed_limits/50.png')):
            return 50
        if self.check_similarity(image, cv2.imread('speed_limits/30.png')):
            return 30
