import random
import string

words = ['python', 'java', 'kotlin', 'javascript']
guess = random.choice(words)
displayed_word = '-' * len(guess)
tries = 8
tried_letters = set()


def reveal(letter):
    global displayed_word
    for i in range(len(guess)):
        if guess[i] == letter:
            displayed_word = displayed_word[:i] + letter + displayed_word[i + 1:]


def has_win():
    return True if guess == displayed_word else False


def main():
    global tries
    global tried_letters
    print('H A N G M A N')
    while tries > 0:
        print()
        print(displayed_word)
        letter = input('Input a letter: ')
        if letter in tried_letters:
            print('You already typed this letter')
        elif len(letter) != 1:
            print('You should print a single letter')
        elif letter not in string.ascii_lowercase:
            print('It is not an ASCII lowercase letter')
        else:
            tried_letters.add(letter)
            if letter in guess:
                reveal(letter)
                if has_win():
                    print(f'You guessed the word {guess}')
                    print('You survived!')
                    break
            else:
                print('No such letter in the word')
                tries -= 1
    else:
        print('You are hanged!')


if __name__ == '__main__':
    main()
