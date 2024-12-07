from pico2d import *
import game_framework
import game_world
import server
import Bowser

PIXEL_PER_METER = (10.0 / 0.3)
FIRE_SPEED_MPS = 10
FIRE_SPEED_PPS = (FIRE_SPEED_MPS * PIXEL_PER_METER)

class  FireBreath:
    image = None
    def __init__(self, x, y, tx, ty):
        self.name = 'fire_breath'
        self.x, self.y, self.tx, self.ty = x, y, tx, ty
        if FireBreath.image == None:
            self.image = load_image('./resource/firebreath.png')
        self.dir = math.atan2(self.ty - self.y, self.tx - self.x)
        self.toward = self.x - self.tx

    def update(self):
        distance = FIRE_SPEED_MPS * game_framework.frame_time
        self.x += distance * math.cos(self.dir)
        self.y += distance * math.sin(self.dir)
        if Bowser.firebreath_exist == True and (self.x < 0 or self.x > 800 or self.y < 0 or self.y > 500):
            Bowser.firebreath_exist = False
            game_world.remove_object(self)

    def draw(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        if self.toward > 0:
            self.image.draw(sx, sy, 50, 50)
        else:
            self.image.clip_composite_draw(0, 0, 79, 61, 0, 'h', sx, sy, 50, 50)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 30 ,sy - 30, sx + 30, sy + 30

    def get_head_box(self):
        return 0,0,0,0

    def handle_collision(self, group, other):
        if group == 'mario-fire_breath':
            Bowser.firebreath_exist = False
            game_world.remove_object(self)