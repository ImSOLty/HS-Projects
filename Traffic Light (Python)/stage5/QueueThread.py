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

        self.rear = -1
        self.front = -1
        self.road_array = ["" for _ in range(max_roads)]

    def run(self):
        while not self.exit:
            if self.printing:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"! {self.from_start}s. have passed since system startup !")
                print(f"! Number of roads: {self.roads} !")
                print(f"! Interval: {self.interval} !\n")

                if self.front != -1:
                    if self.rear >= self.front:
                        for i in range(self.front, self.rear + 1):
                            print(self.road_array[i])
                    else:
                        for i in range(self.front, self.roads):
                            print(self.road_array[i])
                        for i in range(self.rear+1):
                            print(self.road_array[i])

                print(f"\n! Press \"Enter\" to open menu !")
            time.sleep(1)
            self.from_start += 1

    def enqueue(self, name: str):
        if (self.rear + 1) % self.roads == self.front:
            return "Queue is full"
        if self.front == -1:
            self.front = 0
            self.rear = 0
        else:
            self.rear = (self.rear + 1) % self.roads

        self.road_array[self.rear] = name
        return name + " Added!"

    def dequeue(self):
        if self.front == -1:
            return "Queue is empty"
        ret = self.road_array[self.front] + " deleted!"
        if self.front == self.rear:
            self.front = -1
            self.rear = -1
        else:
            self.front = (self.front + 1) % self.roads
        return ret
