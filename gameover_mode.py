from pico2d import *
import game_framework

import game_world
import server
import title_mode
from menu import Menu


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.pop_mode()
            game_framework.change_mode(title_mode)


def init():
    pass

def finish():
    pass


def update():
    game_world.update()
    # delay(0.1)


def draw():
    clear_canvas()
    server.background.draw(400,300)
    game_world.render()
    update_canvas()


def pause():
    pass


def resume():
    pass
