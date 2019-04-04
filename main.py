from connectfour import Window 
from pyngine import Interface

def main():

    interface = Interface(window_text='Connect Four', resolution=(1000,600), grid_width=10, grid_height=6)
    gui = Window(interface)
    gui.run()

if __name__ == '__main__':
    main()