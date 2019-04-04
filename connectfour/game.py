import numpy as np
from enum import Enum
from copy import copy

class State(Enum):
    START = 0
    PLAYER_1 = 1
    PLAYER_2 = 2
    DONE = 3

class ConnectFour:

    def __init__(self, size=(6, 7), printing=True):

        self.size = size
        self.board = np.zeros(self.size)
        self.state = State.START
        self.turn_count = 0
        # record where the next available spot is
        self.placement = np.zeros((1, self.size[1]), dtype=int)[0] + self.size[0] - 1

        self.printing = printing
        self.done = False
        self.winner = 'Tie game'

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

        # all turns are spent
        elif self.state == State.DONE:
            self.done = True

    def player_state(self, cur_player, next_player):

        # check if there are no more moves left
        if self.turn_count == self.size[0] * self.size[1]:
            self.state = State.DONE
            return

        # get valid input if there are turns still
        while not self.place_token(cur_player):
            print('Illegal move')

        # check if the move won the game
        if self.has_won():
            self.winner = cur_player
            self.state = State.DONE

        # go to next player's turn
        else:
            self.turn_count += 1
            self.state = next_player

    def get_input(self, player):
        return input(f'Player {player.value}> ')

    def has_won(self):
        return False

    def place_token(self, player):
        try:
            x = int(self.get_input(player)) - 1
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

        return True

    def print(self):
        if self.printing and self.turn_count < self.size[0] * self.size[1]:
            print('_' * (self.size[1] - 1) * 4)
            print(f'Turn {self.turn_count + 1}:\n')
            print(self.board)
            print('\n', [c for c in range(1, self.size[1] + 1)])

    def play(self):
        # play game
        while not self.done:
            self.next_state()

        # display winner
        if self.printing:
            print('\n', self.winner, '\n', sep='')

if __name__ == '__main__':
    game = ConnectFour()
    game.play()
