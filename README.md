# PyWordle

This project is an implementation of the popular Wordle game. It has been split up into two components, 1) the PyWordle
class, and 2) the PyWordle Web API. 

---

## PyWordle Class
The PyWordle class is a backend implemented in Python to allow developers to create front-end apps based off the Wordle
game. Documentation for the backend are as follows...<br><br>

### PyWordle(max_guesses:str = 5, num_letters:int = 5)
Creates a new PyWordle object.<br>
```game = PyWordle()```<br>
PLEASE NOTE THE _num_letters_ parameter is still a WIP and IS NOT FULLY FUNCTIONAL.

### .make_guess(guess: str)
Make a guess in a PyWordle game instance. Takes only one parameter, guess, of type str representing guess to be made. 
Return type dict.
* Dictionary returned contains following keys
  * '_condition_' -> ```True``` if guess was successfully made, ```False``` if game did not make guess (bool)
  * _'error'_ -> If condition is ```False```, then an explanation of why the guess could not be made is returned (str)
  * '_board_' -> If condition is ```True```, then an updated board list, structure detailed [here](#board-list-structure)
                is returned
  * '_color_board_' -> If condition is```True```, then an updated color board list, structure detailed [here](#color-board-list-structure)
                      is returned
* Example return value when condition is ```True``` 
<br>```{'board': [['H', 'E', 'L', 'L', 'O'], [' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ']], 'color_board': [['LG', 'LG', 'LG', 'LG', 'Y'], [' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ']], 'condition': True}```
* Example return value when condition is ```False``` <br>
```{'condition': False, 'error': "Invalid number of characters"}```

### .get_info()
After an instance is created, you can view details of the game at any point by running ```game.get_info()```. Return type dict.
* Dictionary returned contains following keys
  * _'actual_word'_ -> Answer to the game (str)
  * _'guessed_word'_ -> Boolean with value ```True``` if user guessed the word and ```False``` otherwise (bool)
  * _'guesses_taken'_ -> Number of guesses user has taken (int)
* Example return value <br> ```{'actual_word': 'FOURS', 'guessed_word': False, 'guesses_taken': 2}```

### .check_game_over()
A function which returns either ```True``` if game is over or ```False``` otherwise.

### Board List Structure
PyWordle provides a game board in the form of an array containing one row (list) for every guess, with each row having a 
length corresponding to the number of letters in a PyWordle game. If a guess has not been made yet, the guess row will 
be filled with empty strings for each letter. <br>

Example board with maximum of 5 guesses, word of 5 letters, and only 1 guess has been taken<br>
[<br>
&nbsp; &nbsp; &nbsp; ['H', 'E', 'L', 'L', 'O'], <br>
&nbsp; &nbsp; &nbsp; [' ', ' ', ' ', ' ', ' '], <br>
&nbsp; &nbsp; &nbsp; [' ', ' ', ' ', ' ', ' '], <br>
&nbsp; &nbsp; &nbsp; [' ', ' ', ' ', ' ', ' '], <br>
&nbsp; &nbsp; &nbsp; [' ', ' ', ' ', ' ', ' '] <br>
]


### Color Board List Structure
PyWordle also provides a color board formatted in the same way as the board list detailed above. However, in place of each
letter is a color value.
* G - Green
* LG - Light Grey
* Y - Yellow

These color values correspond to the classic Wordle color values. <br>

Example color board wherein the first and second letters are in the correct spot, the third and fourth letters are not in
the word at all, and the last letter is in the word but is not in the correct spot. Game constraints and number of guesses
taken match example above. <br>
[<br>
&nbsp; &nbsp; &nbsp; ['G', 'G', 'LG', 'LG', 'Y'], <br>
&nbsp; &nbsp; &nbsp; [' ', ' ', ' ', ' ', ' '], <br>
&nbsp; &nbsp; &nbsp; [' ', ' ', ' ', ' ', ' '], <br>
&nbsp; &nbsp; &nbsp; [' ', ' ', ' ', ' ', ' '], <br>
&nbsp; &nbsp; &nbsp; [' ', ' ', ' ', ' ', ' '] <br>
]

### Example
An example implementation of this class in a PyWordle game in the terminal can be found in 
[terminalImplementationExample.py](terminalImplementationExample.py)

## PyWordle Web API
This branch of the project creates a web API (similar to the RESTful architecture) based off the PyWordle class. To create
a game instance, send a POST request to [/create_game](#post-create_game). From there on out, send POST requests to 
[/make_guess](#post-make_guess), [/game_info](#post-game_info),
and [/check_game_over](#post-check_game_over). More details listed below.

### POST /create_game
**Payload** <br>
None <br> <br>
**Return Value** <br>
_'game_id'_ -> ID used to access game in API server

### POST /make_guess
**Payload** <br>
_'game_id'_ -> Game ID obtained from creating a new game instance <br>
_'guess'_ -> Guess to be made in game <br> <br>
**Return Value**
_'game_response'_ -> Response from game which matches return value of .make_guess() in PyWordle class described 
[here](#make_guessguess-str)

### POST /game_info
**Payload** <br>
_'game_id'_ -> Game ID obtained from creating a new game instance <br><br>
**Return Value**
_'game_response'_ -> Response from game which matches return value of .get_info() in PyWordle class described 
[here](#get_info)

### POST /check_game_over
**Payload** <br>
_'game_id'_ -> Game ID obtained from creating a new game instance <br><br>
**Return Value**
_'game_response'_ -> Response from game which matches return value of .check_game_over() in PyWordle class described 
[here](#check_game_over)