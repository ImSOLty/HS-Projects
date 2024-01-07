from string import ascii_lowercase
import math

table = [ascii_lowercase[i:] + ascii_lowercase[:i] for i in range(26)]


def key_vigenere(message, key_length, encoded_message):
    res = ''
    for i in range(key_length):
        res += ascii_lowercase[table[ascii_lowercase.find(message[i])].find(encoded_message[i])]
    return res


def decode_vigenere(encoded, key):
    key = (math.ceil(len(encoded) / len(key)) * key)[:len(encoded)]
    decoded = ''
    for i in range(len(encoded)):
        decoded += ascii_lowercase[table[ascii_lowercase.find(key[i])].find(encoded[i])]
    return decoded


length = int(input())
helper = input().split(' ')
encoded_helper = input().split(' ')
text_encoded = input().split(' ')

print(decode_vigenere(text_encoded, key_vigenere(helper, length, encoded_helper)).replace('x', ' '))
