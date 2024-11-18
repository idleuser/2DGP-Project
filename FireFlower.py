from pico2d import *
import game_world


class  Fireflower:
    image = None
    def __init__(self, x, y):
        self.x, self.y = x, y
        if Fireflower.image == None:
            self.image = load_image('Fireflower.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y, 50, 50)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 25 ,self.y - 25, self.x + 25, self.y + 25

    def handle_collision(self, group, other):
        if group == 'mario-fireflower':
            game_world.remove_object(self)