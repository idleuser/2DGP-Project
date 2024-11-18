from pico2d import *
import game_framework
import game_world
from state_machine import *


PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_MPS = 3
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class SuperMushroom:
    image = None
    def __init__(self):
        self.x, self.y = 300, 90
        self.dir = 1
        if SuperMushroom.image == None:
            self.image = load_image('super_mushroom.png')
        self.state_machine = StateMachine(self)

    def update(self):
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if self.x > 400:
            self.dir = -1
        elif self.x < 200:
            self.dir = 1
        self.x = clamp(200, self.x, 400)

    def draw(self):
        self.image.clip_draw(0, 0, 225, 225, self.x, self.y, 40, 40)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 25 ,self.y - 20, self.x + 25, self.y

    def handle_collision(self, group, other):
        if group == 'mario-super_mushroom':
            game_world.remove_object(self)