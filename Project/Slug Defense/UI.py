from pico2d import *
import main_state

class Bottom_UI:
    def __init__(self):
        self.image = load_image('Bottom_UI_Background.png')
        self.font = load_font('ENCR10B.TTF', 20)

    def update(self):
        pass

    def draw(self):
        self.image.draw(800//2, 100)
        self.font.draw(65, 175, 'Status', (0,0,0))
        self.font.draw(265, 175, 'Skill', (0,0,0))
        self.font.draw(570, 175, 'Store', (0,0,0))


class Top_UI:
    def __init__(self):
        self.image = load_image('top_ui.png')
        self.font = load_font('ENCR10B.TTF', 20)

    def update(self):
        pass

    def draw(self):
        self.image.draw(800//2, 550)
        self.font.draw(800//2, 500, 'Pass', (1,1,1))