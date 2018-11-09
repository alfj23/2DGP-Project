from pico2d import *
import game_world
import main_state


class Barricade:
    image = None

    def __init__(self, x=400, y=300, velocity=3):
        self.x, self.y = 200, 40 + 200
        self.image = load_image('barricade.png')
        self.hp = 300
        pass

    def update(self):
        pass

    def get_bb(self):
        pass

    def draw(self):
        pass