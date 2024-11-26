from pico2d import *
import game_world, game_framework
import title_mode
from state_machine import *


PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_MPS = 5
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class Idle:
    @staticmethod
    def enter(obj , event):
        obj.frame = 0
        obj.time = get_time()
        if start_event(event):
            obj.dir = 1
        # elif right_down(event) or left_up(event):
        #     obj.dir = -1
        # elif left_down(event) or right_up(event):
        #     obj.dir = 1
    @staticmethod
    def do(obj):
        obj.frame = (obj.frame + (FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)) % 3
        if obj.safe and get_time() - obj.time > 1.0:
            obj.safe = 0
    @staticmethod
    def exit(obj, event):
        pass
    @staticmethod
    def draw(obj):
        if obj.dir == 1:
            if obj.life == 1:
                obj.image.clip_draw((int(obj.frame) + 8) * 19, 9 * 24, 19, 24, obj.x, obj.y, 60, 60)
            elif obj.life == 2:
                obj.image.clip_draw((int(obj.frame) + 8) * 19, 9 * 24, 19, 24, obj.x, obj.y+30, 60, 120)
        elif obj.dir == -1:
            if obj.life == 1:
                obj.image.clip_composite_draw((int(obj.frame) + 8)  * 19, 9 * 24, 19, 24, 0, 'h', obj.x, obj.y, 60, 60)
            elif obj.life == 2:
                obj.image.clip_composite_draw((int(obj.frame) + 8)  * 19, 9 * 24, 19, 24, 0, 'h', obj.x, obj.y + 30, 60, 120)

class Run:
    @staticmethod
    def enter(obj, event):
        obj.frame = 0
        obj.time = get_time()
        if right_down(event) or left_up(event):
            obj.dir = 1
        elif left_down(event) or right_up(event):
            obj.dir = -1

    @staticmethod
    def do(obj):
        if obj.safe and get_time() - obj.time > 1.0:
            obj.safe = 0
        obj.frame = (obj.frame + (FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)) % 6
        obj.x += obj.dir * RUN_SPEED_PPS * game_framework.frame_time
        obj.x = clamp(0, obj.x, 800)

    @staticmethod
    def exit(obj, event):
        if space_down(event):
            obj.run = 1
        else:
            obj.run = 0

    @staticmethod
    def draw(obj):
        if obj.dir == 1:
            if obj.life == 1:
                obj.image.clip_draw((int(obj.frame) + 8)  * 19, 5 * 24 - 1, 19, 24, obj.x, obj.y, 60, 60)
            elif obj.life == 2:
                obj.image.clip_draw((int(obj.frame) + 8) * 19, 5 * 24 - 1, 19, 24, obj.x, obj.y+30, 60, 120)
        elif obj.dir == -1:
            if obj.life == 1:
                obj.image.clip_composite_draw((int(obj.frame) + 8)  * 19, 5 * 24 - 1, 19, 24, 0, 'h', obj.x, obj.y, 60, 60)
            elif obj.life == 2:
                obj.image.clip_composite_draw((int(obj.frame) + 8)  * 19, 5 * 24 - 1, 19, 24, 0, 'h', obj.x, obj.y + 30, 60, 120)

class Jump:
    @staticmethod
    def enter(obj, event):
        obj.frame = 0
        obj.limit = False
        obj.time = get_time()
    @staticmethod
    def do(obj):
        obj.frame = (obj.frame + 1) % 6
        if obj.run:
            obj.x += obj.dir * RUN_SPEED_PPS * game_framework.frame_time
        if obj.safe and get_time() - obj.time > 1.0:
            obj.safe = 0
        if get_time() - obj.time > 0.8:
            obj.state_machine.add_event(('TIME_OUT', obj.run))
        if obj.y >= 330:
            obj.limit = True
        if obj.y < 330 and obj.limit == False:
            obj.y += 50
        elif obj.y > 90:
            obj.y -= 50
        obj.y = clamp(90, obj.y, 330)
    @staticmethod
    def exit(obj, event):
        pass
    @staticmethod
    def draw(obj):
        if obj.dir == 1:
            if obj.life == 1:
                obj.image.clip_draw((int(obj.frame) + 8)  * 19, 6 * 24, 19, 24, obj.x, obj.y, 60, 60)
            elif obj.life == 2:
                obj.image.clip_draw((int(obj.frame) + 8)  * 19, 6 * 24, 19, 24, obj.x, obj.y + 30, 60, 120)
        elif obj.dir == -1:
            if obj.life == 1:
                obj.image.clip_composite_draw((int(obj.frame) + 8)  * 19, 6 * 24, 19, 24, 0, 'h', obj.x, obj.y, 60, 60)
            elif obj.life == 2:
                obj.image.clip_composite_draw((int(obj.frame) + 8)  * 19, 6 * 24, 19, 24, 0, 'h', obj.x, obj.y + 30, 60, 120)

class MiniMario:
    def __init__(self):
        self.x, self.y = 100, 90
        self.frame = 0
        self.dir = 0
        self.run = 0
        self.life = 1
        self.safe = 0
        self.limit = False
        self.image = load_image('Mini_Mario.gif')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, space_down: Jump},
                Jump: {time_out_to_idle: Idle, time_out_to_run : Run},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down: Jump},
            }
        )

    def update(self):
            self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        if self.life == 1:
            return self.x - 30,self.y - 30, self.x + 20, self.y + 20
        if self.life == 2:
            return self.x - 30, self.y - 30, self.x + 20, self.y + 65

    def handle_collision(self, group, other):
        if group == 'mario-kill':
            self.safe = 1
        elif group == 'mario-goomba' and self.safe == 0:
            self.life -= 1
            self.safe = 1
            if self.life == 0:
                game_world.remove_object(self)
                game_framework.change_mode(title_mode)
        elif group == 'mario-super_mushroom':
            self.life = 2
        elif group == 'mario-box' or group == 'mario-itembox' or group == 'mario-usedbox':
            self.limit = True