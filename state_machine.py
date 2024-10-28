from sdl2 import SDL_KEYDOWN, SDLK_SPACE

def space_down(event):
    return event[0] == 'INPUT' and event[1].type == SDL_KEYDOWN and event[1].key == SDLK_SPACE

def time_out(event):
    return event[0] == 'TIME_OUT'

class StateMachine:
    def __init__(self, obj):
        self.obj = obj
        self.event_que = []

    def start(self, start_state):
        self.cur_state = start_state

    def update(self):
        self.cur_state.do(self.obj)
        if self.event_que:
            event = self.event_que.pop(0)
            for check_event, next_state in self.transitions[self.cur_state].items():
                if check_event(event):
                    self.cur_state.exit(self.obj)
                    self.cur_state = next_state
                    self.cur_state.entry(self.obj)
                    return

    def draw(self):
        self.cur_state.draw(self.obj)

    def set_transitions(self, transitions):
        self.transitions = transitions

    def add_event(self, event):
        self.event_que.append(event)