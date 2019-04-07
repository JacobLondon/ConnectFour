from threading import Thread
import time, pygame

from pyngine import *
from .game import ConnectFour, State

class Window(Controller):

    def __init__(self, interface):
        Controller.__init__(self, interface, debug=False)

        self.size = (6, 7)
        self.game = ConnectFour(size=self.size, printing=False)
        # override game's input for gui input
        self.game.get_input = self.get_input
        self.game_thread = Thread(target=self.game.play, args=())

        self.debounce = 0.05
        self.options_col = Color['gray20']
        self.even_col = Color['gray']
        self.odd_col = Color['darkgray']
        self.p1_col = Color['yellow1']
        self.p2_col = Color['red1']

    """Initialize gui components and inputs"""
    def initialize_components(self):

        offset = self.size[1] + 1

        # the game board
        self.game_panel = Panel(self)
        self.game_panel.width, self.game_panel.height = \
            self.interface.tile_width * self.size[1], self.screen_height
        self.game_panel.background = self.even_col

        # label and buttons
        self.options_panel = Panel(self)
        self.options_panel.loc = self.screen_grid.get_pixel(self.size[1], 0)
        self.options_panel.width, self.options_panel.height = \
            self.screen_grid.get_pixel(self.screen_width - self.interface.tile_width * self.size[0], self.screen_height)
        self.options_panel.background = self.options_col
        # initialize and set locations of components
        self.color_panel = Panel(self)
        self.logo_label = Label(self, 'Connect Four')
        self.undo_button = Button(self, 'Undo')
        self.reset_button = Button(self, 'Reset')
        # anchor at center
        self.logo_label.anchor = self.logo_label.center
        self.color_panel.anchor = self.color_panel.center
        self.undo_button.anchor = self.undo_button.center
        self.reset_button.anchor = self.reset_button.center
        # locations going downards
        self.logo_label.loc = self.screen_grid.get_pixel(offset, 1)
        self.color_panel.loc = self.logo_label.loc
        self.undo_button.loc = self.screen_grid.get_pixel(offset, 4)
        self.reset_button.loc = self.screen_grid.get_pixel(offset, 5)
        # button event actions
        self.undo_button.action = self.undo
        self.reset_button.action = self.reset
        # misc options
        self.logo_label.foreground = Color['black']
        self.color_panel.height = self.undo_button.height
        self.color_panel.width = self.undo_button.width

        # events and drawing
        self.undo_event = Event(self, action=self.undo, keys=(pygame.K_u,))
        self.reset_event = Event(self, action=self.reset, keys=(pygame.K_n,))
        self.column_drawer = Drawer(self, refresh=self.draw_columns)
        self.token_drawer = Drawer(self, refresh=self.draw_tokens)
        self.turn_drawer = Drawer(self, refresh=self.draw_turn)

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
        for i, row in enumerate(self.game.board):
            for j, token in enumerate(row):
                radius = int(self.interface.tile_width / 2)
                x = int(j * self.interface.tile_width + radius)
                y = int(i * self.interface.tile_height + radius)

                if token == 1:
                    self.painter.draw_circle(x, y, radius, self.p1_col)
                elif token == 2:
                    self.painter.draw_circle(x, y, radius, self.p2_col)

    """Draw a box of who's turn it is"""
    def draw_turn(self):
        if self.game.turn_count % 2 == 0:
            self.color_panel.background = self.p1_col
        else:
            self.color_panel.background = self.p2_col

    """Start playing game after component initialization"""
    def setup(self):
        self.game_thread.start()

    """Forcibly end the game and join the thread"""
    def close_actions(self):
        self.game.state = State.QUIT
        self.game_thread.join()

    """Wait for user mouse input"""
    def get_input(self, player):
        # wait for input
        while not self.game_panel.focused:
            time.sleep(self.interface.frame_time)
            # stop waiting for input if the game comes to an end
            playing = any([
                self.game.state == State.PLAYER_1,
                self.game.state == State.PLAYER_2
            ])
            if self.game.done or not playing:
                return -1

        self.game_panel.focused = False
        #time.sleep(self.debounce)
        tx, _ = self.interface.get_mouse_tile()
        tx = int(tx)
        return tx

    """Undo the last move"""
    def undo(self):
        self.undo_event.halt()
        self.game.state = State.UNDO

    """Reset the game"""
    def reset(self):
        self.reset_event.halt()
        self.game.state = State.RESET
