from pico2d import *
import game_framework
import game_world
import server
import Bowser

PIXEL_PER_METER = (10.0 / 0.3)
FIRE_SPEED_MPS = 10
FIRE_SPEED_PPS = (FIRE_SPEED_MPS * PIXEL_PER_METER)

class  fireBall:
    image = None
    def __init__(self, x, y, dir):
        self.name = 'fire_breath'
        self.x, self.y, self.dir = x, y, dir
        self.count = 0
        if fireBall.image == None:
            self.image = load_image('./resource/firebreath.png')
    def update(self):
        distance = FIRE_SPEED_MPS * game_framework.frame_time
        self.x += distance * self.dir
        self.y += distance * self.dir
        if self.count > 10:
            game_world.remove_object(self)
        else:
            self.count += 1

    def draw(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        if self.dir > 0:
            self.image.draw(sx, sy, 20, 20)
        else:
            self.image.clip_composite_draw(0, 0, 79, 61, 0, 'h', sx, sy, 20, 20)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 10,sy - 10, sx + 10, sy + 10

    def get_head_box(self):
        return 0,0,0,0

    def handle_collision(self, group, other):
        if group == 'goomba-fire_ball':
            game_world.remove_object(self)