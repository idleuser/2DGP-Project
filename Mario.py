from pico2d import load_image

class Mini_Mario:
    def __init__(self):
        self.x, self.y = 100, 90
        self.frame = 0
        self.image = load_image('mini_mario_stand.gif')
    def update(self):
        self.frame = (self.frame + 1) % 3
    def draw(self):
        self.image.clip_draw((self.frame + 8) * 19, 9 * 24, 19, 24, self.x, self.y, 50, 50)