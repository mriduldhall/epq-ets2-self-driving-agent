import cv2
import numpy as np
from pyautogui import screenshot


class Screenshot:
    def __init__(self, fov_x_start=500, fov_y_start=300, fov_x_length=400, fov_y_length=225):
        self.field_of_view_region = (fov_x_start, fov_y_start, fov_x_length, fov_y_length)

    def take_field_of_view_screenshot(self):
        image = screenshot(region=self.field_of_view_region)
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
