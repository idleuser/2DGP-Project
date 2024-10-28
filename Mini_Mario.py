from pico2d import load_image, get_time
from state_machine import StateMachine, space_down, time_out


class Idle:
    @staticmethod
    def entry(obj):
        obj.frame = 0
    @staticmethod
    def do(obj):
        obj.frame = (obj.frame + 1) % 3
    @staticmethod
    def exit(obj):
        pass
    @staticmethod
    def draw(obj):
        obj.image.clip_draw((obj.frame + 8) * 19, 9 * 24, 19, 24, obj.x, obj.y, 60, 60)

class Jump:
    @staticmethod
    def entry(obj):
        obj.frame = 0
        obj.dir = 0
        obj.limit = False
        obj.time = get_time()
    @staticmethod
    def do(obj):
        if get_time() - obj.time > 0.6:
            obj.state_machine.add_event(('TIME_OUT', 0))
        obj.frame = (obj.frame + 1) % 6
        if obj.y >= 270:
            obj.limit = True
        if obj.y < 270 and obj.limit == False:
            obj.y += 60
        elif obj.y > 90:
            obj.y -= 60
    @staticmethod
    def exit(obj):
        pass
    @staticmethod
    def draw(obj):
        obj.image.clip_draw((obj.frame + 8) * 19, 6 * 24, 19, 24, obj.x, obj.y, 60, 60)

class Mini_Mario:
    def __init__(self):
        self.x, self.y = 100, 90
        self.frame = 0
        self.dir = 0
        self.image = load_image('mini_mario.gif')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {space_down: Jump},
                Jump: {time_out: Idle}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.add_event(
            ('INPUT', event)
        )

    def draw(self):
        self.state_machine.draw()