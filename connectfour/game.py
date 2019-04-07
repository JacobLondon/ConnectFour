import numpy as np
from enum import Enum
from copy import copy

class State(Enum):
    START = 0
    PLAYER_1 = 1
    PLAYER_2 = 2
    UNDO = 3
    RESET = 4
    CONTINUE = 5
    DONE = 6
    QUIT = 7

"""Connect four done with a state machine"""
class ConnectFour:

    def __init__(self, size=(6, 7), printing=True):

        self.size = size
        self.printing = printing
        self.clear_board()

    """Defaults for a new game"""
    def clear_board(self):
        self.board = np.zeros(self.size)
        self.state = State.START
        self.turn_count = 0
        # record where the next available spot is
        self.placement = np.zeros((1, self.size[1]), dtype=int)[0] + self.size[0] - 1
        self.moves = []
        self.done = False
        self.quit = False
        self.winner = 'Tie game'

    """Go to the next state available in the game"""
    def next_state(self):
        # game hasn't started
        if self.state == State.START:
            self.state = State.PLAYER_1

        # player 1 just went
        elif self.state == State.PLAYER_1:
            self.print()
            self.player_state(State.PLAYER_1, State.PLAYER_2)

        # player 2 just went
        elif self.state == State.PLAYER_2:
            self.print()
            self.player_state(State.PLAYER_2, State.PLAYER_1)

        # user wants to undo
        elif self.state == State.UNDO:
            self.undo()

        # reset the current state to start
        elif self.state == State.RESET:
            self.reset()

        # game done, prompt for continuing to play
        elif self.state == State.CONTINUE:
            self.prompt()

        # all turns are spent
        elif self.state == State.DONE:
            self.done = True

        # if the program will exit
        elif self.state == State.QUIT:
            self.quit = True

    """All things that occur for each player during their state"""
    def player_state(self, cur_player, next_player):

        # check if there are no more moves left
        if self.turn_count == self.size[0] * self.size[1]:
            self.state = State.DONE
            return

        current_state = copy(self.state)

        # get valid input if there are turns still
        while not self.place_token(cur_player):
            # quit out if the state changes while waiting for input
            if current_state != self.state:
                return

        # check if the move won the game
        if self.has_won():
            self.winner = cur_player
            self.state = State.DONE

        # go to next player's turn
        else:
            self.turn_count += 1
            self.state = next_player

    """Get input for which column to place the token in"""
    def get_input(self, player):
        move = input(f'Player {player.value}> ')
        if move.lower() == 'u':
            self.state = State.UNDO
            return -1
        elif move.lower() == 'n':
            self.state = State.RESET
            return -1
        else:
            return int(move) - 1

    """Determine if the move performed is winning"""
    def has_won(self):
        return False

    """Place token at next available spot on the game board"""
    def place_token(self, player):
        
        # convert user input to int
        try:
            # convert from 1-7 to 0-6
            x = self.get_input(player)
        except ValueError:
            return False

        # oob check
        if x < 0 or x >= self.size[1] or self.placement[x] < 0:
            return False

        # place at the location
        row = copy(self.placement[x])
        col = copy(x)
        self.board[row][col] = player.value

        # the next spot available in that column
        self.placement[x] -= 1
        self.moves.append(x)

        # successful placement
        return True

    """Go to previous game state"""
    def undo(self):
        
        # reset last move
        if self.turn_count - 1 >= 0:
            self.turn_count -= 1

        # take off previous move
        if self.moves:
            x = self.moves.pop()
            self.placement[x] += 1
            y = self.placement[x]
            self.board[y][x] = 0

        # go to previous state
        if self.turn_count % 2 == 1:
            self.state = State.PLAYER_2
        elif self.turn_count % 2 == 0:
            self.state = State.PLAYER_1
        else:
            self.state = State.START

    """Reset the game with a prompt"""
    def reset(self):
        self.clear_board()
        self.play()
        self.state = State.QUIT

    """Prompt the user for a reset"""
    def prompt(self):
        response = input('Play again? [y/n] ')
        if response.lower() == 'y':
            self.state = State.RESET

    """Display the game board and the column numbers 1-7"""
    def print(self):
        # printing and there are still moves left
        if self.printing and self.turn_count < self.size[0] * self.size[1]:
            print('_' * (self.size[1] - 1) * 4)
            print(f'Turn {self.turn_count + 1}:\n')
            print(self.board)
            print('\n', [c for c in range(1, self.size[1] + 1)])

    """Play the game until the state done is reached"""
    def play(self):

        # if used by another, expect a different ending
        def repeat():
            if __name__ == '__main__':
                return not self.done
            else:
                return True

        # play game
        while repeat():
            if self.quit:
                return
            else:
                self.next_state()

if __name__ == '__main__':
    game = ConnectFour()
    game.play()
