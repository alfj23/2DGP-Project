import game_framework
from pico2d import *


name = "StartState"
image = None
logo_time = 0.0


def enter():
    global image
    image = load_image('kpu_credit.png')


def exit():
    pass


def update():
    pass


def draw():
    pass




def handle_events():
    events = get_events()
    pass


def pause(): pass


def resume(): pass




