from pico2d import *
import game_framework
import game_world
import server
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from firebreath import FireBreath

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_MPS = 2
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 5.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 7

states = ['Idle', 'Run']
firebreath_exist = False

class Bowser:
    def __init__(self, name='Noname', x=0, y=0, life=0):
        self.name, self.x, self.y, self.life = name, x, y, life
        self.dir = -1
        self.frame = 0
        self.image = load_image('./resource/bowser.png') # 21 idle
        self.state = 'Idle'
        self.tx, self.ty = server.mario.x, server.mario.y
        self.time = 0
        self.build_behavior_tree()

    def update(self):
        self.tx, self.ty = server.mario.x, server.mario.y
        self.frame = (self.frame + (FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)) % FRAMES_PER_ACTION + 1
        self.bt.run()

    def draw(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        if self.state == 'Idle':
            self.image.clip_composite_draw(int(self.frame) * 55 - 11, 21 * 65 - 3, 55, 65, 0, 'h', sx, sy, 120, 120)
        elif self.state == 'Run':
            if self.dir == 1:
                self.image.clip_draw(int(self.frame) * 55 - 11, 21 * 65 - 3, 55, 65, sx, sy, 120, 120)
            elif self.dir == -1:
                self.image.clip_composite_draw(int(self.frame) * 55 - 11, 21 * 65 - 3, 55, 65, 0, 'h', sx, sy, 120, 120)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 58 ,sy - 50, sx + 50, sy + 58

    def get_head_box(self):
        pass

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        pass


    def distance_x_less_than(self, x1, x2):
        distance = (x1 - x2) ** 2
        return distance < (PIXEL_PER_METER * 0.5) ** 2

    def distance_less_than(self, x1, y1, x2, y2):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * 0.5) ** 2

    def move_to(self, tx):
        self.dir = 1 if tx > self.x else -1
        distance = RUN_SPEED_PPS * game_framework.frame_time
        self.x += distance * self.dir

    def short_rest(self):
        self.state = 'Idle'
        if get_time() - self.time > 0.5:
            return BehaviorTree.RUNNING
        else:
            return BehaviorTree.SUCCESS

    def run_to_mario(self):
        self.state = 'Run'
        self.move_to(self.tx)
        if self.distance_x_less_than(self.tx, self.x):
            self.time = get_time()
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def fire_to_mario(self):
        global firebreath_exist

        self.state = 'Idle'
        if firebreath_exist == False:
            self.time = get_time()
            firebreath_exist = True
            fire_breath = FireBreath(self.x, self.y + 5, self.tx, self.ty)
            game_world.add_object(fire_breath)
            game_world.add_collision_pair('mario-fire_breath', server.mario, fire_breath)

    def is_mario_on_floor(self):
        if self.ty <= 120:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def build_behavior_tree(self):
        a1 = Action('달리기', self.run_to_mario)
        a2 = Action('불 쏘기', self.fire_to_mario)
        a3 = Action('휴식', self.short_rest)

        c1 = Condition('마리오가 땅에 있는가?', self.is_mario_on_floor)

        chase = Sequence('마리오에게 몸통박치기', c1, a1)
        fire = Sequence('마리오를 향해 불 쏘기', a2)

        root = Selector('달리기 or 불 쏘기', chase, fire)

        self.bt = BehaviorTree(root)