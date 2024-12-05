from pico2d import *

import server


class UsedBox:
    image = None
    def __init__(self, x, y):
        self.name = 'used_box'
        self.x, self.y = x, y
        if UsedBox.image == None:
            self.image = load_image('./resource/used_box.png')

    def update(self):
        pass

    def draw(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        self.image.draw(sx, sy, 49, 49)
        draw_rectangle(*self.get_bb())
        draw_rectangle(*self.get_head_box())

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 25 ,sy - 24, sx + 25, sy

    def get_head_box(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 25 ,sy + 1, sx + 25, sy + 24

    def handle_collision(self, group, other):
        if group == 'mario-on':
            return
        elif group == 'mario-usedbox':
            pass
