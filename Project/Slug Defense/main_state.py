import random
import json
import os

from pico2d import *
import game_framework
import game_world
import pause_state
import world_build_state

from player import Player
from map import Map
from pow import Pow
from droptank import Droptank
from barricade import Barricade
from UI import Bottom_UI, Top_UI
from rebel_soldier import Soldier
from store import Store

__name__ = "MainState"

player = None
map = None
prisoner = None
bottom_ui = None
top_ui = None
store = None
#droptanks = []
#soldiers = []
barricade = None




def enter():
    global store
    store = Store()

    global gold
    gold = 3000

    global bottom_ui
    bottom_ui = Bottom_UI()
    game_world.add_object(bottom_ui, 2)

    global top_ui
    top_ui = Top_UI()
    game_world.add_object(top_ui, 2)

    global player, prisoner, barricade, map, left_wave_amount
    map = world_build_state.get_map()
    player = world_build_state.get_player()
    prisoner = world_build_state.get_prisoner()
    barricade = world_build_state.get_barricade()
    left_wave_amount = len(world_build_state.droptanks) + len(world_build_state.soldiers)
    '''
    global player
    player = Player()
    game_world.add_object(player, 1)

    global map
    map = Map()
    game_world.add_object(map, 0)

    

    global prisoner
    prisoner = Pow()
    game_world.add_object(prisoner, 1)
    prisoner.set_background(map)

    #global droptanks
    #droptanks = [Droptank() for i in range(5)]
    #game_world.add_objects(droptanks, 1)
    #for droptank in droptanks:
        #droptank.set_background(map)

    #global soldiers
    #soldiers = [Soldier() for i in range(20)]
    #game_world.add_objects(soldiers, 1)
    #for soldier in soldiers:
        #soldier.set_background(map)

    global barricade
    barricade = Barricade()
    game_world.add_object(barricade, 1)
    barricade.set_background(map)

    #global left_wave_amount
    #left_wave_amount = len(droptanks) + len(soldiers)

    map.set_center_object(player)
    player.set_background(map)

    
'''


def exit():
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    global left_wave_amount
    global prisoner
    events = get_events()
    for event in events:
        if left_wave_amount == 0:
            game_framework.change_state(world_build_state)
        if prisoner.hp_amount < 0:
            print("state fail!")
            #game_framework.change_state(gameover_state)
            pass

        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.push_state(pause_state)
        else:
            player.handle_event(event)
            store.handle_event(event)


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







