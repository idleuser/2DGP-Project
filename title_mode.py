import game_framework
from pico2d import *
import game_world
import play_mode
import server
from Mario import Mario
from background import Title_background, Background, Boss_background


def init():
    global title_background # title이 문제
    title_background = Title_background()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            game_framework.change_mode(play_mode)

def draw():
    clear_canvas()
    title_background.draw()
    update_canvas()

def finish():
    pass

def update():
    pass