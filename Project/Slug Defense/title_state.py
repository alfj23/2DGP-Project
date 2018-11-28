import game_framework
from pico2d import *
import main_state
import world_build_state

__name__ = "TitleState"
image = None


def enter():
    global image
    image = load_image('./resource/title/title.png')


def exit():
    global image
    del(image)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                world_build_state.create_stage1()  # 게임 시작시 스테이지 1 생성
                game_framework.change_state(main_state)


def draw():
    clear_canvas()
    image.draw(800//2, 600//2)
    update_canvas()


def update():
    pass


def pause():
    pass


def resume():
    pass






