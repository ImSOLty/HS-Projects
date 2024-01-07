print("Welcome to the traffic management system!\n" +
      "Input the number of roads:")
a = int(input())
print("Input the interval:")
b = int(input())
while True:
    print("Menu:\n" +
          "1. Add road\n" +
          "2. Delete road\n" +
          "3. Open system\n" +
          "0. Quit")
    ch = int(input())
    if ch == 1:
        print("Road added!")
    elif ch == 2:
        print("Road deleted!")
    elif ch == 3:
        print("System")
    elif ch == 0:
        print("Bye!")
        break
