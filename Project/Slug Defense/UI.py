from pico2d import *
import main_state
name = "UI"
class Bottom_UI:
    def __init__(self):
        self.image = load_image('Bottom_UI_Background.png')
        self.category_font = load_font('ENCR10B.TTF', 20)
        self.contents_font = load_font('ENCR10B.TTF', 16)
        self.y = 175

    def update(self):
        pass

    def draw(self):
        self.image.draw(800//2, 100)
        self.category_font.draw(65,  self.y, 'Status', (0, 0, 0))
        self.category_font.draw(265, self.y, 'Skill', (0, 0, 0))
        self.category_font.draw(575, self.y, 'Store', (0, 0, 0))
        self.contents_font.draw(455, self.y - 30, '1 : Upgrade ATK', (0, 0, 0))
        self.contents_font.draw(455, self.y - 60, '2 : Upgrade HP', (0, 0, 0))
        self.contents_font.draw(455, self.y - 90, '3 : Repair Barricade', (0, 0, 0))
        self.contents_font.draw(455, self.y - 120, '4 : Upgrade BRCDE HP', (0, 0, 0))
        self.contents_font.draw(455, self.y - 150, '5 : Upgrade Skill DMG', (0, 0, 0))
        pass

class Top_UI:
    def __init__(self):
        self.image = load_image('top_ui.png')
        self.font = load_font('ENCR10B.TTF', 40)

    def update(self):
        pass

    def draw(self):
        self.image.draw(800//2, 550)
        self.font.draw(30, 540, 'GOLD : %i' % main_state.gold, (255, 255, 0))
        self.font.draw(300, 540, 'WAVE : %i' % main_state.left_wave_amount, (255, 255, 255))