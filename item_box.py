from pico2d import *
import game_world
import server
from FireFlower import Fireflower
from used_box import UsedBox


class ItemBox:
    image = None
    def __init__(self):
        self.name = 'item_box'
        self.x, self.y = 200, 200
        if ItemBox.image == None:
            self.image = load_image('./resource/item_box.png')

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
        if group == 'mario-on':
            return
        elif group == 'mario-itembox':
            usedbox = UsedBox(self.x, self.y)
            game_world.remove_object(self)
            game_world.add_object(usedbox)
            game_world.add_collision_pair('mario-usedbox', server.mario, usedbox)
            game_world.add_collision_pair('mario-on', server.mario, usedbox)
            fireflower = Fireflower(self.x, self.y + 50)
            game_world.add_object(fireflower)
            game_world.add_collision_pair('mario-fireflower', server.mario, fireflower)

            # handle_collision으로 반복문에서 딕셔너리를 사용하고 있는데, 딕셔너리에 추가할 수 없는 문제
