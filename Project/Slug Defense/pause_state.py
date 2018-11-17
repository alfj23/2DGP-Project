import game_framework
from pico2d import *

import main_state

__name__ = "pause_state"

class Pause_menu:
    def __init__(self):
        self.image
        self.font = load_font('ENCR10B.TTF', 30)

    def draw(self):
        pass
    
def enter():
    pass

def exit():
    pass

def update():
    pass

def draw():
    clear_canvas()
    main_state.draw()
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.pop_state()


def pause():
    pass


def resume():
    pass
