import random

print("How many pencils would you like to use:")
inp = input()
while (not inp.isnumeric()) or (int(inp) < 1):
    print("Error! Provided amount of pencils should be numeric and positive")
    inp = input()
pencils = int(inp)

turn = ""
while True:
    print("Who will be the first (John, Jack):")
    turn = input()
    if not (turn == "John" or turn == "Jack"):
        print("Error! Choose between 'John' and 'Jack'")
    else:
        break

while pencils > 0:
    if turn == "John":
        k = ""
        while True:
            print('|' * pencils)
            print("John's turn!")
            k = input()
            if k.isnumeric() and 0 < int(k) < 4:
                if int(k) <= pencils:
                    break
                else:
                    print("Error! Too much pencils were taken")
            else:
                print("Error! Possible values: '1', '2' or '3'")
        pencils -= int(k)
        turn = "Jack"
    else:
        print('|' * pencils)
        print("Jack's turn:")
        bottake = (pencils - 1) % 4
        if bottake == 0:
            if pencils == 1:
                bottake = 1
            else:
                bottake = random.randint(1, 3)
        print(bottake)
        pencils -= bottake
        turn = "John"

if turn == "Jack":
    print("Jack won!")
else:
    print("John won!")
