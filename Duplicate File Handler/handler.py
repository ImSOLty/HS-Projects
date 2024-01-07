import hashlib
import os
import sys


def walk(form: str, reverse: bool):
    d = dict()
    for root, dirs, files in os.walk(os.getcwd() + '\\' + sys.argv[1]):
        for name in files:
            path = os.path.join(root, name)
            if name.endswith(form) or len(form) == 0:
                size = os.path.getsize(path)
                with open(path, 'rb') as out:
                    d.setdefault(size, {}).setdefault(hashlib.md5(out.read()).hexdigest(), []).append(path)
    for size in sorted(d.keys(), reverse=reverse):
        print(f'{size} bytes')
        for h in d[size].keys():
            print('\n'.join(d[size][h]))
    return d


def check_duplicates(d: dict, reverse: bool):
    arr_paths = []
    i = 0
    for size in sorted(d.keys(), reverse=reverse):
        print(f'{size} bytes')
        for h in d[size].keys():
            if len(d[size][h]) > 1:
                print(f'Hash: {h}')
                for path in d[size][h]:
                    arr_paths.append((size, path))
                    print(f'{i + 1}. {path}')
                    i += 1
    return arr_paths


def delete_files(paths: list):
    ch = input('Enter file numbers to delete:')
    while True:
        try:
            if ch == '' or not all([1 <= int(n) <= len(paths) for n in ch.split()]):
                ch = input('Wrong format. Enter file numbers to delete:')
            else:
                break
        except ValueError:
            ch = input('Wrong format. Enter file numbers to delete:')
    freed = 0
    for n in ch.split():
        freed += paths[int(n) - 1][0]
        os.remove(paths[int(n) - 1][1])
    print(f'Total freed up space: {freed} bytes')


def main():
    if len(sys.argv) < 2:
        print('Directory is not specified')
    else:
        form = input('Enter file format: ')
        print('Size sorting options:\n1. Descending\n2. Ascending')
        ch = input('Enter a sorting option: ')
        while ch not in ['1', '2']:
            ch = input('Wrong option. Enter a sorting option:')
        d = walk(form, ch == '1')

        ch2 = input('Check for duplicates?')
        while ch2 not in ['yes', 'no']:
            ch2 = input('Wrong option. Try again:')
        if ch2 == 'yes':
            paths = check_duplicates(d, ch == '1')
            ch3 = input('Delete files?')
            while ch3 not in ['yes', 'no']:
                ch3 = input('Wrong option. Try again:')
            if ch3 == 'yes':
                delete_files(paths)


if __name__ == '__main__':
    main()
