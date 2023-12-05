from pico2d import *

import game_world
import server


class Obstacle1:
    def __init__(self):
        self.image = load_image('obstacle_1.png')
        self.w = self.image.w/1.5
        self.h = self.image.h/1.5
        self.x = get_canvas_width()//4
        self.y = 70
    def draw(self):
        self.image.draw(self.x,self.y,self.w,self.h)

    def update(self):
        # if self.x + self.w//2 <= 0:
        self.x -= server.horse.speed * 1

class Obstacle2:
    def __init__(self):
        self.image = load_image('obstacle_2.png')
        self.w = self.image.w/1.5
        self.h = self.image.h/1.5
        self.x = get_canvas_width()//4
        self.y = 70
    def draw(self):
        self.image.draw(self.x,self.y,self.w,self.h)

    def update(self):
        # if self.x + self.w//2 <= 0:
        self.x -= server.horse.speed * 1
bar_cnt = 0
class Bar:
    def __init__(self):
        global bar_cnt
        self.image = load_image('obstacle_bar.png')
        self.w = self.image.w/1.5
        self.h = self.image.h/1.5
        self.x = get_canvas_width()//4 - 5
        self.y = 70 + bar_cnt * 20
        bar_cnt += 1
    def draw(self):
        self.image.draw(self.x,self.y,self.w,self.h)

    def update(self):
        # if self.x + self.w//2 <= 0:
        self.x -= server.horse.speed * 1
        pass
    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def handle_collision(self, group, other):
        if group == 'horse:bar':
            game_world.remove_object(self)