from pico2d import *
import game_framework

import game_world
import server
from cloud import Cloud
from grass import Grass
from horse import Horse
from obstacle import Obstacle1, Obstacle2, Bar


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            server.horse.handle_event(event)


def init():
    global image
    running = True

    image = load_image('background.PNG')

    cloud_list = [Cloud() for _ in range(2)]
    for cloud in cloud_list:
        game_world.add_object(cloud, 0)

    grass_list = [Grass() for _ in range(4)]
    for grass in grass_list:
        game_world.add_object(grass, 1)

    obstacle = Obstacle1()
    game_world.add_object(obstacle, 1)

    bar_list = [Bar() for _ in range(2)]
    for bar in bar_list:
        game_world.add_object(bar, 1)

    server.horse = Horse()
    game_world.add_object(server.horse, 2)

    obstacle = Obstacle2()
    game_world.add_object(obstacle, 2)


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
