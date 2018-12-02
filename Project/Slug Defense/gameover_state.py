import title_state
import main_state
import world_build_state
from pico2d import *


def enter():
    global menu, font, background

    background = load_image('./resource/result/game_over.png')
    menu = load_image('./resource/UI/pause_menu.png')
    font = load_font('./resource/font/ENCR10B.TTF', 18)
    draw()


def exit():
    global menu, font, background
    del menu, font, background
    pass


def update():
    pass


def draw():
   pass


def handle_events():
    pass