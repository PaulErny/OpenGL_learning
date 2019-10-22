import cProfile
from guppy import hpy


class CheckOpti:
    def __init__(self):
        self.memory = hpy()
        self.exec_time = cProfile.Profile()

    def start(self):
        self.exec_time.enable()

    def end(self):
        self.exec_time.disable()
        print(self.memory.heap())
        self.exec_time.print_stats()
