from pico2d import *
import game_world


class Bomb:
    image = None

    def __init__(self, x=400, y=300, velocity=1):
        self.x, self.y, self.velocity = x, y, velocity
        self.frame = 0
        if Bomb.image == None:
            self.image = load_image('droptank_bomb.png')

    def update(self):
        self.x -= self.velocity
       # print(self.velocity, self.x)

    def draw(self):
        self.image.clip_draw(self.frame * 14, 40, 14, 14, self.x, self.y)
        if self.x > 0 + 14:
            game_world.remove_object(self)  # cannon 이 범위 벗어날 시 반환됨
