from pico2d import *
import game_framework
import game_world
import main_state
import title_state
import json

from player import Player
from map import Map
from pow import Pow
from droptank import Droptank
from barricade import Barricade
from rebel_soldier import Soldier

__name__ = "world_build_state"

player = None
barricade = None
prisoner = None
map = None

droptanks = []
soldiers = []

menu = None
font = None

def enter():
    global font, background, bgm

    background = load_image('./resource/result/mission_complete.png')
    font = load_font('./resource/font/ENCR10B.TTF', 18)
    bgm = load_music('./resource/sounds/mission_complete.wav')
    bgm.set_volume(64)
    bgm.play(1)
    draw()
    hide_cursor()
    hide_lattice()


def exit():
    global font, background
    del font, background


def build_stage1():
    global player, droptanks, barricade, prisoner, map
    map = Map()
    game_world.add_object(map, 0)

    player = Player()
    game_world.add_object(player, 1)
    map.set_center_object(player)
    player.set_background(map)
    barricade = Barricade()

    game_world.add_object(barricade, 1)
    barricade.set_background(map)
    prisoner = Pow()

    game_world.add_object(prisoner, 1)
    prisoner.set_background(map)

    with open('./stages/stage1_soldier.json', 'r') as f:
        soldier_list = json.load(f)

    for data in soldier_list:
        soldiers.append(Soldier(data['x'], data['hp_amount'], data['damage_amount'], data['gold']))
    game_world.add_objects(soldiers, 1)
    for soldier in soldiers:
        soldier.set_background(map)


def build_stage2():
    global player, droptanks, barricade, prisoner, map
    map = Map()
    game_world.add_object(map, 0)
    player = Player()
    game_world.add_object(player, 1)
    map.set_center_object(player)
    player.set_background(map)
    barricade = Barricade()
    game_world.add_object(barricade, 1)
    barricade.set_background(map)
    prisoner = Pow()
    game_world.add_object(prisoner, 1)
    prisoner.set_background(map)

    with open('./stages/stage2_droptank.json', 'r') as f:
        droptank_list = json.load(f)  # droptank_list에 역직렬화 해서 넣음.

    for data in droptank_list:
        droptanks.append(Droptank(data['x'], data['hp_amount'], data['damage_amount'], data['gold']))
    game_world.add_objects(droptanks, 1)
    for droptank in droptanks:
        droptank.set_background(map)

    with open('./stages/stage2_soldier.json', 'r') as f:
        soldier_list = json.load(f)

    for data in soldier_list:
        soldiers.append(Soldier(data['x'], data['hp_amount'], data['damage_amount'], data['gold']))
    game_world.add_objects(soldiers, 1)
    for soldier in soldiers:
        soldier.set_background(map)


def build_stage3():
    global player, droptanks, barricade, prisoner, map
    map = Map()
    game_world.add_object(map, 0)
    player = Player()
    game_world.add_object(player, 1)
    map.set_center_object(player)
    player.set_background(map)
    barricade = Barricade()
    game_world.add_object(barricade, 1)
    barricade.set_background(map)
    prisoner = Pow()
    game_world.add_object(prisoner, 1)
    prisoner.set_background(map)

    with open('./stages/stage3_droptank.json', 'r') as f:
        droptank_list = json.load(f)  # droptank_list에 역직렬화 해서 넣음.

    for data in droptank_list:
        droptanks.append(Droptank(data['x'], data['hp_amount'], data['damage_amount'], data['gold']))
    game_world.add_objects(droptanks, 1)
    for droptank in droptanks:
        droptank.set_background(map)

    with open('./stages/stage3_soldier.json', 'r') as f:
        soldier_list = json.load(f)

    for data in soldier_list:
        soldiers.append(Soldier(data['x'], data['hp_amount'], data['damage_amount'], data['gold']))
    game_world.add_objects(soldiers, 1)
    for soldier in soldiers:
        soldier.set_background(map)


