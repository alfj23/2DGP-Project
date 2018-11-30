from pico2d import *
import main_state
name = "UI"

class Bottom_UI:
    def __init__(self):
        self.image = load_image('./resource/UI/Bottom_UI_Background.png')
        self.icon = load_image('./resource/UI/icons.png')
        self.category_font = load_font('./resource/font/ENCR10B.TTF', 20)
        self.contents_font = load_font('./resource/font/ENCR10B.TTF', 16)
        self.y = 175

    def update(self):
        pass

    def draw(self):
        self.image.draw(800//2, 100)
        self.icon.clip_draw(0 * 58, 0, 58, 60, 300, 90)  # skill icon
        self.icon.clip_draw(1 * 58, 0, 58, 60, 735, self.y - 50)  # skill upgrade icon
        self.icon.clip_draw(4 * 59, 0, 58, 60, 455, self.y - 50)  # slug_cannon_damage_upgrade_icon
        self.icon.clip_draw(5 * 59, 0, 58, 60, 455, self.y - 125)  # slug_max_hp_upgrade_icon
        self.icon.clip_draw(3 * 59, 0, 58, 60, 595, self.y - 50)  # barricade_repair_icon
        self.icon.clip_draw(2 * 59, 0, 58, 60, 595, self.y - 125)  # barricade_upgrade_icon

        self.category_font.draw(65,  self.y, 'Status', (0, 0, 0))
        self.category_font.draw(265, self.y, 'Skill', (0, 0, 0))
        self.category_font.draw(575, self.y, 'Store', (0, 0, 0))
        self.contents_font.draw(430, self.y - 87, '1:%i'%main_state.store.cost_slug_ATK, (255, 0, 0))
        self.contents_font.draw(430, self.y - 160, '2:%i'%main_state.store.cost_slug_HP, (255, 0, 0))
        self.contents_font.draw(570, self.y - 87, '3:%i'%main_state.store.cost_BRCD_RP, (255, 0, 0))
        self.contents_font.draw(570, self.y - 160, '4:%i'%main_state.store.cost_BRCD_HP, (255, 0, 0))
        self.contents_font.draw(710, self.y - 87, '5:%i'%main_state.store.cost_slug_SK, (255, 0, 0))
        self.contents_font.draw(275, self.y - 130, 'z:%i'%main_state.store.cost_carpet_bombing, (255, 0, 0))

        self.contents_font.draw(30, self.y - 50, 'HP:%i'%main_state.player.hp_amount, (255, 0, 0))
        self.contents_font.draw(30, self.y - 100, 'DMG:%i' %main_state.player.damage_amount_of_cannon, (0, 0, 0))
        self.contents_font.draw(30, self.y - 150, 'SKILL-DMG:%i'%main_state.player.damage_amount_of_skill,  (0 ,0, 0))

        pass

class Top_UI:
    def __init__(self):
        self.image = load_image('./resource/UI/top_ui.png')
        self.font = load_font('./resource/font/ENCR10B.TTF', 40)

    def update(self):
        pass

    def draw(self):
        self.image.draw(800//2, 550)
        self.font.draw(30, 540, 'GOLD : %i' % main_state.gold, (255, 255, 0))
        self.font.draw(350, 540, 'WAVE : %i' % main_state.left_wave_amount, (255, 255, 255))