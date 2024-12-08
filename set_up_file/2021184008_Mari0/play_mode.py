from pico2d import *
import game_framework
import game_world
import server
import title_mode
from Goomba import Goomba
from Mario import Mario
from Pipe import Pipe
from Super_Mushroom import SuperMushroom
from background import Background, Boss_background
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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_s:
            print('Save Completed!')
            game_world.save()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_l:
            print('Load Completed!')
            load_saved_world()
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
            elif item["name"] == 'box1':
                box1 = Box()
                box1.__dict__.update(item)
                game_world.add_object(box1, 1)
            elif item["name"] == 'box2':
                box2 = Box()
                box2.__dict__.update(item)
                game_world.add_object(box2, 1)
            elif item["name"] == 'box3':
                box3 = Box()
                box3.__dict__.update(item)
                game_world.add_object(box3, 1)
            elif item["name"] == 'item_box1':
                item_box1 = ItemBox()
                item_box1.__dict__.update(item)
                game_world.add_object(item_box1, 1)
            elif item["name"] == 'item_box2':
                item_box2 = ItemBox()
                item_box2.__dict__.update(item)
                game_world.add_object(item_box2, 1)
            elif item["name"] == 'pipe1':
                pipe1 = Pipe()
                pipe1.__dict__.update(item)
                game_world.add_object(pipe1, 2)
            elif item["name"] == 'pipe2':
                pipe2 = Pipe()
                pipe2.__dict__.update(item)
                game_world.add_object(pipe2, 2)

    game_world.add_collision_pair('mario-goomba', server.mario, goomba)
    game_world.add_collision_pair('mario-box', server.mario, box1)
    game_world.add_collision_pair('mario-box', server.mario, box2)
    game_world.add_collision_pair('mario-box', server.mario, box3)
    game_world.add_collision_pair('mario-item_box1', server.mario, item_box1)
    game_world.add_collision_pair('mario-item_box2', server.mario, item_box2)
    game_world.add_collision_pair('mario-pipe', server.mario, pipe1)
    game_world.add_collision_pair('mario-pipe', server.mario, pipe2)

    game_world.add_collision_pair('mario-on',server.mario, goomba)
    game_world.add_collision_pair('mario-on',server.mario, box1)
    game_world.add_collision_pair('mario-on',server.mario, item_box1)
    game_world.add_collision_pair('mario-on',server.mario, item_box2)
    game_world.add_collision_pair('mario-on', server.mario, pipe1)
    game_world.add_collision_pair('mario-on', server.mario, pipe2)


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

def load_saved_world():
    game_world.load()
    for obj in game_world.all_objects():
        if isinstance(obj, Mario):
            server.mario = obj
        elif isinstance(obj, Background):
            server.background = obj
        elif isinstance(obj, Boss_background):
            server.background = obj