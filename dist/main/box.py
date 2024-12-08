from pico2d import *
import game_world
import server


class Box:
    image = None

    def __init__(self, name='None', x=0, y=0):
        self.name, self.x, self.y = name, x, y
        if Box.image == None:
            self.image = load_image('./resource/box.png')

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
        self.image.draw(sx, sy, 50, 48)
        #draw_rectangle(*self.get_bb())
        #draw_rectangle(*self.get_head_box())

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 25 ,sy - 24, sx + 25, sy

    def get_head_box(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 25 ,sy + 1, sx + 25, sy + 25

    def handle_collision(self, group, other):
        if group == 'mario-on':
            return
        elif group == 'mario-box':
            game_world.remove_object(self)
