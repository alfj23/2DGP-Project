import title_state
import main_state
import game_framework
import world_build_state
from pico2d import *


def enter():
    global font, background, bgm
    background = load_image('./resource/result/game_over.png')
    font = load_font('./resource/font/ENCR10B.TTF', 18)
    bgm = load_music('./resource/sounds/gameover.mp3')
    bgm.set_volume(64)
    bgm.play(1)
    draw()


def exit():
    global font, background
    del font, background
    pass


def update():
    pass


def draw():
    clear_canvas()
    background.draw(get_canvas_width() // 2, get_canvas_height() // 2)
    font.draw(get_canvas_width() // 3 - 100, 520, 'STAGE FAILED!', (255, 0, 0))
    font.draw(get_canvas_width() // 3 - 100, 480, 'R REPLAY STAGE', (255, 255, 255))
    font.draw(get_canvas_width() // 3 - 100, 435, 'ESC BACK TO TITLE', (255, 255, 255))
    update_canvas()
    pass


def handle_events():
    global bgm
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_r):  # 현 스테이지 다시 시작.
                if main_state.cleared_stage_count == 1:
                    world_build_state.build_stage1()
                elif main_state.cleared_stage_count == 2:
                    world_build_state.build_stage2()
                elif main_state.cleared_stage_count == 3:
                    world_build_state.build_stage3()
                elif main_state.cleared_stage_count == 4:
                    world_build_state.build_stage4()
                elif main_state.cleared_stage_count == 5:
                    world_build_state.build_stage5()
                bgm.stop()
                game_framework.change_state(main_state)

            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):  # 타이틀로 이동.
                main_state.cleared_stage_count = 0
                game_framework.change_state(title_state)

    pass