import random

from pico2d import *

import server


class Cloud:
    def __init__(self):
        self.image = load_image('cloud.PNG')
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.image.w*1.5
        self.h = self.image.h*1.5
        self.x = self.cw//2 + server.cloud_cnt * self.w
        self.y = self.ch//2
        server.cloud_cnt += 1
    def draw(self):
        self.image.draw(self.x,self.y,self.w,self.h)

    def update(self):
        if self.x + self.w//2 <= 0:
            self.x = self.cw//2 + self.w
        self.x -= server.horse.speed * 0.2 + 0.1
        # self.x -= 0.1*random.randint(4,8)
        pass
