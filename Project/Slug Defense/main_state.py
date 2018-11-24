import random
import json
import os

from pico2d import *
import game_framework
import game_world
import pause_state

from player import Player
from map import Map
from pow import Pow
from droptank import Droptank
from barricade import Barricade
from UI import Bottom_UI, Top_UI
from rebel_soldier import Soldier
__name__ = "MainState"

player = None
map = None
prisoner = None
bottom_ui = None
top_ui = None

droptanks = []
soldiers = []
cannonballs = []
droptank_bombs = []
barricade = None

global gold
gold = 3000


def enter():
    global player
    player = Player()
    game_world.add_object(player, 1)

    global map
    map = Map()
    game_world.add_object(map, 0)

    global bottom_ui
    bottom_ui = Bottom_UI()
    game_world.add_object(bottom_ui, 2)

    global top_ui
    top_ui = Top_UI()
    game_world.add_object(top_ui, 2)

    global prisoner
    prisoner = Pow()
    game_world.add_object(prisoner, 1)
    prisoner.set_background(map)

    global droptanks
    droptanks = [Droptank() for i in range(20)]
    game_world.add_objects(droptanks, 1)

    global soldiers
    soldiers = [Soldier() for i in range(20)]
    game_world.add_objects(soldiers, 1)

    global barricade
    barricade = Barricade()
    game_world.add_object(barricade, 1)
    barricade.set_background(map)

    global left_wave_amount
    left_wave_amount = len(droptanks) + len(soldiers)

    map.set_center_object(player)
    player.set_background(map)


def exit():
    game_world.clear()


def pause():
    pass


def resume():
    pass


global cost_ATK, cost_HP, cost_BRCD_RP, cost_BRCD_HP, cost_SK
cost_ATK, cost_HP, cost_BRCD_RP, cost_BRCD_HP, cost_SK = 100, 100, 300, 100, 300


def handle_events():
    global gold
    global cost_ATK, cost_HP, cost_BRCD_RP, cost_BRCD_HP, cost_SK, chk_barricade_alive
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.push_state(pause_state)

        elif event.type == SDL_KEYDOWN and event.key == SDLK_1:  # 키입력으로 상점 상호작용 처리.
            # 플레이어 공격력 증가
            if gold - cost_ATK >= 0:
                gold -= cost_ATK
                player.damage_amount_of_cannon += 50
                cost_ATK = cost_ATK * 2
            pass
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            # 플레이어 최대 체력 증가
            if gold - cost_HP >= 0:
                gold -= cost_HP
                player.max_hp += 200
                player.hp_amount = player.hp_rate * player.max_hp
                cost_HP = cost_HP * 2
            pass
        elif event.type == SDL_KEYDOWN and event.key == SDLK_3:
            # 바리게이트 수리
            if (gold - cost_BRCD_RP) >= 0 and 0 < barricade.hp_amount < barricade.max_hp:
                gold -= cost_BRCD_RP
                barricade.hp_amount = barricade.max_hp
                cost_BRCD_RP = cost_BRCD_RP * 2
            elif (gold - cost_BRCD_RP) >= 0 and not barricade.chk_alive:
                barricade.chk_alive = True
                gold -= cost_BRCD_RP
                barricade.hp_amount = barricade.max_hp
                cost_BRCD_RP = cost_BRCD_RP * 2
            pass
        elif event.type == SDL_KEYDOWN and event.key == SDLK_4:
            if gold - cost_BRCD_HP >= 0:
                gold -= cost_BRCD_HP
                barricade.max_hp += 200
                barricade.hp_amount = barricade.hp_rate * barricade.max_hp
                cost_BRCD_HP = cost_BRCD_HP * 2
            pass
        elif event.type == SDL_KEYDOWN and event.key == SDLK_5:
            # 스킬 데미지 업그레이드 ==> 현재 스킬 미구현으로 업그레이드 또한 미구현
            pass

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







