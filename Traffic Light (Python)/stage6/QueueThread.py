import os
import threading
import time


class QueueThread(threading.Thread):

    def __init__(self, max_roads: int, interval: int, name: str):
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

        self.current = -1
        self.cur_int = -1

    def run(self):
        while not self.exit:
            if self.printing:
                os.system('cls' if os.name == 'nt' else 'clear')

                message = ""
                message += f"! {self.from_start}s. have passed since system startup !\n"
                message += f"! Number of roads: {self.roads} !\n"
                message += f"! Interval: {self.interval} !\n"

                if self.front != -1:
                    if self.rear >= self.front:
                        for i in range(self.front, self.rear + 1):
                            message += self.print_road(i)
                    else:
                        for i in range(self.front, self.roads):
                            message += self.print_road(i)
                        for i in range(0, self.rear + 1):
                            message += self.print_road(i)

                message += f"! Press \"Enter\" to open menu !"
                print(message)
            time.sleep(1)
            if self.current != -1:
                self.cur_int -= 1
                if self.cur_int == 0:
                    self.cur_int = self.interval
                    self.current = self.front if self.current == self.rear else (self.current + 1) % self.roads
            self.from_start += 1

    def enqueue(self, name: str):
        if (self.rear + 1) % self.roads == self.front:
            return "Queue is full"
        if self.front == -1:
            self.front = 0
            self.rear = 0
            self.current = self.front
            self.cur_int = self.interval + 1
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

    def calculate_time(self, from_pos: int, to_pos: int, s: int):
        result = (to_pos - from_pos) % self.roads
        result += self.roads if result < 0 else 0
        if to_pos < from_pos:
            act_size = self.rear - self.front if self.rear > self.front else self.roads - self.front + self.rear
            act_size += 1
            result -= (self.roads - act_size)
        result = result * self.interval - (self.interval - s)
        return result

    def print_road(self, i: int):
        ret = ""
        ret += self.road_array[i] + " is "
        if i == self.current:
            ret += '\033[32m' + "open for " + str(self.cur_int)
        else:
            ret += '\033[31m' + "closed for " + str(self.calculate_time(self.current, i, self.cur_int))
        ret += 's.\033[0m\n'
        return ret
