
import random

from pico2d import *

import server
class Score:
    def __init__(self):
        self.image = load_image('carrot.png')
        self.w = self.image.w//10
        self.h = self.image.h//10
        self.x = 50
        self.y = get_canvas_height() - 50
        self.font = load_font('neodgm.ttf', 25)
        self.point = 0
    def draw(self):
        self.image.draw(self.x,self.y,self.w,self.h)
        self.font.draw(self.x + 25, self.y-5, f'{self.point:02d}', (255, 255, 150))
    def update(self):
        pass
