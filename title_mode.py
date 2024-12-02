import game_framework
from pico2d import *
from sdl2 import *
import play_mode


def init():
    global image
    image = load_image('./resource/title.png')

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN):
            game_framework.change_mode(play_mode)

def draw():
    clear_canvas()
    image.draw(800/2,500/2)
    update_canvas()

def finish():
    global image
    del image

def update():
    pass