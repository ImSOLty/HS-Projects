import os.path
import random


def parse_options(opts):
    opts2 = opts + opts
    result = dict()
    for i in range(len(opts)):
        for j in range(-(len(opts) // 2), (len(opts) // 2) + 1):
            result[(opts2[i], opts2[i + j])] = 0 if j == 0 else 1 if j < 0 else -1
    return result


name = input('Enter your name:')
score = 0
print(f'Hello, {name}')
if os.path.exists('rating.txt'):
    with open('rating.txt') as f:
        for l in f.readlines():
            player_name, player_score = l.split(' ')
            if player_name == name:
                score = int(player_score.strip())

custom = input()
if custom == '':
    options = ['paper', 'scissors', 'rock']
else:
    options = custom.split(',')
d = parse_options(options)

print('Okay, let\'s start')

while True:
    ch = input()
    if ch == '!exit':
        break
    if ch == '!rating':
        print(f'Your rating: {score}')
        continue
    if ch not in options:
        print('Invalid input')
        continue
    ch_bot = random.choice(options)
    match d[(ch, ch_bot)]:
        case 0:
            print(f'There is a draw ({ch_bot})')
            score += 50
        case -1:
            print(f'Sorry, but the computer chose {ch_bot}')
        case 1:
            print(f'Well done. The computer chose {ch_bot} and failed')
            score += 100
print('Bye!')
