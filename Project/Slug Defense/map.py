from pico2d import *

class Map:
    def __init__(self):
        self.image = load_image('maaap.png')

    def update(self):
        pass
    
    def get_bb(self):
        pass

    def draw(self):
        self.image.draw_to_origin(0 - 2, 0 + 200 , 1600 * 1.367, 220 * 1.367)
       # self.image.draw(1200, 30)
