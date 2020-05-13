__author__ = 'Evgeniy Golovin {edgolovin@yandex.ru}'
"""
Tic Tac Toe game

    play_field is a string of length 9: '_________'
    play_field is being printed like:
    0 1 2
    3 4 5
    6 7 8
    user input is a tuple of two integers: (1, 1)
    coordinates match cells from above like:
    {(1, 3): 0, (2, 3): 1, (3, 3): 2,
     (1, 2): 3, (2, 2): 4, (3, 2): 5,
     (1, 1): 6, (2, 1): 7, (3, 1): 8}
"""
import logging

# GLOBAL variables
play_field = '_________'
current_user = 'X'
coord_matcher = dict()
game_over = False

# making dictionary to match user input to the play_field

str_coord = [i for i in range(9)]
field_coord = []
for y in range(3, 0, -1):
    for x in range(1, 4):
        field_coord.append((x, y))
for i in range(9):
    coord_matcher[field_coord[i]] = str_coord[i]


def show_ttt_line(line: str):
    print(f'| {line[0]} {line[1]} {line[2]} |')


def show_ttt(ui: str):
    print('-' * 9)
    show_ttt_line(ui[:3])
    show_ttt_line(ui[3:6])
    show_ttt_line(ui[6:])
    print('-' * 9)


def who_won(ui) -> (bool, bool):
    logger = logging.getLogger('FUNC:who_won')
    x_won = False
    o_won = False
    line_0 = ui[:3]
    line_1 = ui[3:6]
    line_2 = ui[6:]
    row_0 = ui[0] + ui[3] + ui[6]
    row_1 = ui[1] + ui[4] + ui[7]
    row_2 = ui[2] + ui[5] + ui[8]
    diag_08 = ui[0] + ui[4] + ui[8]
    diag_62 = ui[6] + ui[4] + ui[2]
    win_lines = [line_0, line_1, line_2,
                 row_0, row_1, row_2,
                 diag_08, diag_62]
    logger.debug(f'win_lines {win_lines}')
    for wn in win_lines:
        if wn.count('X') == 3:
            x_won = True
        if wn.count('O') == 3:
            o_won = True
    logger.debug(f'result being returned is {x_won, o_won}')
    return x_won, o_won


def check_game_status(ui: str):
    global game_over
    logger = logging.getLogger('FUNC:check_game_state')
    x_won, o_won = who_won(ui)
    logger.debug(f'X won: {x_won}')
    logger.debug(f'O won: {o_won}')
    if abs(ui.count('X') - ui.count('O')) > 1 or x_won and o_won:
        print('Impossible')
        game_over = True
    elif x_won:
        print('X wins')
        game_over = True
    elif o_won:
        print('O wins')
        game_over = True
    elif ui.count('X') + ui.count('O') == 9:
        print('Draw')
        game_over = True
    else:
        print('Game not finished')


def switch_user():
    global current_user
    if current_user == 'X':
        current_user = 'O'
    else:
        current_user = 'X'


def start_game():
    global play_field
    global coord_matcher
    global current_user
    logger = logging.getLogger('FUNC:user_move')
    while True:
        try:
            x_y = tuple(map(int, input('Enter the coordinates: ').split()))
            try:
                cell = play_field[coord_matcher[x_y]]
                logger.debug(f' Coordinates as a tuple: {x_y} | as a play_field character: {cell}')
                logger.debug(f' Coordinates matching dictionary: {coord_matcher}')
                if cell != '_':
                    print('This cell is occupied! Choose another one!')
                else:
                    play_field = play_field[:coord_matcher[x_y]] + current_user + play_field[coord_matcher[x_y] + 1:]
                    show_ttt(play_field)
                    check_game_status(play_field)
                    if game_over:
                        break
                    else:
                        switch_user()
            except KeyError:
                print('Coordinates should be from 1 to 3!')
        except ValueError:
            print('You should enter numbers!')


def main():
    logging.basicConfig(level=logging.DEBUG)
    global play_field
    show_ttt(play_field)
    start_game()


if __name__ == '__main__':
    main()
