from pico2d import *
import server

class Pipe:
    image = None
    def __init__(self):
        self.name = 'pipe'
        self.x, self.y = 1520, 100
        self.image = load_image('./resource/pipe.png')


    def update(self):
        pass

    def draw(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        self.image.draw(sx, sy, 100, 110)
        draw_rectangle(*self.get_bb())
        draw_rectangle(*self.get_head_box())

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 50 ,sy - 55, sx + 50, sy + 20

    def get_head_box(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 50 ,sy + 21, sx + 50, sy + 55

    def handle_collision(self, group, other):
        pass
