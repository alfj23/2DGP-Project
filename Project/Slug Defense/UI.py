from pico2d import *
import main_state

class Bottom_UI:
    def __init__(self):
        self.image = load_image('Bottom_UI_Background.png')
        self.font = load_font('ENCR10B.TTF', 20)
        self.y = 175

    def update(self):
        pass

    def draw(self):
        self.image.draw(800//2, 100)
        self.font.draw(65,  self.y, 'Status', (0,0,0))
        self.font.draw(265, self.y, 'Skill', (0,0,0))
        self.font.draw(575, self.y, 'Store', (0,0,0))


class Top_UI:
    def __init__(self):
        self.image = load_image('top_ui.png')
        self.font = load_font('ENCR10B.TTF', 40)

    def update(self):
        pass

    def draw(self):
        self.image.draw(800//2, 550)
        self.font.draw(30, 540, 'GOLD : %i' %main_state.gold, (255, 255, 0))
        self.font.draw(300, 540, 'WAVE : %i', (255, 255, 255))