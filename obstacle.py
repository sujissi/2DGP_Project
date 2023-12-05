import random

from pico2d import *

import game_world
import server

def create_obstacle():
    obstacle1 = Obstacle1()
    obstacle2 = Obstacle2()
    bar_list = [Bar() for _ in range(random.randint(1,2))]

    game_world.add_object(obstacle1, 2)
    for bar in bar_list:
        game_world.add_object(bar, 3)
    game_world.add_object(obstacle2, 5)

class Obstacle1:
    def __init__(self):
        self.image = load_image('obstacle_1.png')
        self.w = self.image.w/1.5
        self.h = self.image.h/1.5
        self.x = get_canvas_width()
        self.y = 80

    def draw(self):
        self.image.draw(self.x,self.y,self.w,self.h)

    def update(self):
        self.x -= server.horse.speed
        if self.x+ self.w< 0:
            game_world.remove_object(self)

class Obstacle2:
    def __init__(self):
        self.image = load_image('obstacle_2.png')
        self.w = self.image.w/1.5
        self.h = self.image.h/1.5
        self.x = get_canvas_width()
        self.y = 80
    def draw(self):
        self.image.draw(self.x,self.y,self.w,self.h)

    def update(self):
        self.x -= server.horse.speed
        if self.x+ self.w< 0:
            game_world.remove_object(self)

bar_num = 0
class Bar:
    def __init__(self):
        global bar_num
        self.image = load_image('obstacle_bar.png')
        self.w = self.image.w/1.5
        self.h = self.image.h/1.5
        self.x = get_canvas_width() - 5
        self.y = 80 + bar_num * 20
        if bar_num == 0:
            bar_num = 1
        else:
            bar_num = 0
        self.is_collision = False
    def draw(self):
        self.image.draw(self.x,self.y,self.w,self.h)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.x -= server.horse.speed
        if self.x < get_canvas_width()//3:
            if self.is_collision:
                if self.y > 40:
                    self.x -= 2
                    self.y -= 2
            if collide(self, server.horse):
                if not self.is_collision:
                    server.score.point -= 20
                self.is_collision = True
        elif self.x + self.w < 0:
            game_world.remove_object(self)
        pass
    def get_bb(self):
        return self.x - 5, self.y - 10, self.x + 5, self.y + 10


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True
