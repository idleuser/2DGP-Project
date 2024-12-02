from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT

def start_event(event):
    return event[0] == 'START'

def space_down(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_SPACE

def time_out_to_idle(event):
    return event[0] == 'TIME_OUT'

def right_down(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_RIGHT

def right_up(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYUP and event[1].key == SDLK_RIGHT

def left_down(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_LEFT

def left_up(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYUP and event[1].key == SDLK_LEFT


class StateMachine:
    def __init__(self, obj):
        self.obj = obj
        self.event_que = []

    def start(self, start_state):
        self.cur_state = start_state
        self.cur_state.enter(self.obj, ('START', 0))

    def update(self):
        self.cur_state.do(self.obj)
        if self.event_que:
            event = self.event_que.pop(0)
            self.handle_event(event)

    def draw(self):
        self.cur_state.draw(self.obj)

    def set_transitions(self, transitions):
        self.transitions = transitions

    def add_event(self, event):
        self.event_que.append(event)

    def handle_event(self, e):
        for event, next_state in self.transitions[self.cur_state].items():
            if event(e):
                print(f'Exit from {self.cur_state}')
                self.cur_state.exit(self.obj, e)
                self.cur_state = next_state
                print(f'Enter into {self.cur_state}')
                self.cur_state.enter(self.obj, e)
                return