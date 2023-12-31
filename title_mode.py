from pico2d import *
import game_framework

import game_world
import play_mode
import server
from cloud import Cloud
from grass import Grass
from horse import Horse


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(play_mode)


def init():
    global white_box, title_text, title_text2, title_mode_start_time
    running = True

    title_mode_start_time = get_time()

    server.bgm = load_music('Wind Run.mp3')
    server.bgm.set_volume(32)
    server.bgm.repeat_play()

    server.background = load_image('background.PNG')
    white_box = load_image('title.png')
    white_box.opacify(200)
    title_text = load_font('neodgm.ttf', 70)
    title_text2 = load_font('neodgm.ttf', 20)

    cloud_list = [Cloud() for _ in range(2)]
    for cloud in cloud_list:
        game_world.add_object(cloud, 0)

    grass_list = [Grass() for _ in range(4)]
    for grass in grass_list:
        game_world.add_object(grass, 1)

    server.horse = Horse()


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    # delay(0.1)


def draw():
    clear_canvas()
    server.canvas_cx = get_canvas_width() // 2
    server.canvas_cy = get_canvas_height() // 2
    server.background.draw(server.canvas_cx, server.canvas_cy)
    game_world.render()
    white_box.draw(server.canvas_cx, server.canvas_cy)
    title_text.draw(server.canvas_cx - 200, server.canvas_cy + 50, 'I AM HORSE...', (255, 255, 255))
    if (int)(get_time() - title_mode_start_time) % 2 == 0:
        title_text2.draw(server.canvas_cx - 130, server.canvas_cy, '* press space to start *', (180, 180, 180))
    update_canvas()


def pause():
    pass


def resume():
    pass
