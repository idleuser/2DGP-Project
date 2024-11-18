from pico2d import *
import game_framework
import game_world
import title_mode
from Goomba import Goomba
from Mini_Mario import MiniMario
from Super_Mushroom import SuperMushroom


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
    global mario
    mario = MiniMario()
    game_world.add_object(mario, 1)

    goomba = Goomba()
    game_world.add_object(goomba, 1)

    super_mushroom = SuperMushroom()
    game_world.add_object(super_mushroom, 1)

    game_world.add_collision_pair('mario-kill', mario, goomba)
    game_world.add_collision_pair('mario-goomba', mario, goomba)
    game_world.add_collision_pair('mario-super_mushroom', mario, super_mushroom)


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
