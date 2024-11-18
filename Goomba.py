from pico2d import *
import game_framework
import game_world
from state_machine import *


PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_MPS = 3
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Goomba:
    image = None
    def __init__(self):
        self.x, self.y = 400, 90
        self.dir = 0
        self.life = 2
        if Goomba.image == None:
            self.image = load_image('Goomba.png')
        self.state_machine = StateMachine(self)

    def update(self):
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if self.x > 800:
            self.dir = -1
        elif self.x < 400:
            self.dir = 1
        self.x = clamp(400, self.x, 800)

    def draw(self):
        if self.life == 2:
            self.image.clip_draw(0, 2 * 528, 699, 529, self.x, self.y, 50, 40)
        elif self.life == 1:
            self.image.clip_draw(0, 0, 699, 400, self.x, self.y, 50, 40)
        draw_rectangle(*self.get_bb())
        draw_rectangle(*self.get_head_box())

    def get_bb(self):
        return self.x - 25 ,self.y - 20, self.x + 25, self.y
    def get_head_box(self):
        return self.x - 20 ,self.y + 1, self.x + 20, self.y + 20

    def handle_collision(self, group, other):
        if group == 'mario-kill':
            self.life -= 1
            if self.life == 0:
                game_world.remove_object(self)
        elif group == 'mario-goomba':
            pass