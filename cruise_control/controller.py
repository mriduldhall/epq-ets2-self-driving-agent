from time import sleep
from pyautogui import hold


class Controller:
    def __init__(self):
        pass

    def control(self, command):
        while True:
            current_command = command.get_command()
            if current_command == "N":
                sleep(0.2)
            elif current_command == "A":
                with hold("w"):
                    sleep(0.2)
