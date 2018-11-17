from pico2d import *
import main_state

class Bottom_UI:
    def __init__(self):
        self.image = load_image('Bottom_UI_Background.png')
        self.font = load_font('ENCR10B.TTF')

    def update(self):
        pass

    def draw(self):
        self.image.draw(800//2, 100)
