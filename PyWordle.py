import linecache
import random

class PyWordle:
    def __init__(self, max_guesses = 5, num_letters = 5):
        self.max_guesses = max_guesses
        self.num_letters = num_letters
        self.num_guesses = 0
        self.game_board = []
        self.color_board = []
        self.win_state = []

        word_count = 0
        with open("5LetterWords.txt", "r") as file:
            for i in file:
                word_count += 1
            random_num = random.randrange(1, word_count+1)
            self.word = linecache.getline("5LetterWords.txt", random_num).upper()

        for i in range(max_guesses):
            self.game_board.append([' ', ' ', ' ', ' ', ' '])
            self.color_board.append([' ', ' ', ' ', ' ', ' '])

        for i in range(num_letters):
            self.win_state.append('G')

    def _is_valid_guess(self, guess: str):
        if self.num_guesses >= self.max_guesses:
            return [False, "Max guesses made"]
        elif len(guess) != self.num_letters:
            return [False, "Invalid number of characters"]
        else:
            return [True]

    def _update_game_board(self, guess: str):
        # Need to reset empty row (i.e. [' ', ' ', ' ', ' ', ' ']) to [] in order to prevent appending to end of former
        self.game_board[self.num_guesses - 1] = []
        self.color_board[self.num_guesses - 1] = []

        for char in guess:
            self.game_board[self.num_guesses-1].append(char)

        for char_index in range(len(guess)):
            if guess[char_index] == self.word[char_index]:
                self.color_board[self.num_guesses-1].append('G')
            elif guess[char_index] in self.word:
                self.color_board[self.num_guesses-1].append('Y')
            else:
                self.color_board[self.num_guesses-1].append('B')

    def make_guess(self, guess):
        guess = guess.upper()
        is_valid = self._is_valid_guess(guess)

        if not is_valid[0]:
            return is_valid
        else:
            self.num_guesses += 1
            self._update_game_board(guess)
            return [True, self.game_board, self.color_board]

    def check_game_over(self):
        if self.color_board[self.num_guesses-1] == self.win_state:
            return True
        elif self.num_guesses >= self.max_guesses:
            return True
        else:
            return False

    def get_info(self):
        if self.color_board[self.num_guesses-1] == self.win_state:
            win = True
        else:
            win = False

        return {'guessed_word': win, 'guesses_taken': self.num_guesses, 'actual_word': self.word}
