from pico2d import *
import game_world
import main_state

# barricade Events
REPAIR, UNDER50, DESTROYED = range(3)  # repair barricade / hp_amount under 50% / barricade destroyed
# barricade States
class IdleState:
    @staticmethod
    def enter(barricade, event):
        pass

    @staticmethod
    def exit(barricade, event):
        pass

    @staticmethod
    def do(barricade):
        pass

    @staticmethod
    def draw(barricade):
        pass


class HitState:
    @staticmethod
    def enter(barricade, event):
        pass

    @staticmethod
    def exit(barricade, event):
        pass

    @staticmethod
    def do(barricade):
        pass

    @staticmethod
    def draw(barricade):
        pass


class DamagedState:
    @staticmethod
    def enter(barricade, event):
        pass

    @staticmethod
    def exit(barricade, event):
        pass

    @staticmethod
    def do(barricade):
        pass

    @staticmethod
    def draw(barricade):
        pass


class DestroyedState:
    @staticmethod
    def enter(barricade, event):
        pass

    @staticmethod
    def exit(barricade, event):
        pass

    @staticmethod
    def do(barricade):
        pass

    @staticmethod
    def draw(barricade):
        pass


class Bomb:
    image = None

    def __init__(self, x=800, y=200, velocity=0.5):
        self.x, self.y, self.velocity = x, y, velocity
        self.frame = 0
        self.damage_amount = 100
        if Bomb.image == None:
            self.image = load_image('droptank_bomb.png')

    def update(self):
        self.x -= self.velocity
        self.frame = (self.frame + 1) % 20

        if main_state.collide(self, main_state.barricade):
            game_world.remove_object(self)
            main_state.barricade.hp -= self.damage_amount

        if main_state.collide(self, main_state.player):
            game_world.remove_object(self)
            main_state.player.hp -= self.damage_amount



    def get_bb(self):
        return self.x - 47, self.y - 7, self.x - 33, self.y + 7

    def draw(self):
        self.image.clip_draw(self.frame * 14, 40, 14, 14, self.x-40, self.y)
        draw_rectangle(*self.get_bb())
        if self.x < 0 + 14:
            game_world.remove_object(self)  # cannon 이 범위 벗어날 시 반환됨
