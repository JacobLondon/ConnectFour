from connectfour import Window 
from pyngine import Interface

def main():

    interface = Interface(window_text='Connect Four', resolution=(900,600), grid_width=9, grid_height=6)
    gui = Window(interface)
    gui.run()

if __name__ == '__main__':
    main()