from pico2d import *

class Map:
    def __init__(self):
        self.image = load_image('maaap.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(1600//2, 600//2)
       # self.image.draw(1200, 30)
