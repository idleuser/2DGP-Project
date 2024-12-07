from pico2d import *
import Mario
import game_framework
import game_world
import server
import title_mode
from Bowser import Bowser
from background import Boss_background

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            server.mario.handle_event(event)

def init():
    server.background = Boss_background()
    game_world.add_object(server.background, 0)

    server.mario = Mario.Mario()
    game_world.add_object(server.mario, 1)

    with open('object_data.json', 'r') as f:
        obj_data_list = json.load(f)
        for item in obj_data_list:
            if item["name"] == 'Bowser':
                bowser = Bowser()
                bowser.__dict__.update(item)
                game_world.add_object(bowser, 1)


def finish():
    game_world.clear()

def update():
    game_world.update()
    #game_world.handle_collisions()
    delay(0.08)

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass
