import argparse
import json
import re
import string

import additional
from additional import log
from brute_force import brute_force
from kmp import KMP, calculate_lps
from boyer_moore import boyer_moore, bad_character_table, good_suffix_table
from rabin_karp import rabin_karp, hash_table
from aho_corasick import aho_corasick, aho_create_statemachine

DIVIDER = "=" * 58


def preprocessing(alg, words):
    log("Preprocessing:")
    if alg == 'brute-force':
        log("Not needed")
        return None
    elif alg == 'knuth-morris-pratt':
        return calculate_lps(words[0])
    elif alg == 'boyer-moore':
        return [bad_character_table(words[0]), good_suffix_table(words[0])]
    elif alg == 'rabin-karp':
        return hash_table(words)
    elif alg == 'aho-corasick':
        return aho_create_statemachine(words)
    else:
        if words[0] == '*' * len(words[0]):
            return None
        matches = [(m.group(0), (m.start(), m.end() - 1)) for m in re.finditer(r'[^\*]+', words[0])]
        word, indices = zip(*matches)
        # log("Substrings and indices without wildcards:")
        for i in range(len(word)):
            log(f'\t{word[i]}({indices[i][0]})')
        return aho_create_statemachine(list(word), [i[0] for i in indices])


def main(args):
    with open(args.file) as f:
        chat_list = [line.strip().lower() for line in f]
    words = [args.word]
    if args.multiple:
        with open(args.word) as f:
            words = [line.strip().lower() for line in f]
    result = []
    log(f"Started \"{args.algorithm}\" algorithm")

    log(DIVIDER)

    helper = preprocessing(args.algorithm, words)
    log(DIVIDER)

    for msg_id in range(len(chat_list)):
        log(f"Line: \"{chat_list[msg_id]}\"")
        in_msg = []
        if args.algorithm == "brute-force":
            in_msg = brute_force(words[0], chat_list[msg_id])
        elif args.algorithm == "knuth-morris-pratt":
            in_msg = KMP(words[0], chat_list[msg_id], helper)
        elif args.algorithm == "boyer-moore":
            in_msg = boyer_moore(words[0], chat_list[msg_id], helper)
        elif args.algorithm == "rabin-karp":
            in_msg = rabin_karp(words, chat_list[msg_id], helper)
        elif args.algorithm == "aho-corasick":
            in_msg = aho_corasick(chat_list[msg_id], helper)
        elif args.algorithm == "aho-corasick-wildcard":
            in_msg = aho_corasick(chat_list[msg_id], helper, args.word)
        if len(in_msg) != 0:
            result.append([msg_id, in_msg])

    log(DIVIDER)
    if len(result) == 0:
        log("No inappropriate content detected")
    else:
        for i in result:
            for j in i[1]:
                chat_list[i[0]] = chat_list[i[0]][:j[1]] + "*" * len(j[0]) + chat_list[i[0]][j[1] + len(j[0]):]
        print("\n".join(chat_list))


