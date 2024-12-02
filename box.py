from pico2d import *
import game_world
import server


class Box:
    image = None
    num = 0

    def __init__(self):
        self.x, self.y = 250 + self.num, 200
        # if Box.num == 0:
        #     self.num = 100
        if Box.image == None:
            self.image = load_image('./resource/box.png')

    def update(self):
        pass

    def draw(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        self.image.draw(sx, sy, 50, 48)
        draw_rectangle(*self.get_bb())
        draw_rectangle(*self.get_head_box())

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 25 ,sy - 24, sx + 25, sy

    def get_head_box(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 25 ,sy + 1, sx + 25, sy + 25

    def handle_collision(self, group, other):
        if group == 'mario-box':
            game_world.remove_object(self)
