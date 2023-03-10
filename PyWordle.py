import linecache
import random
from bs4 import BeautifulSoup
import requests


class PyWordle:

    def __init__(self, max_guesses = 5, num_letters = 5) -> None:
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
            self.game_board.append([' ' for i in range(self.num_letters)])
            self.color_board.append([' ' for i in range(self.num_letters)])

        for i in range(num_letters):
            self.win_state.append('G')

    def _is_valid_guess(self, guess: str) -> dict:
        dictionary_url = 'https://wordreference.com/definition/' + guess # Checks word against wordreference.com dictionary
        dictionary_call = requests.get(dictionary_url)
        dictionary_call = BeautifulSoup(dictionary_call.text, 'html.parser')
        dictionary_call = dictionary_call.find_all(id = 'noEntryFound') # Looks for marker 'noEntryFound' signifying invalid word

        if self.num_guesses >= self.max_guesses:
            return {'condition': False, 'error': "Max guesses made"}
        elif len(guess) != self.num_letters:
            return {'condition': False, 'error': "Invalid number of characters"}
        elif len(dictionary_call) > 0:
            return {'condition': False, 'error': f'"{guess}" is not a valid word'}
        else:
            return {'condition': True}

    def _update_game_board(self, guess: str) -> None:
        # Need to reset empty row (i.e. [' ', ' ', ' ', ' ', ' ']) to [] in order to prevent appending to end of former
        self.game_board[self.num_guesses - 1] = []
        self.color_board[self.num_guesses - 1] = []

        for char in guess:
            self.game_board[self.num_guesses-1].append(char)

        for char_index in range(len(guess)):
            if guess[char_index] == self.word[char_index]:
                self.color_board[self.num_guesses-1].append('G') # Green
            elif guess[char_index] in self.word:
                self.color_board[self.num_guesses-1].append('Y') # Yellow
            else:
                self.color_board[self.num_guesses-1].append('LG') # Light grey

    def make_guess(self, guess) -> dict:
        guess = guess.upper()
        is_valid = self._is_valid_guess(guess)

        if not is_valid['condition']:
            return is_valid
        else:
            self.num_guesses += 1
            self._update_game_board(guess)
            return {'condition': True, 'board': self.game_board, 'color_board': self.color_board}

    def check_game_over(self) -> dict:
        if self.color_board[self.num_guesses-1] == self.win_state:
            return {'condition': True}
        elif self.num_guesses >= self.max_guesses:
            return {'condition': True}
        else:
            return {'condition': False}

    def get_info(self) -> dict:
        if self.color_board[self.num_guesses-1] == self.win_state:
            win = True
        else:
            win = False

        return {'guessed_word': win, 'guesses_taken': self.num_guesses, 'actual_word': self.word}
