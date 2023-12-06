from pico2d import *
import game_framework

import game_world
import server
import title_mode


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.pop_mode()
            game_framework.change_mode(title_mode)


def init():
    global gameover_text, white_box,score_result, score_result2,text,mode_start_time

    mode_start_time = get_time()
    white_box = load_image('title.png')

    white_box.opacify(200)
    gameover_text = load_font('neodgm.ttf', 90)
    score_result = load_font('neodgm.ttf', 30)
    score_result2 = load_font('neodgm.ttf', 50)
    text = load_font('neodgm.ttf', 20)
    pass

def finish():
    pass


def update():
    game_world.update()
    # delay(0.1)


def draw():
    clear_canvas()
    server.background.draw(server.canvas_cx, server.canvas_cy)
    game_world.render()

    white_box.draw(server.canvas_cx, server.canvas_cy)

    gameover_text.draw(280, 300, 'GAME OVER', (255, 120, 120))
    score_result.draw(server.canvas_cx-50, 240, 'SCORE', (255, 200, 150))
    score_result2.draw(server.canvas_cx-50, 200, f'{server.score_result:03.0f}', (255, 200, 150))
    if (int)(get_time() - mode_start_time) % 2 == 0:
        text.draw(server.canvas_cx - 130, server.canvas_cy-100, '* press space to restart *', (180, 180, 180))
    update_canvas()


def pause():
    pass


def resume():
    pass
