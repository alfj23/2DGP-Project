from pico2d import *
import game_framework
import game_world
import main_state
import json


def enter():
    global menu, font
    menu = load_image('./resource/UI/pause_menu.png')
    font = load_font('./resource/font/ENCR10B.TTF', 18)
    pass


def exit():
    pass


def create_stage1():
    pass


def handle_events():
    pass


def update():
    pass


def draw():
    clear_canvas()
    main_state.draw()
    menu.draw(get_canvas_width()//2, get_canvas_height()//2)
    font.draw(380, 385, 'STAGE CLEAR!', (255, 255, 255))
    update_canvas()
    pass