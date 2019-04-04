from threading import Thread
import time, pygame

from pyngine import *
from .game import ConnectFour

class Window(Controller):

    def __init__(self, interface):
        Controller.__init__(self, interface, debug=False)

        self.size = (6, 7)
        self.game = ConnectFour(size=self.size, printing=True)
        # override game's input for gui input
        self.game.get_input = self.get_input
        self.game_thread = Thread(target=self.game.play, args=())

        self.create_new = False
        self.debounce = 0.1
        self.even_col = Color['gray']
        self.odd_col = Color['darkgray']
        self.p1_col = Color['red1']
        self.p2_col = Color['yellow1']

    def initialize_components(self):
        self.game_panel = Panel(self)
        self.game_panel.width, self.game_panel.height = \
            self.screen_grid.get_pixel(self.size[0], self.size[1])
        
        self.game_panel.background = self.even_col

        self.column_drawer = Drawer(self, refresh=self.draw_columns)
        self.token_drawer = Drawer(self, refresh=self.draw_tokens)

    """Draw columns for tokens to be in"""
    def draw_columns(self):
        for col in range(self.size[1]):
            if col % 2 == 0:
                self.painter.fill_area(
                    x=col * self.interface.tile_width,
                    y=0,
                    width=self.interface.tile_width,
                    height=self.interface.resolution[1],
                    color=self.odd_col
                )

    """Draw the tokens at the specified locations"""
    def draw_tokens(self):
        for gy in range(len(self.game.board)):
            for gx in range(len(self.game.board[0])):
                radius = int(self.interface.tile_width / 2)
                x = int(gx * self.interface.tile_width + radius)
                y = int(gy * self.interface.tile_height + radius)

                if self.game.board[gy][gx] == 1:
                    self.painter.draw_circle(x, y, radius, self.p1_col)
                elif self.game.board[gy][gx] == 2:
                    self.painter.draw_circle(x, y, radius, self.p2_col)

    """Start playing game after component initialization"""
    def setup(self):
        self.game_thread.start()

    """Forcibly end the game and join the thread"""
    def close_actions(self):
        self.game.done = True
        self.game_thread.join()

    """Wait for user mouse input and debounce"""
    def get_input(self, player):
        # wait for input
        while not self.mouse.presses[Mouse.l_click]:
            time.sleep(self.interface.frame_time)
            # stop waiting for input if the game comes to an end
            if self.game.done:
                return 0
        
        tx, _ = self.interface.get_mouse_tile()
        tx = int(tx)
        time.sleep(self.debounce)
        return tx
