from pico2d import *
import game_world
import server

class SteppingStone:
    image = None
    def __init__(self, name='None', x=0, y=0):
        self.name, self.x, self.y = name, x, y
        if SteppingStone.image == None:
            self.image = load_image('./resource/steppingstone.png')

    def __getstate__(self):
        info = {'name': self.name, 'x':self.x, 'y': self.y}
        return info

    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)

    def update(self):
        pass

    def draw(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        self.image.draw(sx, sy, 80, 30)
        #draw_rectangle(*self.get_head_box())

    def get_bb(self):
        return 0,0,0,0

    def get_head_box(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 30 ,sy - 15, sx + 30, sy + 15

    def handle_collision(self, group, other):
        pass