import requests
from bs4 import BeautifulSoup
from argparse import ArgumentParser


class IncorrectInputException(Exception):
    def __init__(self, message="Oops..."):
        self.message = message
        super().__init__(self.message)


link_translate = 'https://context.reverso.net/translation/{0}-{1}/{2}'

full = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese',
        'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish', 'All']

WELCOME_MSG = 'Hello, welcome to the translator. Translator supports:\n' + \
              '\n'.join([f'{i + 1}. {lang}' for i, lang in enumerate(full)]) + \
              '\nType the number of your language: '


def word_translation(content):
    soup = BeautifulSoup(content, 'html.parser')
    terms = soup.find_all('span', {'class': 'display-term'})
    return [t.text for t in terms]


def examples_usage(content):
    soup = BeautifulSoup(content, 'html.parser')
    usages = soup.find_all('div', {'class': 'example'})
    return [[t.text.strip() for t in usage.find_all('span', {'class': 'text'})] for usage in usages]


def call(lang_from: int, lang_to: int, word: str):
    try:
        res = requests.get(
            link_translate.format(full[lang_from].lower(), full[lang_to].lower(), word),
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        if res.status_code != 200:
            raise IncorrectInputException(f"Sorry, unable to find {word}")
    except IncorrectInputException as e:
        raise IncorrectInputException(e.message)
    except BaseException:
        raise IncorrectInputException(f"Something wrong with your internet connection")
    if 'not found in Context' in res.text:
        raise IncorrectInputException(f"Sorry, unable to find {word}")
    return res


def format_response(res, lang):
    return f'{full[lang]} Translations:\n' + '\n'.join(word_translation(res.content)) + \
        f'\n\n{full[lang]} Examples:\n' + '\n'.join([f'{s[0]}\n{s[1]}\n' for s in examples_usage(res.content)])


def determine_language(lang):
    try:
        return full.index(lang.capitalize())
    except ValueError:
        raise IncorrectInputException(f"Sorry, the program doesn't support {lang}")


def main(args):
    # int(input(WELCOME_MSG)) - 1
    # int(input('Type the number of language you want to translate to: ')) - 1
    # input('Type the word you want to translate: ')
    lang_from = determine_language(args[0])
    lang_to = determine_language(args[1])
    word = args[2]
    if lang_to != 13:
        res = call(lang_from, lang_to, word)
        output = format_response(res, lang_to)
    else:
        output = ""
        for i in range(len(full)):
            res = call(lang_from, i, word)
            output += f'{format_response(res, i)}\n'
    print(output)
    with open(f'{word}.txt', 'w', encoding='utf-8') as out:
        out.write(output)


if __name__ == '__main__':
    parser = ArgumentParser()
    try:
        main(parser.parse_known_args()[1])
    except IncorrectInputException as e:
        print(e.message)
