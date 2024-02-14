from command import Command
from detector import Detector
from controller import Controller
from concurrent.futures import ThreadPoolExecutor


if __name__ == '__main__':
    command = Command()
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(Detector().engage, command)
        executor.submit(Controller().control, command)
