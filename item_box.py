from pico2d import *
import game_world
from FireFlower import Fireflower
from used_box import UsedBox


class ItemBox:
    image = None
    def __init__(self):
        self.x, self.y = 200, 200
        if ItemBox.image == None:
            self.image = load_image('item_box.png')

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
        if group == 'mario-itembox':
            game_world.remove_object(self)
            usedbox = UsedBox(self.x, self.y)
            game_world.add_object(usedbox)
            # game_world.add_collision_pair('mario-usedbox', None, usedbox)
            fireflower = Fireflower(self.x, self.y + 50)
            game_world.add_object(fireflower)
            # game_world.add_collision_pair('mario-fireflower', None, fireflower)

            # handle_collision으로 반복문에서 딕셔너리를 사용하고 있는데, 딕셔너리에 추가할 수 없는 문제
