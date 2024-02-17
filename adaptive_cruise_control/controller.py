from time import sleep
from pyautogui import hold, press


class Controller:
    def __init__(self):
        self.differential = 0
        self.differential_up = ";"
        self.differential_down = "'"
        self.accelerate = "w"

    def apply_differential(self, differential):
        increments = int(differential) - self.differential
        if increments > 0:
            press(self.differential_up, presses=increments, interval=0.05)
        elif increments < 0:
            press(self.differential_down, presses=-increments, interval=0.05)
        self.differential = int(differential)

    def control(self, command):
        press(self.differential_down, presses=4, interval=0.05)
        current_command = command.get_command()
        while True:
            if current_command == "N":
                sleep(0.2)
                current_command = command.get_command()
            elif current_command == "A":
                with hold(self.accelerate):
                    while current_command == "A":
                        sleep(0.2)
                        current_command = command.get_command()
            elif current_command in ("1", "2", "3", "4"):
                self.apply_differential(current_command)
                sleep(0.2)
                current_command = command.get_command()
                if current_command not in ("1", "2", "3", "4"):
                    self.apply_differential(0)
