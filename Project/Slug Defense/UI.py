from pico2d import *

class Bottom_UI:
    def __init__(self):
        self.image = load_image('Bottom_UI_Background.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(800//2, 100)
       # self.image.draw(1200, 30)
