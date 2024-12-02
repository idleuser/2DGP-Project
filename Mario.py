from pico2d import *
import game_world, game_framework
import server
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
        obj.speed = 0
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
        obj.run = 0
    @staticmethod
    def draw(obj):
        sx = obj.x - server.background.window_left
        sy = obj.y - server.background.window_bottom
        if obj.dir == 1:
            if obj.life == 1:
                obj.image.clip_draw((int(obj.frame) + 8) * 19, 9 * 24, 19, 24, sx, sy, 60, 60)
            elif obj.life == 2:
                obj.image.clip_draw((int(obj.frame) + 8) * 19, 9 * 24, 19, 24, sx, sy + 30, 60, 120)
        elif obj.dir == -1:
            if obj.life == 1:
                obj.image.clip_composite_draw((int(obj.frame) + 8) * 19, 9 * 24, 19, 24, 0, 'h', sx, sy, 60, 60)
            elif obj.life == 2:
                obj.image.clip_composite_draw((int(obj.frame) + 8) * 19, 9 * 24, 19, 24, 0, 'h', sx, sy + 30, 60, 120)

class Run:
    @staticmethod
    def enter(obj, event):
        obj.frame = 0
        obj.time = get_time()
        if right_down(event) or left_up(event):
            obj.dir = 1
        elif left_down(event) or right_up(event):
            obj.dir = -1
        obj.speed = RUN_SPEED_PPS

    @staticmethod
    def do(obj):
        if obj.safe and get_time() - obj.time > 1.0:
            obj.safe = 0
        obj.frame = (obj.frame + (FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)) % 6
        obj.x += obj.dir * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def exit(obj, event):
        obj.run = 1

    @staticmethod
    def draw(obj):
        sx = obj.x - server.background.window_left
        sy = obj.y - server.background.window_bottom
        if obj.dir == 1:
            if obj.life == 1:
                obj.image.clip_draw((int(obj.frame) + 8)  * 19, 5 * 24 - 1, 19, 24, sx, sy, 60, 60)
            elif obj.life == 2:
                obj.image.clip_draw((int(obj.frame) + 8) * 19, 5 * 24 - 1, 19, 24, sx, sy + 30, 60, 120)
        elif obj.dir == -1:
            if obj.life == 1:
                obj.image.clip_composite_draw((int(obj.frame) + 8) * 19, 5 * 24 - 1, 19, 24, 0, 'h', sx, sy, 60, 60)
            elif obj.life == 2:
                obj.image.clip_composite_draw((int(obj.frame) + 8) * 19, 5 * 24 - 1, 19, 24, 0, 'h', sx, sy + 30, 60, 120)

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
            obj.state_machine.add_event(('TIME_OUT', 0))
        if obj.y >= 330:
            obj.limit = True
        if obj.limit == False:
            obj.y += 50
        elif obj.limit == True:
            obj.y -= 50
        obj.y = clamp(80, obj.y, 330)
    @staticmethod
    def exit(obj, event):
        pass
    @staticmethod
    def draw(obj):
        sx = obj.x - server.background.window_left
        sy = obj.y - server.background.window_bottom
        if obj.dir == 1:
            if obj.life == 1:
                obj.image.clip_draw((int(obj.frame) + 8)  * 19, 6 * 24, 19, 24, sx, sy, 60, 60)
            elif obj.life == 2:
                obj.image.clip_draw((int(obj.frame) + 8)  * 19, 6 * 24, 19, 24, sx, sy + 30, 60, 120)
        elif obj.dir == -1:
            if obj.life == 1:
                obj.image.clip_composite_draw((int(obj.frame) + 8)  * 19, 6 * 24, 19, 24, 0, 'h', sx, sy, 60, 60)
            elif obj.life == 2:
                obj.image.clip_composite_draw((int(obj.frame) + 8)  * 19, 6 * 24, 19, 24, 0, 'h', sx, sy + 30, 60, 120)

class Mario:
    def __init__(self):
        self.x, self.y = 100, 80
        self.frame = 0
        self.dir = 0
        self.run = 0
        self.life = 1
        self.safe = 0
        self.speed = 0
        self.limit = False
        self.image = load_image('./resource/Mini_Mario.gif')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, space_down: Jump},
                Jump: {time_out_to_idle: Idle},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down: Jump},
            }
        )

    def update(self):
        self.state_machine.update()

        self.x = clamp(25.0, self.x, server.background.w - 25.0)
        self.y = clamp(30.0, self.y, server.background.h - 45.0)


    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        if self.life == 1:
            return sx - 30,sy - 30, sx + 20, sy + 20
        if self.life == 2:
            return sx - 30, sy - 30, sx + 20, sy + 65

    def handle_collision(self, group, other):
        if group == 'mario-kill':
            self.safe = 1
        elif group == 'mario-goomba' and self.safe == 0:
            print(self.safe)
            self.life -= 1
            self.safe = 1
            if self.life == 0:
                game_world.remove_object(self)
                game_framework.change_mode(title_mode)
        elif group == 'mario-super_mushroom':
            pass
            #self.life = 2
        elif group == 'mario-box' or group == 'mario-itembox' or group == 'mario-usedbox':
            self.limit = True
        # elif group == 'mario-onbox':
        #     self.y =