def build_stage4():
    global player, droptanks, barricade, prisoner, map
    map = Map()
    game_world.add_object(map, 0)
    player = Player()
    game_world.add_object(player, 1)
    map.set_center_object(player)
    player.set_background(map)
    barricade = Barricade()
    game_world.add_object(barricade, 1)
    barricade.set_background(map)
    prisoner = Pow()
    game_world.add_object(prisoner, 1)
    prisoner.set_background(map)

    with open('./stages/stage4_droptank.json', 'r') as f:
        droptank_list = json.load(f)  # droptank_list에 역직렬화 해서 넣음.

    for data in droptank_list:
        droptanks.append(Droptank(data['x'], data['hp_amount'], data['damage_amount'], data['gold']))
    game_world.add_objects(droptanks, 1)
    for droptank in droptanks:
        droptank.set_background(map)

    with open('./stages/stage4_soldier.json', 'r') as f:
        soldier_list = json.load(f)

    for data in soldier_list:
        soldiers.append(Soldier(data['x'], data['hp_amount'], data['damage_amount'], data['gold']))
    game_world.add_objects(soldiers, 1)
    for soldier in soldiers:
        soldier.set_background(map)


def build_stage5():
    global player, droptanks, barricade, prisoner, map

    map = Map()
    game_world.add_object(map, 0)

    player = Player()
    game_world.add_object(player, 1)
    map.set_center_object(player)
    player.set_background(map)

    barricade = Barricade()
    game_world.add_object(barricade, 1)
    barricade.set_background(map)

    prisoner = Pow()
    game_world.add_object(prisoner, 1)
    prisoner.set_background(map)

    with open('./stages/stage5_droptank.json', 'r') as f:
        droptank_list = json.load(f)  # droptank_list에 역직렬화 해서 넣음.

    for data in droptank_list:
        droptanks.append(Droptank(data['x'], data['hp_amount'], data['damage_amount'], data['gold']))
    game_world.add_objects(droptanks, 1)
    for droptank in droptanks:
        droptank.set_background(map)

    with open('./stages/stage5_soldier.json', 'r') as f:
        soldier_list = json.load(f)

    for data in soldier_list:
        soldiers.append(Soldier(data['x'], data['hp_amount'], data['damage_amount'], data['gold']))
    game_world.add_objects(soldiers, 1)
    for soldier in soldiers:
        soldier.set_background(map)


def get_map():
    return map


def get_player():
    return player


def get_barricade():
    return barricade


def get_prisoner():
    return prisoner


def handle_events():
    global bgm
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_n):  # 다음 스테이지로 이동해야함.
                if main_state.cleared_stage_count == 1:
                    build_stage2()
                elif main_state.cleared_stage_count == 2:
                    build_stage3()
                elif main_state.cleared_stage_count == 3:
                    build_stage4()
                elif main_state.cleared_stage_count == 4:
                    build_stage5()
                elif main_state.cleared_stage_count == 5:
                    game_framework.change_state(title_state)
                bgm.stop()
                game_framework.change_state(main_state)

            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_r):  # 현 스테이지 다시 시작.
                if main_state.cleared_stage_count == 1:
                    build_stage1()
                elif main_state.cleared_stage_count == 2:
                    build_stage2()
                elif main_state.cleared_stage_count == 3:
                    build_stage3()
                elif main_state.cleared_stage_count == 4:
                    build_stage4()
                elif main_state.cleared_stage_count == 5:
                    build_stage5()
                bgm.stop()
                game_framework.change_state(main_state)

            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):  # 타이틀로 이동.
                main_state.cleared_stage_count = 0
                game_framework.change_state(title_state)


def update():
    pass


def draw():
    clear_canvas()
    background.draw(get_canvas_width() // 2, get_canvas_height() // 2)
    if main_state.cleared_stage_count == 5:
        font.draw(105, 385, 'ALL STAGE CLEAR!', (255, 255, 255))
        font.draw(115, 295, 'R REPLAY STAGE', (255, 255, 255))
        font.draw(115, 255, 'ESC BACK TO TITLE', (255, 255, 255))
    else:
        font.draw(135, 385, 'STAGE CLEAR!', (255, 255, 255))
        font.draw(115, 335, 'N NEXT STAGE', (255, 255, 255))
        font.draw(115, 295, 'R REPLAY STAGE', (255, 255, 255))
        font.draw(110, 255, 'ESC BACK TO TITLE', (255, 255, 255))
    update_canvas()