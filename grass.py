from pico2d import *

grass_cnt = 0

class Grass:
    def __init__(self):
        global grass_cnt
        self.image = load_image('grass.PNG')
        self.cw = get_canvas_width()
        self.w = self.image.w//2
        self.h = self.image.h//2
        self.x = self.cw//4 + grass_cnt * self.w
        self.y = 50
        grass_cnt += 1
    def draw(self):
        self.image.draw(self.x,self.y,self.w,self.h)

    def update(self):
        if self.x + self.w//2 < 0:
            self.x = self.cw + self.w
        self.x -= 1
        # 말이 이동해야 하는 만큼 x 위치 이동
        pass
