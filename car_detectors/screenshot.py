import cv2
import numpy as np
from pyautogui import screenshot


class Screenshot:
    def __init__(self, fov_x_start=500, fov_y_start=300, fov_x_length=400, fov_y_length=225, speed_limit_x_start=23, speed_limit_y_start=782, speed_limit_x_length=33, speed_limit_y_length=33):
        self.field_of_view_region = (fov_x_start, fov_y_start, fov_x_length, fov_y_length)
        self.speed_limit_region = (speed_limit_x_start, speed_limit_y_start, speed_limit_x_length, speed_limit_y_length)

    def take_field_of_view_screenshot(self):
        image = screenshot(region=self.field_of_view_region)
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    def take_speed_limit_screenshot(self):
        image = screenshot(region=self.speed_limit_region)
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
