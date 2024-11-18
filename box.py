from pico2d import *
import game_world


class Box:
    image = None
    num = 0

    def __init__(self):
        self.x, self.y = 250 + self.num, 200
        # if Box.num == 0:
        #     self.num = 100
        if Box.image == None:
            self.image = load_image('box.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y, 50, 48)
        draw_rectangle(*self.get_bb())
        draw_rectangle(*self.get_head_box())

    def get_bb(self):
        return self.x - 25 ,self.y - 24, self.x + 25, self.y

    def get_head_box(self):
        return self.x - 25 ,self.y + 1, self.x + 25, self.y + 25

    def handle_collision(self, group, other):
        if group == 'mario-box':
            game_world.remove_object(self)