from pico2d import *

class Map:
    def __init__(self):
        self.image = load_image('maaap.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw_to_origin(0, 0 + 200 , 1600 * 1.2, 220 * 1.2)
       # self.image.draw(1200, 30)
