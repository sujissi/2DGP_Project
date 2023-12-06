from pico2d import *
import game_framework

import game_world
import server
import stop_mode
import title_mode
from cloud import Cloud
from grass import Grass
from horse import Horse
from rider import Rider
from score import Score


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_TAB:
            game_framework.push_mode(stop_mode)
        else:
            server.horse.handle_event(event)


def init():
    running = True

    cloud_list = [Cloud() for _ in range(2)]
    for cloud in cloud_list:
        game_world.add_object(cloud, 0)

    grass_list = [Grass() for _ in range(4)]
    for grass in grass_list:
        game_world.add_object(grass, 1)

    server.score = Score()
    game_world.add_object(server.score, 0)

    server.rider = Rider()
    game_world.add_object(server.rider, 0)

    server.horse = Horse()
    game_world.add_object(server.horse, 4)



def finish():
    game_world.clear()
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
    server.stop_state = True
    server.horse.speed =0
    pass


def resume():
    server.stop_state = False
    server.horse.idle_start_time = get_time()
    pass
