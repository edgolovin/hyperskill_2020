import random
from collections import deque

rps = deque(['rock', 'paper', 'scissors'])
user_name = ''
user_rating = 0


def check_who_won(u, c):
    global user_rating
    rotation = (len(rps) // 2) - rps.index(u)
    rps.rotate(rotation)
    if rps.index(u) < rps.index(c):
        print(f'Sorry, but computer chose {c}')
    elif rps.index(u) > rps.index(c):
        print(f'Well done. Computer chose {c} and failed')
        user_rating += 100


def identify_user():
    global user_name
    user_name = input('Enter your name: ')
    print(f'Hello, {user_name}')


def load_saved_ratings():
    global user_rating
    try:
        with open('rating.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if user_name in line:
                    user_rating = int(line.split()[1])
    except FileNotFoundError:
        pass


def play_game():
    global user_rating
    while True:
        user_input = input()
        comp_choice = random.choice(rps)
        if user_input == '!exit':
            print('Bye!')
            break
        elif user_input == '!rating':
            print(f'Your rating: {user_rating}')
        elif user_input == comp_choice:
            print(f'There is a draw ({user_input})')
            user_rating += 50
        elif user_input not in rps:
            print('Invalid input')
        else:
            check_who_won(user_input, comp_choice)


def main():
    global rps
    identify_user()
    load_saved_ratings()
    user_rps = input()
    if user_rps:
        rps = deque(user_rps.split(','))
    print("Okay, let's start")
    play_game()


if __name__ == '__main__':
    main()