def calc_hash(s):
    hash_value = 0
    for char in s:
        hash_value = (hash_value * 256 + ord(char)) % 101
    return hash_value


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--algorithm", type=str,
                        choices=['brute-force', 'knuth-morris-pratt', 'boyer-moore', 'rabin-karp', 'aho-corasick',
                                 'aho-corasick-wildcard'],
                        help="String-searching algorithm", required=True)
    parser.add_argument("-w", "--word", type=str, help="Inappropriate content", required=True)
    parser.add_argument("-f", "--file", type=str, help="Text file that should be processed", required=True)
    parser.add_argument("-l", "--logging", action='store_true', help="Enable logging")
    parser.add_argument("-m", "--multiple", action='store_true',
                        help="Multiple words from a file provided with --word argument")
    arguments = parser.parse_args()

    if arguments.multiple and (arguments.algorithm not in ['rabin-karp', 'aho-corasick']):
        parser.error("--multiple requires rabin-karp or aho-corasick algorithm usage.")

    additional.logging = arguments.logging
    main(arguments)
    # data = json.loads(
    #     '''[{"pattern": "gcagagaga", "gst": [9, 9, 9, 9, 2, 9, 4, 9, 6, 1]}, {"pattern": "ababab", "gst": [2, 2, 2, 4, 4, 6, 1]}, {"pattern": "abcde", "gst": [5, 5, 5, 5, 5, 1]}, {"pattern": "aaaaa", "gst": [1, 1, 2, 3, 4, 5]}, {"pattern": "xyzxyzxyz", "gst": [3, 3, 3, 3, 6, 6, 6, 9, 9, 1]}, {"pattern": "abcabc", "gst": [3, 3, 3, 3, 6, 6, 1]}, {"pattern": "aaaaaa", "gst": [1, 1, 2, 3, 4, 5, 6]}, {"pattern": "abcd", "gst": [4, 4, 4, 4, 1]}, {"pattern": "abcdefg", "gst": [7, 7, 7, 7, 7, 7, 7, 1]}, {"pattern": "ab", "gst": [2, 2, 1]}, {"pattern": "abcdefgh", "gst": [8, 8, 8, 8, 8, 8, 8, 8, 1]}, {"pattern": "abcdeabcde", "gst": [5, 5, 5, 5, 5, 5, 10, 10, 10, 10, 1]}, {"pattern": "ababa", "gst": [2, 2, 2, 4, 4, 1]}, {"pattern": "abccba", "gst": [5, 5, 5, 5, 5, 5, 1]}, {"pattern": "abc", "gst": [3, 3, 3, 1]}, {"pattern": "abccde", "gst": [6, 6, 6, 6, 6, 6, 1]}, {"pattern": "abcdabcd", "gst": [4, 4, 4, 4, 4, 8, 8, 8, 1]}, {"pattern": "abcdeabc", "gst": [5, 5, 5, 5, 5, 5, 8, 8, 1]}, {"pattern": "abcdeabcdef", "gst": [11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 1]}, {"pattern": "aaaa", "gst": [1, 1, 2, 3, 4]}, {"pattern": "abcabcabc", "gst": [3, 3, 3, 3, 6, 6, 6, 9, 9, 1]}, {"pattern": "abcdefghi", "gst": [9, 9, 9, 9, 9, 9, 9, 9, 9, 1]}, {"pattern": "abcdeabcdeabcde", "gst": [5, 5, 5, 5, 5, 5, 10, 10, 10, 10, 10, 15, 15, 15, 15, 1]}, {"pattern": "abcabcabcabcabc", "gst": [3, 3, 3, 3, 6, 6, 6, 9, 9, 9, 12, 12, 12, 15, 15, 1]}, {"pattern": "abababa", "gst": [2, 2, 2, 4, 4, 6, 6, 1]}, {"pattern": "aabcaabc", "gst": [4, 4, 4, 4, 4, 8, 8, 8, 1]}, {"pattern": "ababc", "gst": [5, 5, 5, 5, 5, 1]}, {"pattern": "aabaabaab", "gst": [3, 3, 3, 3, 6, 6, 6, 9, 9, 1]}, {"pattern": "abababab", "gst": [2, 2, 2, 4, 4, 6, 6, 8, 1]}, {"pattern": "abcdef", "gst": [6, 6, 6, 6, 6, 6, 1]}, {"pattern": "aabbcc", "gst": [6, 6, 6, 6, 6, 1, 2]}, {"pattern": "abacaba", "gst": [4, 4, 4, 4, 4, 6, 2, 1]}]''')
    # for d in data:
    #     print(d['pattern'], good_suffix_table(d['pattern']), d['gst'])
    #     # if good_suffix_table(d['pattern']) != d['gst']:
    #     #     print(d['pattern'], good_suffix_table(d['pattern']), d['gst'])
    #     # else:
    #     #     print('Correct')
