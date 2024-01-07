import random

n = int(input("Enter the number of friends joining (including you):\n"))

if n <= 0:
    print("No one is joining for the party")
else:
    d = {}
    print("Enter the name of every friend (including you), each on a new line:")
    for i in range(n):
        name = input()
        d[name] = 0
    amount = int(input('Enter the total bill value:\n'))
    lucky = ''
    if input('Do you want to use the "Who is lucky?" feature? Write Yes/No:\n').lower() == 'yes':
        lucky = random.choice(list(d.keys()))
        print(f'{lucky} is the lucky one!')
    else:
        print('No one is going to be lucky')
    for i in d.keys():
        if not i.lower() == lucky.lower():
            d[i] = round(amount / (len(d.keys()) - (1 if lucky != '' else 0)) * 100) / 100
    print(f'\n{d}')
