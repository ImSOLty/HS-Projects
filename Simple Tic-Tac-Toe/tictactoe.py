def print_field(field):
    print(f"{'-' * 9}\n" + '\n'.join(['| ' + " ".join(row).replace('_', ' ') + ' |' for row in field]) + f"\n{'-' * 9}")


def check_win(player, field):
    for i in range(3):
        won = [0] * 4
        for j in range(3):
            won[0] += 1 if field[i][j] == player else 0
            won[1] += 1 if field[j][i] == player else 0
            won[2] += 1 if field[j][j] == player else 0
            won[3] += 1 if field[2 - j][j] == player else 0
        if any([w == 3 for w in won]):
            return True


def check_finish(field):
    return '_' not in str(field)


def input_coos(field):
    ret = None
    while ret is None:
        try:
            coos = [int(x) - 1 for x in input().split()]
        except:
            print('You should enter numbers!')
            continue
        if 0 <= coos[0] < 3 and 0 <= coos[1] < 3:
            if field[coos[0]][coos[1]] != '_':
                print('This cell is occupied! Choose another one!')
            else:
                ret = (coos[0], coos[1])
        else:
            print('Coordinates should be from 1 to 3!')
    return ret


game = [['_'] * 3 for i in range(3)]
next = 'X'
print_field(game)
while not (check_win('X', game) or check_win('O', game) or check_finish(game)):
    x, y = input_coos(game)
    game[x][y] = next
    print_field(game)
    next = 'X' if next == 'O' else 'O'
if check_win('X', game):
    print('X wins')
elif check_win('O', game):
    print('O wins')
elif check_finish(game):
    print('Draw')
