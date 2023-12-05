
import random

from pico2d import *

import server
class Rider:
    def __init__(self):
        self.image = load_image('word_balloon.png')
        self.w = self.image.w*1.2
        self.h = self.image.h*1.2
        self.x = get_canvas_width()//2 - 200
        self.y = get_canvas_height()//2 -30
        self.font = load_font('neodgm.ttf', 30)
        self.point = 0
    def draw(self):
        self.image.draw(self.x,self.y,self.w,self.h)
        self.font.draw(self.x-15, self.y+10, 'GO!', (0, 0, 0))
    def update(self):
        pass
