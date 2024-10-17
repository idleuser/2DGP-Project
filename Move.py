from pico2d import *
from Mario import Mini_Mario

def handle_events():
    global game_running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_running = False

def reset_world():
    global game_running
    global world
    global mario

    game_running = True
    world = []
    mini_mario = Mini_Mario()
    world.append(mini_mario)

def update_world():
    for obj in world:
        obj.update()

def render_world():
    clear_canvas()
    for obj in world:
        obj.draw()
    update_canvas()

def main():
    open_canvas()
    reset_world()
    while game_running:
        handle_events()
        update_world()
        render_world()
        delay(0.5)

    close_canvas()

if __name__ == '__main__':
    main()