import math

from pico2d import get_time, load_image, load_font, clamp
from sdl2 import SDL_KEYDOWN, SDLK_UP, SDLK_DOWN, SDL_KEYUP, SDLK_SPACE

import game_world
import game_framework


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

def jump_stop(e):
    return e[0] == 'JUMP_STOP'

def jump_jump(e):
    return e[0] == 'JUMP_JUMP'

# Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Action Speed
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


################################################
class Idle:

    @staticmethod
    def enter(horse, e):
        pass

    @staticmethod
    def exit(horse, e):
        pass

    @staticmethod
    def do(horse):
        pass

    @staticmethod
    def draw(horse):
        if horse.frame // 4 == 1:
            horse.action += 1

        horse.image.clip_draw(int(horse.frame) * horse.w, horse.action * horse.h, horse.w, horse.h,
                              horse.x, horse.y, horse.w * 1.5, horse.h * 1.5)
        pass


class Run:

    @staticmethod
    def enter(horse, e):
        pass

    @staticmethod
    def exit(horse, e):
        pass

    @staticmethod
    def do(horse):
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
        print("jump")
        horse.jump_dest = 200
        pass

    @staticmethod
    def exit(horse, e):
        pass

    @staticmethod
    def do(horse):
        if horse.jump_dist < 0 and horse.y <= 120:
            horse.jump_dist = -horse.jump_dist
            horse.jump_cnt = 0
            horse.state_machine.handle_event(('JUMP_STOP', 0))
        pass

    @staticmethod
    def draw(horse):
        horse.y += horse.jump_dist
        if horse.y >= horse.jump_dest:
            horse.jump_dist = -horse.jump_dist
        horse.image.clip_draw(int(horse.frame) * horse.w, horse.action * horse.h, horse.w, horse.h,
                              horse.x, horse.y, horse.w * 1.5, horse.h * 1.5)
        pass

class JumpJump:
    @staticmethod
    def enter(horse, e):
        print("jumpjump")
        horse.jump_dest = 250
        pass

    @staticmethod
    def exit(horse, e):
        pass

    @staticmethod
    def do(horse):
        if horse.jump_dist < 0 and horse.y <= 120:
            horse.jump_dist = -horse.jump_dist
            horse.jump_cnt = 0
            horse.state_machine.handle_event(('JUMP_STOP', 0))
        pass

    @staticmethod
    def draw(horse):
        horse.y += horse.jump_dist
        if horse.y >= horse.jump_dest:
            horse.jump_dist = -horse.jump_dist
        horse.image.clip_draw(int(horse.frame) * horse.w, horse.action * horse.h, horse.w, horse.h,
                              horse.x, horse.y, horse.w * 1.5, horse.h * 1.5)
        pass


###################################################
class StateMachine:
    def __init__(self, horse):
        self.horse = horse
        self.cur_state = Idle
        self.transitions = {
            Idle: {space_down: Jump, jump_stop: Run,upkey_down:Run,upkey_up:Run,downkey_down:Run ,downkey_up:Run },
            Run: {space_down: Jump, jump_stop: Run,upkey_down:Run,upkey_up:Run,downkey_down: Run,downkey_up:Run },
            Jump: {space_down: JumpJump,jump_stop: Run},
            JumpJump: {space_down: JumpJump,jump_stop: Run},
        }

    def start(self):
        self.cur_state.enter(self.horse, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.horse)

        self.horse.frame = (self.horse.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        # self.horse.x += self.horse.speed * game_framework.frame_time
        # self.horse.y += self.horse.speed * game_framework.frame_time

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
        self.x, self.y = 200, 120
        self.frame = 0
        self.action = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.speed = 0

        self.jump_cnt = 0
        self.jump_dist = 0.5
        self.jump_dest = 200

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
