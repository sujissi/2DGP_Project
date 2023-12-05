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
    def draw(self):
        self.image.draw(self.x,self.y,self.w,self.h)

    def update(self):
        # if self.x + self.w//2 <= 0:
        self.x -= server.horse.speed
        if self.x + self.w < 0:
            server.horse.point += 1
            game_world.remove_object(self)
        pass
    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def handle_collision(self, group, other):
        if group == 'horse:bar':
            game_world.remove_object(self)