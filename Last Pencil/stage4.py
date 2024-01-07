print("How many pencils would you like to use:")
inp = input()
while (not inp.isnumeric()) or (int(inp) < 1):
    if not inp.isnumeric():
        print("Amount of pencils should be numeric")
    else:
        print("Amount of pencils should be positive")
    inp = input()
pencils = int(inp)

turn = ""
print("Who will be the first (John, Jack):")
while True:
    turn = input()
    if not (turn == "John" or turn == "Jack"):
        print("Choose between 'John' and 'Jack'")
    else:
        break

while pencils > 0:
    k = ""
    print('|' * pencils)
    print(turn + "'s turn!")
    while True:
        k = input()
        if k.isnumeric() and 0 < int(k) < 4:
            if int(k) <= pencils:
                break
            else:
                print("Too many pencils were taken")
        else:
            print("Possible values: '1', '2' or '3'")
    if turn == "John":
        turn = "Jack"
    elif turn == "Jack":
        turn = "John"
    pencils -= int(k)

if turn == "Jack":
    print("Jack won!")
else:
    print("John won!")
