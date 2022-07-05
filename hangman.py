import time
from random_word import RandomWords
import os
from termios import tcflush, TCIOFLUSH
import sys
import rich

loading_list = ['_', '_', '_', '🛒', '_', '_', '_']
result = []
wrong_letters = set()
level = ('DEBUG', 'PROD')[1]


def insert_to_result_if_in_word(letter, hang_man_word):
    is_inserted = False
    index = hang_man_word.find(letter)
    while index != -1:
        result[index] = letter
        is_inserted = True
        index = word.find(letter, index + 1)
    return is_inserted


def get_random_word():
    index = 0
    first_cycle = True
    while index < 7:
        if not first_cycle:
            word_ = RandomWords().get_random_word()
            if word_:
                return word_
        os.system('clear')
        print(f'getting word {"".join(loading_list)}')
        buf = loading_list.pop(0)
        loading_list.append(buf)
        index += 1
        if index == 7:
            index = 0
            first_cycle = False
        time.sleep(0.5)


def if_letter(letter, hang_man_word, tries_):
    if insert_to_result_if_in_word(letter, hang_man_word):
        print('Letter in a word')
        if '_' not in result:
            print(f'Correct word is: {hang_man_word}')
            print('YOU WON!')
            exit(0)
    else:
        print('Letter not in word')
        if letter not in wrong_letters:
            tries_ -= 1
        wrong_letters.add(letter)
    return tries_


def if_word(input_word, hang_man_word, tries_):
    if input_word == hang_man_word:
        print(f'Correct word is: {hang_man_word}')
        print('YOU WON!')
        exit(0)
    else:
        print('try once more')
        tries_ -= 1
    return tries_


HANGMAN_PICS = ['''
     +---+
     O   |
    /|\  |
    /    |
        ===''', '''
     +---+
     O   |
    /|\  |
         |
        ===''', '''
     +---+
     O   |
    /|   |
         |
        ===''', '''
     +---+
     O   |
     |   |
         |
        ===''', '''
     +---+
     O   |
         |
         |
        ===''', '''
     +---+
         |
         |
         |
        ===''', '''
     +---+
     O   |
    /|\  |
    / \  |
        ===''']


def game():
    tries = 7
    while tries > 0:
        status = f'result_word: {" ".join(result)}\nwrong_letters: {" ".join(wrong_letters)}'
        if level == 'DEBUG':
            status += f'\nword: {word}'
        print(status)
        input_ = input('Enter a letter: ').lower()
        if input_ == 'exit':
            break
        os.system('clear')
        if len(input_) == 1:
            tries = if_letter(input_, word, tries)
        elif len(input_) == len(word):
            tries = if_word(input_, word, tries)
        else:
            print('Try again!')
            tries -= 1
        print(f'tries left {tries}')
        if tries < 7:
            print(HANGMAN_PICS[tries - 1], )
        if tries == 0:
            print(f'Correct word is: {word}')
            print("YOU LOSE")


if __name__ == '__main__':
    word = get_random_word().lower()
    result = ['_' if letter.isalpha() else letter for letter in word]

    while True:
        tcflush(sys.stdin, TCIOFLUSH)
        game()
        restart = input("you want play again y/n: ").lower()
        if restart == 'y':
            os.system('clear')
            wrong_letters.clear()
            word = get_random_word().lower()
            result = ['_' if letter.isalpha() else letter for letter in word]
            tcflush(sys.stdin, TCIOFLUSH)
            game()
        else:
            print("BB")
            break
