from pico2d import *
import game_framework
import play_mode as start_mode

def main():
    open_canvas(800, 500)
    game_framework.run(start_mode)
    close_canvas()

if __name__ == '__main__':
    main()