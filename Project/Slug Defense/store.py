import main_state
from pico2d import *
UPGRADE_SLUG_ATK, UPGRADE_SLUG_HP, REPAIR_BARRICADE, UPGRADE_BARRICADE_HP, UPGRADE_SKILL_DAMAGE = range(5)
key_event_table = {
    (SDL_KEYDOWN, SDLK_1): UPGRADE_SLUG_ATK,
    (SDL_KEYDOWN, SDLK_2): UPGRADE_SLUG_HP,
    (SDL_KEYDOWN, SDLK_3): REPAIR_BARRICADE,
    (SDL_KEYDOWN, SDLK_4): UPGRADE_BARRICADE_HP,
    (SDL_KEYDOWN, SDLK_5): UPGRADE_SKILL_DAMAGE
}

def enter():
    global cost_ATK, cost_HP, cost_BRCD_RP, cost_BRCD_HP, cost_SK
    cost_ATK, cost_HP, cost_BRCD_RP, cost_BRCD_HP, cost_SK = 100, 100, 300, 100, 300
    pass

def exit():
    pass

def handle_events():

    pass