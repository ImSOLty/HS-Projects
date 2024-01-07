import random
import re


def input_exact(msg, func):
    ret = input(msg)
    while not func(ret):
        ret = input('Incorrect format.\n')
    return ret


level = int(input_exact('''Which level do you want? Enter a number:
1 - simple operations with numbers 2-9
2 - integral squares of 11-29
''', lambda t: t in ['1', '2']))

mark = 0
for i in range(5):
    if level == 1:
        x, op, y = random.randint(2, 9), random.choice(['+', '-', '*']), random.randint(2, 9)
        expr = f'{x} {op} {y}'
        res = int(input_exact(f'{expr}\n', lambda t: re.match(r'^-?\d+$', t))) == eval(expr)
    else:
        x = random.randint(11, 29)
        expr = f'{x}**2'
        res = int(input_exact(f'{x}\n', lambda t: t.isnumeric())) == eval(expr)
    print('Right!' if res else 'Wrong!')
    mark += 1 if res else 0
if input(f'Your mark is {mark}/5. Would you like to save the result? Enter yes or no.').lower() in ['yes', 'y']:
    with open('results.txt', 'a') as outfile:
        outfile.write(f'{input("What is your name?")}: {mark}/5 in level {level} '
                      f'({"simple operations with numbers 2-9" if level==1 else "integral squares of 11-29"})')
        print('The results are saved in "results.txt".')
