from pico2d import *
import game_world
import server


class  Fireflower:
    image = None
    def __init__(self, x, y):
        self.name = 'fireflower'
        self.x, self.y = x, y
        if Fireflower.image == None:
            self.image = load_image('./resource/Fireflower.png')

    def update(self):
        pass

    def draw(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        self.image.draw(sx, sy, 50, 50)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 25 ,sy - 25, sx + 25, sy + 25

    def get_head_box(self):
        return 0,0,0,0

    def handle_collision(self, group, other):
        if group == 'mario-fireflower':
            game_world.remove_object(self)