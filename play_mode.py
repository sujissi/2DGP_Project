from pico2d import *
import game_framework

import game_world
from grass import Grass
from cloud import Cloud
from horse import Horse


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            horse.handle_event(event)


def init():
    global cloud
    global grass
    global horse
    global image
    running = True

    image = load_image('background.PNG')

    cloud = Cloud()
    game_world.add_object(cloud, 0)

    grass = Grass()
    game_world.add_object(grass, 1)

    horse = Horse()
    game_world.add_object(horse, 2)


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    # delay(0.1)


def draw():
    clear_canvas()
    image.draw(400,300)
    game_world.render()
    update_canvas()


def pause():
    pass


def resume():
    pass
