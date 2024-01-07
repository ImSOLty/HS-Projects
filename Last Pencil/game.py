import random

print("How many pencils would you like to use:")

k = input()

while not k.isnumeric() or int(k) == 0:
    if not k.isnumeric():
        print("The number of pencils should be numeric")
    else:
        print("The number of pencils should be positive")
    k = input()

k = int(k)
print("Who will be the first (John, Jack):")
cur = input()
while cur != "John" and cur != "Jack":
    print("Choose between 'John' and 'Jack'")
    cur = input()
while k > 0:
    print(k * '|')
    print(f"{cur} turn!")

    if(cur=='John'):
        take = input()
        while take != '1' and take != '2' and take != '3' or int(take) > k:
            if take != '1' and take != '2' and take != '3':
                print("Possible values: '1', '2' or '3'")
            else:
                print("Too many pencils were taken")
            take = input()
    else:
        take = (k - 1) % 4
        if take == 0:
            if k == 1:
                take = 1
            else:
                take = random.randint(1, 3)
        print(take)
    k -= int(take)
    if cur == "John":
        cur = "Jack"
    else:
        cur = "John"
print(f"{cur} won!")
