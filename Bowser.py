from pico2d import *
import game_framework
import game_world
import server
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_MPS = 4
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 5.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 7

class Bowser:
    def __init__(self, name='Noname', x=0, y=0, life=0):
        self.name, self.x, self.y, self.life = name, x, y, life
        self.dir = -1
        self.frame = 0
        self.image = load_image('./resource/bowser.png') # 21 idle

    def update(self):
        #self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        self.frame = (self.frame + (FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)) % 7 + 1


    def draw(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        self.image.clip_composite_draw(int(self.frame) * 55 - 11, 21 * 65 - 3, 55, 65, 0, 'h', sx, sy, 120, 120)
        # draw_rectangle(*self.get_bb())
        # draw_rectangle(*self.get_head_box())

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 25 ,sy - 20, sx + 25, sy

    def get_head_box(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 10 ,sy + 1, sx + 10, sy + 20

    def handle_collision(self, group, other):
        pass