from pico2d import *
import main_state

UPGRADE_SLUG_ATK, UPGRADE_SLUG_HP, REPAIR_BARRICADE, UPGRADE_BARRICADE_HP, UPGRADE_SKILL_DAMAGE, CASTING_CAPET_BOMBING = range(6)
key_event_table = {
    (SDL_KEYDOWN, SDLK_1): UPGRADE_SLUG_ATK,
    (SDL_KEYDOWN, SDLK_2): UPGRADE_SLUG_HP,
    (SDL_KEYDOWN, SDLK_3): REPAIR_BARRICADE,
    (SDL_KEYDOWN, SDLK_4): UPGRADE_BARRICADE_HP,
    (SDL_KEYDOWN, SDLK_5): UPGRADE_SKILL_DAMAGE,
    (SDL_KEYDOWN, SDLK_z): CASTING_CAPET_BOMBING
}

#  슬러그 스킬 구현 시 스킬 데미지 업 기능 구현해야함.

class Store:
    def __init__(self):
        self.cost_slug_ATK = 100
        self.cost_slug_HP = 100
        self.cost_BRCD_RP = 300  # BRCD == Barricade
        self.cost_BRCD_HP = 100
        self.cost_slug_SK = 500  # upgrade capet_bombing damage_amount
        self.cost_capet_bombing = 1000

    def handle_event(self, event):
        if(event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            if key_event == UPGRADE_SLUG_ATK:
                if main_state.gold - self.cost_slug_ATK >= 0:
                    main_state.gold -= self.cost_slug_ATK
                    main_state.player.damage_amount_of_cannon += 50
                    self.cost_slug_ATK *= 2

            elif key_event == UPGRADE_SLUG_HP:
                if main_state.gold - self.cost_slug_HP >= 0:
                    main_state.gold -= self.cost_slug_HP
                    main_state.player.max_hp += 200
                    main_state.player.hp_amount = main_state.player.hp_rate * main_state.player.max_hp
                    self.cost_slug_HP *= 2

            elif key_event == REPAIR_BARRICADE:
                if ((main_state.gold - self.cost_BRCD_RP) >= 0 and
                        0 < main_state.barricade.hp_amount < main_state.barricade.max_hp):
                    main_state.gold -= self.cost_BRCD_RP
                    main_state.barricade.hp_amount = main_state.barricade.max_hp
                    self.cost_BRCD_RP *= 2
                elif ((main_state.gold - self.cost_BRCD_RP) >= 0)and not main_state.barricade.chk_alive:
                    main_state.barricade.chk_alive = True
                    main_state.gold -= self.cost_BRCD_RP
                    self.cost_BRCD_RP *= 2

            elif key_event == UPGRADE_BARRICADE_HP:
                if main_state.gold - self.cost_BRCD_HP >= 0 and main_state.barricade.hp_amount > 0:
                    main_state.gold -= self.cost_BRCD_HP
                    main_state.barricade.max_hp += 200
                    self.cost_BRCD_HP *= 2
                    main_state.barricade.hp_amount = main_state.barricade.max_hp * main_state.barricade.hp_rate

            elif key_event == UPGRADE_SKILL_DAMAGE:
                if main_state.gold - self.cost_slug_SK >= 0:
                    main_state.gold -= self.cost_slug_SK
                    main_state.player.damage_amount_of_skill *= 1.5
                    self.cost_slug_SK *= 2
                    self.cost_capet_bombing *= 1.5
                    print(main_state.player.damage_amount_of_skill)
                pass

    def casting_skill(self):
        main_state.gold -= self.cost_capet_bombing


