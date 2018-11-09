from pico2d import *
import game_world
import main_state


class Barricade:
    image = None

    def __init__(self, x=400, y=300, velocity=3):
        self.x, self.y = 200, 40 + 200
        self.image = load_image('barricade.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.hp = 300

    def update(self):
        if self.hp <= 0:
            game_world.remove_object(self)
            self.x = -100  # 좌표를 어떻게 없애지? ㅠㅠ

        pass

    def get_bb(self):
        return self.x - 25, self.y - 20, self.x + 25, self.y + 20

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())
        self.font.draw(self.x - 60, self.y + 50,
                       '(HP : %i)' % self.hp, (255, 0, 0))