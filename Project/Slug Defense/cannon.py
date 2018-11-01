from pico2d import *
import game_world


class Cannon:
    image = None

    def __init__(self, x=400, y=300, velocity=3):
        self.x, self.y, self.velocity = x, y, velocity
        self.frame = 0
        if Cannon.image == None:
            self.image = load_image('cannon_ball.png')

    def update(self):
        self.x += self.velocity

    def draw(self):
        self.image.clip_draw(self.frame * 40, 0, 40, 30, self.x + 30, self.y + 10)
        if self.x > 1600 - 20:
            game_world.remove_object(self)  # cannon 이 범위 벗어날 시 반환됨
