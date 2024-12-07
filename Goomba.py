from pico2d import *
import game_framework
import game_world
import server
from state_machine import *


PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_MPS = 2
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.25
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Goomba:
    image = None
    def __init__(self, name='Noname', x=0, y=0, life=0):
        self.name, self.x, self.y, self.life = name, x, y, life
        self.dir = -1
        self.frame = 0
        self.img_y = 0
        if Goomba.image == None:
            self.image = load_image('./resource/goomba.png')
            self.image_die = load_image('./resource/goomba_die.png')

    def update(self):
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        self.frame = (self.frame + (FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)) % 8
        if self.frame == 0:
            self.img_y = 1 - self.img_y
        if self.x > 790:
            self.dir = -1
        elif self.x < 480:
            self.dir = 1
        self.x = clamp(480, self.x, 790)

    def draw(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        if self.life == 2:
            if self.dir == 1:
                self.image.clip_composite_draw(int(self.frame) * 120 + 2, self.img_y * 106, 121, 106, 0, 'h',sx, sy, 60, 50)
            elif self.dir == -1:
                self.image.clip_draw(int(self.frame) * 120 + 2, self.img_y * 106, 121, 106, sx, sy, 60, 50)
        elif self.life == 1:
            self.image_die.draw(sx,sy,70,60)
        draw_rectangle(*self.get_bb())
        draw_rectangle(*self.get_head_box())

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 25 ,sy - 20, sx + 25, sy

    def get_head_box(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 15 ,sy + 1, sx + 15, sy + 20

    def handle_collision(self, group, other):
        if group == 'mario-on':
            self.life -= 1
            if self.life == 0:
                game_world.remove_object(self)
        elif group == 'mario-goomba':
            pass