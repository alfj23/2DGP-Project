from pico2d import *
import game_world
import main_state
name = "barricade"

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


class BrokenState:
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

next_state_table = {
    IdleState: {},
    HitState: {},
    DamagedState: {},
    BrokenState: {}

}


class Barricade:
    image = None

    def __init__(self):
        self.x, self.y = 200, 35 + 200
        self.image = load_image('barricade.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.hp = 300
        self.cur_state = IdleState
        self.event_que = []
        self.cur_state.enter(self, None)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state]
            self.cur_state.enter(self, event)
        if self.hp <= 0:
            game_world.remove_object(self)
            self.x = -100

        pass

    def get_bb(self):
        return self.x - 25, self.y - 20, self.x + 25, self.y + 20

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())
        self.font.draw(self.x - 60, self.y + 50,
                       '(HP : %i)' % self.hp, (255, 0, 0))