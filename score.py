
import random

from pico2d import *

import server
class Score:
    def __init__(self):
        self.carrot_image = load_image('carrot.png')
        self.whip_image = load_image('whip.png')
        self.w = self.carrot_image.w // 12
        self.h = self.carrot_image.h // 12
        self.x = 50
        self.y = get_canvas_height() - 50
        self.current_score = load_font('neodgm.ttf', 20)
        self.current_whip = load_font('neodgm.ttf', 20)
        self.minus_point = 0
        self.score = 0
        self.whip_cnt = 5
    def draw(self):
        self.carrot_image.draw(self.x, self.y, self.w, self.h)
        self.current_score.draw(self.x + 25, self.y - 5, f'SCORE {self.score:.0f}', (255, 200, 150))
        self.whip_image.draw(self.x-5, self.y-30, self.whip_image.w//5, self.whip_image.h//5)
        self.current_whip.draw(self.x + 25, self.y - 30, f'WHIP {self.whip_cnt}', (200, 200, 200))
    def update(self):
        if self.minus_point < -10:
            self.score += self.minus_point
            self.minus_point = 0
        pass
