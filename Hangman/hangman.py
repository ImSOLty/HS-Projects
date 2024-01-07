import random
from string import ascii_lowercase

print(f'H A N G M A N')
won, lost = 0, 0
while True:
    cmd = ''
    while cmd not in ['play', 'results', 'exit']:
        cmd = input('Type "play" to play the game, "results" to show the scoreboard, and "exit" to quit: ')
    match cmd:
        case "play":
            word = random.choice(['python', 'java', 'swift', 'javascript'])
            attempts = 8
            guesses = set()
            finish = False
            for i in range(attempts):
                if finish:
                    break
                while True:
                    print('\n' + ''.join([l if l in guesses else '-' for l in word]))
                    if all(l in guesses for l in set(word)):
                        print(f'You guessed the word {word}!\nYou survived!')
                        won += 1
                        finish = True
                        break
                    guess = input('Input a letter: ')
                    if len(guess) != 1:
                        print('Please, input a single letter.')
                        continue
                    if guess not in ascii_lowercase:
                        print('Please, enter a lowercase letter from the English alphabet.')
                        continue
                    if guess in guesses:
                        print('You\'ve already guessed this letter.')
                        continue
                    guesses.add(guess)
                    if guess not in set(word):
                        print('That letter doesn\'t appear in the word.')
                        break
            if not finish:
                print('You lost!')
                lost += 1
        case "results":
            print(f'You won: {won} times\nYou lost: {lost} times')
        case "exit":
            break
