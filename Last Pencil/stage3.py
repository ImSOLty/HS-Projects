print("How many pencils would you like to use:")
pencils = int(input())

print("Who will be the first (John, Jack):")
turn = input()

while pencils > 0:
    print('|'*pencils)
    print(turn+"'s turn:")
    k = int(input())
    pencils -= k
    if turn == "John":
        turn = "Jack"
    elif turn == "Jack":
        turn = "John"
