from pico2d import *


class UsedBox:
    image = None
    def __init__(self, x, y):
        self.x, self.y = x, y
        if UsedBox.image == None:
            self.image = load_image('used_box.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y, 49, 49)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 25 ,self.y - 24, self.x + 25, self.y + 24

    def handle_collision(self, group, other):
        if group == 'mario-usedbox':
            pass