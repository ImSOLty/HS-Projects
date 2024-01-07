# Write your code here
import random

stock = [[i, j] for i in range(7) for j in range(i, 7)]
player_hand = []
bot_hand = []
snake = []
status = ''


def print_play_field():
    print(f'''======================================================================
Stock size: {len(stock)}
Computer pieces: {len(bot_hand)}

{''.join([str(p) for p in (snake if len(snake) < 6 else snake[:3] + ['...'] + snake[len(snake) - 3:])])}

Your pieces:''')
    for i in range(len(player_hand)):
        print(f'{i + 1}:{player_hand[i]}')
    if status:
        print("Status: It's your turn to make a move. Enter your command.")
    else:
        print("Status: Computer is about to make a move. Press Enter to continue...")


while len(snake) == 0:
    for i in range(14):
        elem = random.choice(stock)
        stock.remove(elem)
        if i % 2 == 0:
            player_hand.append(elem)
        else:
            bot_hand.append(elem)
    status = True
    for i in range(6, -1, -1):
        if [i, i] in bot_hand + player_hand:
            if [i, i] in player_hand:
                player_hand.remove([i, i])
                status = not status
            else:
                bot_hand.remove([i, i])
            snake.append([i, i])
            break
times = 0
while True:
    print_play_field()
    if len(bot_hand) == 0 or len(player_hand) == 0 or times == 8:
        if times == 8:
            print('Status: The game is over. It\'s a draw!')
        else:
            print(f"Status: The game is over. {'You won!' if not status else 'The computer won!'}")
        break
    ch = input()
    while True:
        if status:
            if ch is None:
                ch = input()
            while ch not in [str(i) for i in range(-(len(player_hand) + 1), len(player_hand) + 1)]:
                ch = input('Invalid input. Please try again.\n')
            if ch == '0':
                if len(stock) > 0:
                    player_hand.append(stock.pop())
                item = None
                break
            else:
                if ch.startswith('-') and snake[0][0] in player_hand[abs(int(ch)) - 1] or \
                        not ch.startswith('-') and snake[-1][-1] in player_hand[int(ch) - 1]:
                    item = player_hand.pop(abs(int(ch)) - 1)
                    break
                else:
                    ch = input('Illegal move. Please try again.\n')
        else:
            ch = random.randint(0, len(bot_hand))
            if ch == 0:
                if len(stock) > 0:
                    bot_hand.append(stock.pop())
                item = None
                break
            else:
                if snake[0][0] in bot_hand[int(ch) - 1] or snake[-1][-1] in bot_hand[int(ch) - 1]:
                    item = bot_hand.pop(int(ch) - 1)
                    break

    if item is not None:
        if snake[-1][-1] in item:
            snake.insert(len(snake), item if snake[-1][-1] == item[0] else item[::-1])
        elif snake[0][0] in item:
            snake.insert(0, item if snake[0][0] == item[-1] else item[::-1])
        times = 0
    else:
        times += 1
    status = not status
