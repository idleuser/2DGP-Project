from pico2d import *
import game_framework
import game_world
from state_machine import *


PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_MPS = 2
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Box:
    image = None
    num = 0

    def __init__(self):
        self.x, self.y = 250 + self.num, 260
        self.dir = 1
        # if Box.num == 0:
        #     self.num = 100
        if Box.image == None:
            self.image = load_image('box.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y, 50, 48)

    def get_bb(self):
        return self.x - 25 ,self.y - 24, self.x + 25, self.y + 24

    def handle_collision(self, group, other):
        if group == 'mario-box':
            game_world.remove_object(self)