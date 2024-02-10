import cv2
import numpy as np
from time import time
from pyautogui import screenshot


if __name__ == '__main__':
    start_time = time()
    image = screenshot(region=(0, 0, 300, 400))
    end_time = time()
    print(f"Screenshot took {end_time - start_time} seconds.")
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cv2.imshow('screenshot', image)
    cv2.waitKey(0)
