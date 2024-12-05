import server
from pico2d import *

class Title_background:
    def __init__(self):
        self.image = load_image('./resource/title.png')
        self.bgm = load_music('bgm/Title.mp3')
        self.bgm.set_volume(32)
        self.bgm.repeat_play()

    def draw(self):
        clear_canvas()
        self.image.draw(800 / 2, 500 / 2)
        update_canvas()

    def update(self):
        pass

    def handle_event(self, event):
        pass

class Background:
    def __init__(self):
        self.image = load_image('./resource/stage_1.png')
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h
        self.bgm = load_music('bgm/World1.mp3')
        self.bgm.set_volume(32)
        self.bgm.repeat_play()

    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)

    def update(self):
        self.window_left = clamp(0, int(server.mario.x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(server.mario.y) - self.ch // 2, self.h - self.ch - 1)

    def handle_event(self, event):
        pass