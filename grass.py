from pico2d import *

import server



class Grass:
    def __init__(self):
        global grass_cnt
        self.image = load_image('grass.PNG')
        self.cw = get_canvas_width()
        self.w = self.image.w/2
        self.h = self.image.h/2
        self.x = self.cw//4 + server.grass_cnt * self.w
        self.y = 50
        server.grass_cnt += 1

    def draw(self):
        self.image.draw(self.x,self.y,self.w,self.h)

    def update(self):
        self.x -= server.horse.speed
        if self.x + self.w/2 < 0:
            self.x = self.cw//4 + (server.grass_cnt-1) * self.w
        pass
