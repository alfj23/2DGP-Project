import random
import json
import os

from pico2d import *
import game_framework
import game_world

from player import Player
from map import Map
from pow import Pow
from droptank import Droptank
from barricade import Barricade
from UI import Bottom_UI, Top_UI
name = "MainState"

player = None
map = None
prisoner = None
bottom_ui = None
top_ui = None

droptanks = []
cannonballs = []
droptank_bombs = []
barricade = None

def enter():
    global gold
    gold = 0

    global player
    player = Player()
    game_world.add_object(player, 1)

    global map
    map = Map()
    game_world.add_object(map, 0)

    global bottom_ui
    bottom_ui = Bottom_UI()
    game_world.add_object(bottom_ui, 0)

    global top_ui
    top_ui = Top_UI()
    game_world.add_object(top_ui, 0)

    global prisoner
    prisoner = Pow()
    game_world.add_object(prisoner, 1)

    global droptanks
    droptanks = [Droptank() for i in range(20)]
    game_world.add_objects(droptanks, 1)

    global barricade
    barricade = Barricade()
    game_world.add_object(barricade, 1)


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


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True







