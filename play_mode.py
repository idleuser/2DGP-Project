from pico2d import *
import game_framework
import game_world
import title_mode
from Goomba import Goomba
from Mini_Mario import MiniMario
from Super_Mushroom import SuperMushroom
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
            mario.handle_event(event)

def init():
    global background
    global mario

    background = load_image('Background.png')

    mario = MiniMario()
    game_world.add_object(mario, 1)

    goomba = Goomba()
    game_world.add_object(goomba, 1)

    super_mushroom = SuperMushroom()
    game_world.add_object(super_mushroom, 1)

    box = Box()
    game_world.add_object(box, 1)

    itembox = ItemBox()
    game_world.add_object(itembox, 1)

    game_world.add_collision_pair('mario-kill', mario, goomba)
    game_world.add_collision_pair('mario-goomba', mario, goomba)
    game_world.add_collision_pair('mario-super_mushroom', mario, super_mushroom)
    game_world.add_collision_pair('mario-box', mario, box)
    game_world.add_collision_pair('mario-itembox', mario, itembox)

def finish():
    game_world.clear()

def update():
    game_world.update()
    game_world.handle_collisions()
    delay(0.08)

def draw():
    clear_canvas()
    background.draw(800 / 2, 600 / 2 + 20)
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass
