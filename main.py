from tictactoe import Window 
from pyngine import Interface

def main():
    interface = Interface(window_text='Tic Tac Toe', resolution=(800,700), grid_width=8, grid_height=7)

    gui = Window(interface)
    gui.run()

if __name__ == '__main__':
    main()