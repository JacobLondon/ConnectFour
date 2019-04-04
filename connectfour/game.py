import numpy as np
from enum import Enum

class State(Enum):
    START = 0
    PLAYER_1 = 1
    PLAYER_2 = 2
    DONE = 3

class Cell(Enum):
    EMPTY = 0

class ConnectFour:

    def __init__(self):

        self.size = (6, 7)
        self.board = np.zeros(self.size)
        self.state = State.START
        self.turn_count = 0

        self.done = False
        self.winner = None

    def next_state(self):
        # game hasn't started
        if self.state == State.START:
            self.state = State.PLAYER_1

        # player 1 just went
        elif self.state == State.PLAYER_1:
            if self.has_won():
                self.winner = State.PLAYER_1
                self.state = State.DONE
            elif self.turn_count == self.size[0] * self.size[1] - 1:
                self.state = State.DONE
            else:
                self.turn_count += 1
                self.state = State.PLAYER_2

        # player 2 just went
        elif self.state == State.PLAYER_2:
            if self.has_won():
                self.winner = State.PLAYER_2
                self.state = State.DONE
            elif self.turn_count == self.size[0] * self.size[1] - 1:
                self.state = State.DONE
            else:
                self.turn_count += 1
                self.state = State.PLAYER_1

        # all turns are spent
        elif self.state == State.DONE:
            self.done = True

    def has_won(self):
        pass

    def place_token(self, x):
        for cell in range(self.size[0]):
            if cell == self.size[0] - 1 and self.board[cell][x] == Cell.EMPTY:
                self.board[cell][x] = self.state
            elif cell != Cell.EMPTY:#TODO
                pass
