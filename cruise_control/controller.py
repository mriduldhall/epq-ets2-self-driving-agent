from time import sleep
from pyautogui import hold


class Controller:
    def __init__(self):
        pass

    def control(self, command):
        current_command = command.get_command()
        while True:
            if current_command == "N":
                sleep(0.2)
                current_command = command.get_command()
            elif current_command == "A":
                with hold("w"):
                    while current_command == "A":
                        sleep(0.2)
                        current_command = command.get_command()
