import json
import os
import string
from typing import List

MENU = """***Welcome to the Journey to Mount Qaf*** 

1. Start a new game (START)
2. Load your progress (LOAD)
3. Quit the game (QUIT)"""

CREATION = """Good luck on your journey, {username}!
Your character: {name}, {species}, {gender}
Your inventory: {snack}, {weapon}, {tool}
Difficulty: {difficulty}
Number of lives: {lives}
---------------------------"""

HELP = """Type the number of the option you want to choose.
Commands you can use:
/i => Shows inventory.
/q => Exits the game.
/c => Shows the character traits.
/h => Shows help.
/s => Save the game."""
INVENTORY = """Inventory: {inventory}"""
CHARACTER = """Your character: {name}, {species}, {gender}.
Lives remaining: {lives}"""


def input_exact(correct: List, output=''):
    inp = input(output).lower()
    while inp not in correct:
        print("Unknown input! Please enter a valid one.")
        inp = input().lower()
    return inp


class Player:
    def __init__(self, username, data):
        self.username = username
        self.data = data

    @classmethod
    def load(cls, username):
        with open(f'data/saves/{username}.json', 'r') as outfile:
            data = json.load(outfile)
            return cls(username, data)

    @classmethod
    def create_character(cls, username):
        print('Create your character:')
        char = []
        for i in ['name', 'species', 'gender', 'snack', 'weapon', 'tool']:
            char.append(input(f'\t{string.capwords(i)}:'))
        difficulty = input_exact(['1', '2', '3', 'easy', 'medium', 'hard'],
                                 'Choose your difficulty: \n\t1. Easy\n\t2. Medium\n\t3. Hard\n\t')
        difficulty = 'easy' if difficulty in ['1', 'easy'] else 'medium' if difficulty in ['2', 'medium'] else 'hard'
        lives = 5 if difficulty == 'easy' else 3 if difficulty == 'medium' else 1
        return cls(username, {
            "character": {"name": char[0], "species": char[1], "gender": char[2]},
            "inventory": {"snack_name": char[3], "weapon_name": char[4], "tool_name": char[5], "content": char[3:6]},
            "progress": {"level": f'level1', "scene": 'scene1'},
            "lives": lives,
            "difficulty": difficulty
        })

    def create_story(self):
        with (open('./data/story.json', 'r') as file):
            f = file.read().replace('{tool}', self.data['inventory']['tool_name']). \
                replace('{weapon}', self.data['inventory']['weapon_name']). \
                replace('{snack}', self.data['inventory']['snack_name'])
            return json.loads(f)

    def save(self):
        with open(f'data/saves/{self.username}.json', 'w') as outfile:
            outfile.write(json.dumps(self.data))
        print('Game saved!')

    def show_inventory(self):
        print(INVENTORY.format(inventory=', '.join(self.data['inventory']['content'])))

    def show_character(self):
        print(CHARACTER.format(name=self.data['character']['name'], species=self.data['character']['species'],
                               gender=self.data['character']['gender'], lives=self.data['lives']))

    def __str__(self):
        return CREATION.format(username=self.username, name=self.data['character']['name'],
                               species=self.data['character']['species'], gender=self.data['character']['gender'],
                               snack=self.data['inventory']['snack_name'], weapon=self.data['inventory']['weapon_name'],
                               tool=self.data['inventory']['tool_name'], difficulty=self.data['difficulty'],
                               lives=self.data['lives'])


def game_process(data, player):
    dead = False
    c = False
    while True:
        cur_scene = data[player.data['progress']['level']]['scenes'][player.data['progress']['scene']]
        if not c:
            print(cur_scene['text'])
            for i in range(1, len(cur_scene['options']) + 1):
                print(f'{i}. {cur_scene["options"][i - 1]["option_text"]}')
        print()
        ch = input_exact(['/h', '/c', '/q', '/i', '/s'] + [str(i) for i in range(1, len(cur_scene['options']) + 1)])
        c = True
        match ch:
            case '/h':
                print(HELP)
            case '/c':
                player.show_character()
            case '/i':
                player.show_inventory()
            case '/s':
                player.save()
            case '/q':
                print('Thanks for playing!')
                exit()
            case _:
                print()
                c = False
                opt = cur_scene["options"][int(ch) - 1]
                print(opt['result_text'])
                for action in opt['actions']:
                    if action.startswith('+'):
                        player.data['inventory']['content'].append(action[1:])
                        print(f"------ Item added: {action[1:]} ------")
                    if action.startswith('-'):
                        player.data['inventory']['content'].remove(action[1:])
                        print(f"------ Item removed: {action[1:]} ------")
                    if action == 'hit':
                        player.data['lives'] -= 1
                        if player.data['lives'] == 0:
                            print('------ You died ------')
                            dead = True
                        else:
                            print(f"------ Lives remaining: {player.data['lives']} ------")
                    if action == 'heal':
                        player.data['lives'] += 1
                        print(f"------ Lives remaining: {player.data['lives']} ------")
                player.data['progress']['scene'] = 'scene1' if dead else opt['next']
                if player.data['progress']['scene'] == 'end':
                    player.data['progress']['level'] = 'level' + str(int(player.data['progress']['level'][-1]) + 1)
                    print(f"\n------ Level {player.data['progress']['level'][-1]} ------")
                    player.data['progress']['scene'] = 'scene1'


def main():
    while True:
        print(MENU)
        option = input_exact(['1', '2', '3', 'start', 'load', 'quit'])
        if option in ['1', 'start']:
            username = input("Starting a new game...\nEnter a username ('/b' to go back): ")
            if username.lower() == '/b':
                continue
            player = Player.create_character(username)
            print(player)
            game_process(player.create_story(), player)
        elif option in ['2', 'load']:
            print('No save data found!')
            # print('Choose username (/b - back):\n')
            # files = [f.replace('.json', '') for f in os.listdir('./data/saves')]
            # print('\n'.join(files) + '\n')
            # ch = input_exact(files + ['/b'])
            # if ch.lower() == '/b':
            #     continue
            # player = Player.load(ch)
            # print(f"Loading your progress...\n\n------ Level {player.data['progress']['level'][-1]} ------")
            # game_process(player.create_story(), player)
        else:
            print("Goodbye!")
            break


if __name__ == '__main__':
    main()
