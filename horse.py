import math

from pico2d import get_time, load_image, load_font, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT
import game_world
import game_framework


# state event check
# ( state event type, event value )

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def time_out(e):
    return e[0] == 'TIME_OUT'


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
        if horse.frame // 4 == 1:
            horse.action += 1

        horse.image.clip_draw(int(horse.frame) * horse.w, horse.action * horse.h, horse.w, horse.h,
                              horse.x, horse.y, horse.w*1.5, horse.h*1.5)
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
        pass


###################################################
class StateMachine:
    def __init__(self, horse):
        self.horse = horse
        self.cur_state = Idle
        self.transitions = {
            Idle: {space_down: Idle},
            Run: {space_down: Run},
        }

    def start(self):
        self.cur_state.enter(self.horse, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.horse)

        self.horse.frame = (self.horse.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        self.horse.x += self.horse.speed * game_framework.frame_time
        self.horse.y += self.horse.speed * game_framework.frame_time

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

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
