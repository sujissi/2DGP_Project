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
        elif event.type == SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_1:
                    game_framework.pop_mode()
                case pico2d.SDLK_2:
                    game_framework.pop_mode()
                    game_framework.change_mode(title_mode)
                case pico2d.SDLK_3:
                    game_framework.quit()


def init():
    global menu
    menu = Menu()
    game_world.add_object(menu,6)



def finish():
    game_world.remove_object(menu)
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
