import cv2
import numpy as np
from pyautogui import screenshot


class Screenshot:
    def __init__(self, region=(500, 300, 400, 225)):
        self.region = region

    def take_screenshot(self):
        image = screenshot(region=self.region)
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
