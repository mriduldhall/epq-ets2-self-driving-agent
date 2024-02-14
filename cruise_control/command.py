from threading import Lock


class Command:
    def __init__(self):
        self.command = "N"
        self.detector_lock = Lock()
        self.controller_lock = Lock()
        self.detector_lock.acquire()

    def set_command(self, command):
        self.controller_lock.acquire()
        self.command = command
        self.detector_lock.release()

    def get_command(self):
        self.detector_lock.acquire()
        command = self.command
        self.controller_lock.release()
        return command
