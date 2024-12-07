from pico2d import *
import game_world
import server
from FireFlower import Fireflower
from used_box import UsedBox


class ItemBox:
    image = None
    def __init__(self, name='None', x=0, y=0):
        self.name, self.x, self.y = name, x, y
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
        elif group == 'mario-item_box':
            game_world.remove_object(self)

            used_box = UsedBox(self.x, self.y)
            game_world.add_object(used_box)
            game_world.add_collision_pair('mario-used_box', server.mario, used_box)
            game_world.add_collision_pair('mario-on', server.mario, used_box)

            fireflower = Fireflower(self.x, self.y + 50)
            game_world.add_object(fireflower)
            game_world.add_collision_pair('mario-fireflower', server.mario, fireflower)
