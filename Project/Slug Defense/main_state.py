import random
import json
import os

from pico2d import *
import game_framework
import game_world

from player import Player
from grass import Grass
from pow import Pow
from droptank import Droptank
from cannon import Cannon

name = "MainState"

player = None
grass = None
prisoner = None
droptank = None

def enter():
    global player, prisoner, grass, droptank
    player = Player()
    grass = Grass()
    prisoner = Pow()
    droptank = Droptank()
    game_world.add_object(grass, 0) # (변수, 레이어번호)
    game_world.add_object(player, 1)
    game_world.add_object(prisoner, 1)
    game_world.add_object(droptank, 1)


def exit():
    game_world.clear()

def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            player.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()






