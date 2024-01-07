def input_exact(s, feedback, func):
    ret = input(s)
    while not func(ret.lower()):
        print(feedback)
        ret = input(s)
    return ret


HELP = '''Available formatters: plain bold italic header link inline-code ordered-list unordered-list new-line
Special commands: !help !done'''


def plain():
    return input("Text: ")


def bold():
    return f'**{input("Text: ")}**'


def italic():
    return f'*{input("Text: ")}*'


def inline_code():
    return f'`{input("Text: ")}`'


def link():
    return f'[{input("Label:")}]({input("URL: ")})'


def header():
    level = input_exact('Level: ', 'The level should be within the range of 1 to 6', lambda x: 0 < int(x) < 7)
    s = input('Text')
    return f'{int(level) * "#"} {s}\n'


def new_line():
    return '\n'


def md_list(t):
    r = int(input_exact('Number of rows: ', 'The number of rows should be greater than zero', lambda x: int(x) > 0))
    return '\n'.join([(f'{i}. ' if t == 'ordered-list' else '*') + input(f'Row #{i}:') for i in range(1, r + 1)]) + '\n'


formatters = {'plain': plain,
              'bold': bold,
              'italic': italic,
              'header': header,
              'link': link,
              'inline-code': inline_code,
              'ordered-list': md_list,
              'unordered-list': md_list,
              'new-line': new_line}
commands = ['!help', '!done']

result = ''
while True:
    print(result)
    cmd = input_exact('Choose a formatter: ', 'Unknown formatting type or command',
                      lambda x: x in list(formatters.keys()) + commands)
    match cmd:
        case '!help':
            print(HELP)
        case '!done':
            with open('output.md', 'w') as outfile:
                outfile.write(result)
            break
        case _:
            result += formatters[cmd]() if 'list' not in cmd else formatters[cmd](cmd)
