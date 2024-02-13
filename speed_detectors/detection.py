import cv2
import numpy as np
import pytesseract
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

    def detect_speed_tesseract(self):
        img = self.screenshot.take_speed_screenshot()
        return pytesseract.image_to_string(img, lang='eng', config='--psm 6 -c tessedit_char_whitelist=0123456789')

    @staticmethod
    def pre_process_image(image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        image = cv2.bitwise_not(image)
        return image

    @staticmethod
    def speed_in_double_digits(image):
        first_column = image[:, 0]
        last_column = image[:, -1]
        if len(set(first_column)) == 1 and np.all(first_column[0] == 0) and len(set(last_column)) == 1 and np.all(last_column[0] == 0):
            return False
        return True

    def detect_speed_opencv(self, current_speed_image):
        # current_speed_image = self.screenshot.take_speed_screenshot()
        current_speed_image = self.pre_process_image(current_speed_image)
        self.speed_in_double_digits(current_speed_image)
