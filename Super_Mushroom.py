from pico2d import *
import game_framework
import game_world
import server
from state_machine import *


PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_MPS = 2
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class SuperMushroom:
    image = None
    def __init__(self, name='None', x=0, y=0):
        self.name, self.x, self.y = name, x, y
        self.dir = 1
        if SuperMushroom.image == None:
            self.image = load_image('./resource/super_mushroom.png')

    def update(self):
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if self.x > 355:
            self.dir = -1
        elif self.x < 200:
            self.dir = 1
        self.x = clamp(200, self.x, 355)

    def draw(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        self.image.clip_draw(0, 0, 225, 225, sx, sy, 40, 40)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 25 ,sy - 20, sx + 25, sy + 20

    def get_head_box(self):
        return 0,0,0,0

    def handle_collision(self, group, other):
        if group == 'mario-super_mushroom':
            game_world.remove_object(self)