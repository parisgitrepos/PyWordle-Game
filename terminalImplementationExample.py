from PyWordle import PyWordle

LIGHT_GREY = '\033[97m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
END_COLOR = '\033[00m'


running = True

while running:
    num_guesses = int(input('Welcome to PyWordle! How many guesses would you like to have: '))
    guess = 1
    print('')
    game = PyWordle(num_guesses)
    invalid_guess = True

    while guess <= num_guesses and not game.check_game_over()['condition']:

        while invalid_guess:
            guess_str = input("Make a guess: ")
            print('')
            result = game.make_guess(guess_str)

            if result['condition'] is True:
                invalid_guess = False
            else:
                print("Invalid guess - " + result['error'])
                print('')

        invalid_guess = True

        board = result['board']
        color_mapping = result['color_board']

        board_formatted = ''

        for row_index in range(len(board)):
            for char_index in range(len(board[row_index])):
                char = board[row_index][char_index]
                color = color_mapping[row_index][char_index]
                if char != ' ':
                    if color == 'LG':
                        color_code = LIGHT_GREY
                    elif color == 'G':
                        color_code = GREEN
                    else:
                        color_code = YELLOW

                    board_formatted += color_code+char+END_COLOR+'   '

                else:
                    board_formatted += '[]   '

            board_formatted += '\n'
        print(board_formatted)

        if game.check_game_over()['condition']:
            info = game.get_info()
            win = info['guessed_word']
            guesses_taken = info['guesses_taken']
            actual_word = info['actual_word']

            print('Game over!')
            print('Win Status: ' + str(win))
            print('Number of Guesses Taken: ' + str(guesses_taken))
            print('Actual Word: ' + str(actual_word))

    replay = input('Would you like to play again? (y/n) ')
    if replay.lower() == 'n':
        running = False
