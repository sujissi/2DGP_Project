from pico2d import get_time, load_image, load_font, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT
import game_world
import game_framework


# state event check
# ( state event type, event value )

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def time_out(e):
    return e[0] == 'TIME_OUT'


################################################

class Idle:

    @staticmethod
    def enter(boy, e):
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        pass

    @staticmethod
    def draw(boy):
        pass


###################################################
class StateMachine:
    def __init__(self, horse):
        self.horse = horse
        self.cur_state = Idle
        self.transitions = {
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
        self.x, self.y = 400, 90
        self.frame = 0
        self.action = 3
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
