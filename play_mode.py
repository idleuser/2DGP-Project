from pico2d import *
import game_framework
import game_world
import server
import title_mode
from Goomba import Goomba
from Mario import Mario
from Pipe import Pipe
from Super_Mushroom import SuperMushroom
from background import Background
from box import Box
from item_box import ItemBox


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
    server.background = Background()
    game_world.add_object(server.background, 0)

    with open('object_data.json','r') as f:
        obj_data_list = json.load(f)
        for item in obj_data_list:
            if item["name"] == 'Mario':
                server.mario = Mario()
                server.mario.__dict__.update(item)
                game_world.add_object(server.mario, 1)
            elif item["name"] == 'goomba':
                goomba = Goomba()
                goomba.__dict__.update(item)
                game_world.add_object(goomba, 1)
            elif item["name"] == 'super_mushroom':
                super_mushroom = SuperMushroom()
                super_mushroom.__dict__.update(item)
                game_world.add_object(super_mushroom, 1)
            elif item["name"] == 'box':
                box = Box()
                box.__dict__.update(item)
                game_world.add_object(box, 1)
            elif item["name"] == 'item_box':
                item_box = ItemBox()
                item_box.__dict__.update(item)
                game_world.add_object(item_box, 1)
            elif item["name"] == 'pipe':
                pipe = Pipe()
                pipe.__dict__.update(item)
                game_world.add_object(pipe, 2)

    game_world.add_collision_pair('mario-goomba', server.mario, goomba)
    game_world.add_collision_pair('mario-super_mushroom', server.mario, super_mushroom)
    game_world.add_collision_pair('mario-box', server.mario, box)
    game_world.add_collision_pair('mario-item_box', server.mario, item_box)
    game_world.add_collision_pair('mario-pipe', server.mario, pipe)

    game_world.add_collision_pair('mario-on',server.mario, goomba)
    game_world.add_collision_pair('mario-on',server.mario, box)
    game_world.add_collision_pair('mario-on',server.mario, item_box)

    game_world.add_collision_pair('mario-on',server.mario, pipe)


def finish():
    game_world.clear()

def update():
    game_world.update()
    game_world.handle_collisions()
    delay(0.08)

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass
