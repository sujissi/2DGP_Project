import math
import random

from pico2d import get_time, load_image, load_font, clamp, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_UP, SDLK_DOWN, SDL_KEYUP, SDLK_SPACE, SDLK_a, SDLK_d

import game_world
import game_framework
import server
from obstacle import create_obstacle


# state event check
# ( state event type, event value )

def upkey_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP


def upkey_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP

def downkey_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN


def downkey_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def akey_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

# def akey_up(e):
#     return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a

def dkey_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d

# def dkey_up(e):
#     return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d

def time_out(e):
    return e[0] == 'TIME_OUT'

def jump_stop(e):
    return e[0] == 'JUMP_STOP'
def jump_jump(e):
    return e[0] == 'JUMP_JUMP'

# Action Speed
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2


################################################
class Idle:

    @staticmethod
    def enter(horse, e):
        horse.speed = 0

        pass

    @staticmethod
    def exit(horse, e):
        pass

    @staticmethod
    def do(horse):
        pass

    @staticmethod
    def draw(horse):
        horse.image.clip_draw(int(horse.frame) * horse.w, horse.action * horse.h, horse.w, horse.h,
                              horse.x, horse.y, horse.w * 1.5, horse.h * 1.5)
        pass


class Run:
    @staticmethod
    def enter(horse, e):
        server.score.point += 5
        horse.action = 0
        horse.speed = 4
        horse.run_time = get_time()
        if random.randint(1,5) == 1:
            create_obstacle()
        pass

    @staticmethod
    def exit(horse, e):
        pass

    @staticmethod
    def do(horse):
        horse.frame = (horse.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        if get_time() - horse.run_time > 0.1:
            horse.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(horse):
        if horse.frame // 4 == 1:
            horse.action += 1

        horse.image.clip_draw(int(horse.frame) * horse.w, horse.action * horse.h, horse.w, horse.h,
                              horse.x, horse.y, horse.w * 1.5, horse.h * 1.5)
        pass


class Jump:
    @staticmethod
    def enter(horse, e):
        horse.speed = 3
        horse.jump_dest = 200
        horse.jump_dist = 1
        horse.rad_d = 10
        if random.randint(1,5) == 1:
            create_obstacle()
        pass

    @staticmethod
    def exit(horse, e):
        pass

    @staticmethod
    def do(horse):
        if horse.y > 150:
            horse.action = 3
        elif horse.jump_dist < 0:
            if horse.y > 140:
                horse.action = 2
            elif horse.y > 130:
                horse.action = 1
            elif horse.y <= 120:
                horse.action = 0
                horse.jump_dist = -horse.jump_dist
                horse.jump_cnt = 0
                horse.state_machine.handle_event(('JUMP_STOP', 0))
        pass

    @staticmethod
    def draw(horse):
        horse.y += horse.jump_dist
        if horse.rad_d > 5:
            horse.rad_d -= 0.01
        if horse.rad_d < 0:
            horse.rad_d += 0.01
        if horse.y >= horse.jump_dest:
            horse.jump_dist = -horse.jump_dist
            horse.rad_d = -horse.rad_d*2
        horse.image.clip_composite_draw(int(horse.jump_frame) * horse.w, horse.action * horse.h, horse.w, horse.h,
                                        3.141592 / horse.rad_d, '', horse.x, horse.y, horse.w * 1.5, horse.h * 1.5)
        pass

class JumpJump:
    @staticmethod
    def enter(horse, e):
        horse.jump_dest = 250
        horse.jump_dist = 1.2
        horse.speed *= 0.8
        pass

    @staticmethod
    def exit(horse, e):
        pass

    @staticmethod
    def do(horse):
        if horse.y > 200:
            horse.action = 3
        elif horse.jump_dist < 0:
            if horse.y > 150:
                horse.action = 2
            elif horse.y > 130:
                horse.action = 1
            elif horse.y <= 120:
                horse.action = 0
                horse.jump_dist = -horse.jump_dist
                horse.jump_cnt = 0
                horse.state_machine.handle_event(('JUMP_STOP', 0))
        pass

    @staticmethod
    def draw(horse):
        horse.y += horse.jump_dist
        if horse.rad_d > 5:
            horse.rad_d -= 0.01
        if horse.rad_d < 0:
            horse.rad_d += 0.01
        if horse.y >= horse.jump_dest:
            horse.jump_dist = -horse.jump_dist
            horse.rad_d = -horse.rad_d*2
        horse.image.clip_composite_draw(int(horse.jump_frame) * horse.w, horse.action * horse.h, horse.w, horse.h,
                              3.141592/horse.rad_d,'',horse.x, horse.y, horse.w * 1.5, horse.h * 1.5)
        pass


###################################################
class StateMachine:
    def __init__(self, horse):
        self.horse = horse
        self.cur_state = Idle
        self.transitions = {
            Idle: {space_down: Jump, jump_stop: Run,akey_down:Run,dkey_down:Run },
            Run: {space_down: Jump, jump_stop: Run,akey_down:Run,dkey_down:Run,time_out:Idle },
            Jump: {space_down: JumpJump,jump_stop: Idle},
            JumpJump: {space_down: JumpJump,jump_stop: Idle},
        }

    def start(self):
        self.cur_state.enter(self.horse, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.horse)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.horse, e)
                self.cur_state = next_state
                self.cur_state.enter(self.horse, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.horse)


##################################################
class Horse:
    def __init__(self):
        self.image = load_image('horse_with_rider.png')
        self.w, self.h = 146, 106
        self.x, self.y = 220, 120
        self.frame = 2
        self.action = 2
        self.state_machine = StateMachine(self)
        self.state_machine.start()

        self.jump_cnt = 0
        self.jump_dist = 1
        self.jump_dest = 200
        self.jump_frame = 2

        self.rad_d = 0
        self.speed = 0

        self.last_key = None

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_a:
                if self.last_key == 'a': return
                self.last_key = 'a'
            elif event.key == SDLK_d:
                if self.last_key == 'd': return
                self.last_key = 'd'
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        # draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - (self.w/2 -30), self.y - (self.w/2 -20), self.x + (self.w/2 -30), self.y # -> 값 4개짜리 튜플 한개
