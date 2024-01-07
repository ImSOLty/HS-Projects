import os
import threading
import time


class QueueThread(threading.Thread):

    def __init__(self, interval: int, max_roads: int, name: str):
        super().__init__()
        self.setName(name)
        self.interval = interval
        self.roads = max_roads
        self.from_start = 0
        self.printing = False
        self.exit = False

    def run(self):
        while not self.exit:
            if self.printing:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"! {self.from_start}s. have passed since system startup !")
                print(f"! Number of roads: {self.roads} !")
                print(f"! Interval: {self.interval} !")
                print(f"! Press \"Enter\" to open menu !")
            time.sleep(1)
            self.from_start += 1
