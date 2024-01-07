import os

from QueueThread import QueueThread

print("Welcome to the traffic management system!\n" +
      "Input the number of roads: ", end='')

a = input()
while not a.isdigit() or a == "0":
    print("Error! Incorrect Input. Try again: ", end='')
    a = input()
a = int(a)

print("Input the interval: ", end='')
b = input()
while not b.isdigit() or b == "0":
    print("Error! Incorrect Input. Try again: ", end='')
    b = input()
b = int(b)

thread = QueueThread(a, b, "QueueThread")
thread.start()

os.system('cls' if os.name == 'nt' else 'clear')

while True:
    print("Menu:\n" +
          "1. Add road\n" +
          "2. Delete road\n" +
          "3. Open system\n" +
          "0. Quit")
    ch = input()
    if ch == "1":
        print("Input road name: ", end='')
        name = input()
        print(thread.enqueue(name))
    elif ch == "2":
        print(thread.dequeue())
    elif ch == "3":
        thread.printing = True
    elif ch == "0":
        thread.exit = True
        print("Bye!")
        break
    else:
        print("Incorrect option")
    input()
    thread.printing = False
    os.system('cls' if os.name == 'nt' else 'clear')
