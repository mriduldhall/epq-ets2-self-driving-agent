from time import sleep
from pyautogui import hold, press


class Controller:
    def __init__(self):
        self.differential = 0

    def control(self, command):
        press("'", presses=4, interval=0.05)
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
