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
        return self.x - 25, self.y - 20, self.x + 25, self.y + 20
        pass

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())
        pass