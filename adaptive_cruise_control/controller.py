from time import sleep
from pyautogui import hold, press


class Controller:
    def __init__(self):
        self.differential = 0
        self.differential_up = ";"
        self.differential_down = "'"
        self.accelerate = "w"
        self.engine_brake = "b"
        self.air_brake = "s"
        self.sleep_time = 0.5

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
                sleep(self.sleep_time)
                current_command = command.get_command()
            elif current_command == "A":
                with hold(self.accelerate):
                    while current_command == "A":
                        sleep(self.sleep_time)
                        current_command = command.get_command()
            elif current_command in ("1", "2", "3", "4"):
                self.apply_differential(current_command)
                sleep(self.sleep_time)
                current_command = command.get_command()
                if current_command not in ("1", "2", "3", "4"):
                    self.apply_differential(0)
            elif current_command == "E":
                with hold(self.engine_brake):
                    self.apply_differential("4")
                    while current_command == "E":
                        sleep(self.sleep_time)
                        current_command = command.get_command()
                    self.apply_differential(0)
            elif current_command == "B":
                with hold(self.air_brake):
                    with hold(self.engine_brake):
                        self.apply_differential("4")
                        while current_command == "B":
                            sleep(self.sleep_time)
                            current_command = command.get_command()
                        self.apply_differential(0)
