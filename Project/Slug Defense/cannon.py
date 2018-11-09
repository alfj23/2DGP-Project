from pico2d import *
import game_world
import main_state


class Cannon:
    image = None

    def __init__(self, x=400, y=300, velocity=3):
        self.x, self.y, self.velocity = x, y, velocity
        self.frame = 0
        self.damage = 200
        if Cannon.image == None:
            self.image = load_image('cannon_ball.png')

    def update(self):
        self.x += self.velocity
        self.frame = (self.frame + 1) % 4

        for droptank in main_state.droptanks:
            if main_state.collide(self, droptank):
                droptank.hp -= self.damage
                game_world.remove_object(self)
                break

    def get_bb(self):
        return self.x + 10, self.y, self.x + 45, self.y + 20

    def draw(self):
        self.image.clip_draw(self.frame * 40, 0, 40, 30, self.x + 30, self.y + 10)
        draw_rectangle(*self.get_bb())
        if self.x > 1600 - 20:
            game_world.remove_object(self)  # cannon 이 범위 벗어날 시 반환됨
