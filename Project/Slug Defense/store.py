from pico2d import *
import main_state

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

def handle_event(event):
    events = get_events()
    for event in events:
        if event == UPGRADE_SLUG_ATK:
            if main_state.gold - cost_ATK >= 0:
                main_state.gold -= cost_ATK
                main_state.player.damage_amount_of_cannon += 50
                cost_ATK *= 2

        elif event == UPGRADE_SLUG_HP:
            if main_state.gold - cost_HP >= 0:
                main_state.gold -= cost_HP
                main_state.player.max_hp += 200
                main_state.player.hp_amount = main_state.player.hp_rate * main_state.player.max_hp
                cost_HP *= 2

        elif event == REPAIR_BARRICADE:
            if ((main_state.gold - cost_BRCD_RP) >= 0 and
                    0 < main_state.barricade.hp_amount < main_state.barricade.max_hp):
                main_state.gold -= cost_BRCD_RP
                main_state.barricade.hp_amount = main_state.barricade.max_hp
                cost_BRCD_RP *= 2
            elif ((main_state.gold - cost_BRCD_RP) >= 0)and not main_state.barricade.chk_alive:
                main_state.barricade.chk_alive = True
                main_state.gold -= cost_BRCD_RP
                cost_BRCD_RP *= 2

        elif event == UPGRADE_SKILL_DAMAGE:
            pass


