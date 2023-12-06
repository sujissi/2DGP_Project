
import random

from pico2d import *

import server
from horse import Jump, JumpJump


class Rider:
    def __init__(self):
        self.image = load_image('word_balloon.png')
        self.w = self.image.w*1.2
        self.h = self.image.h*1.2
        self.x = get_canvas_width()//2 - 250
        self.y = get_canvas_height()//2 - 30
        self.font = load_font('neodgm.ttf', 30)
        self.minus_font = load_font('neodgm.ttf', 20)
        self.wait_time = 2
        self.say_stop_time = 0
        self.punish_state = False
        self.say_state = 'go'
        self.is_use_whip = False
    def draw(self):
        self.say()
        if self.punish_state:
            self.minus_font.draw(server.horse.x - 50, server.horse.y + 50, '-10', (150, 100, 100))
    def update(self):
        self.wait_time = get_time() - server.horse.idle_start_time
        self.check_use_whip()
        pass
    def say(self):
        # if server.horse.state_machine.cur_state == Jump: return
        # if server.horse.state_machine.cur_state == JumpJump: return

        if self.wait_time > 3:
            self.image.draw(self.x,self.y,self.w,self.h)
            self.font = load_font('neodgm.ttf', 30)
            self.font.draw(self.x - 15, self.y + 10, 'GO!', (0, 0, 0))
            self.say_state = 'go'
            if self.wait_time > 3:
                server.score.minus_point -= 0.2
                self.punish_state = True
            else:
                self.punish_state = False
        if server.horse.run_cnt > 30:
            self.image.draw(self.x, self.y, self.w, self.h)
            self.font = load_font('neodgm.ttf', 28)
            self.font.draw(self.x - 25, self.y + 10, 'STOP', (0, 0, 0))
            self.say_state = 'stop'
            if self.wait_time > 1:
                server.horse.run_cnt = 0
                self.punish_state = False
            else:
                server.score.minus_point -= 0.2
                if not self.punish_state:
                    self.say_stop_time = get_time()
                self.punish_state = True


    def check_use_whip(self):
       if self.punish_state:
           if self.say_state =='go' and self.wait_time < 5: return
           if self.say_state =='stop' and get_time() - self.say_stop_time < 2: return
           if self.is_use_whip: return

           self.is_use_whip = True
           server.score.whip_cnt -= 1
       elif not self.punish_state:
               self.is_use_whip = False


