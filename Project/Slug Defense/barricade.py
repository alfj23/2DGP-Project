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
        if event == REPAIR:
            barricade.initialize()

    @staticmethod
    def exit(barricade, event):
        pass

    @staticmethod
    def do(barricade):
        if barricade.hp_amount <= 0:
            barricade.chk_alive = False
            barricade.add_event(DESTROYED)

    @staticmethod
    def draw(barricade):
        cx = barricade.x - barricade.bg.window_left
        barricade.image.draw(cx, barricade.y)


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
        if event == DESTROYED:
            barricade.x = -100

    @staticmethod
    def exit(barricade, event):
        pass

    @staticmethod
    def do(barricade):
        if barricade.chk_alive:
            barricade.add_event(REPAIR)

    @staticmethod
    def draw(barricade):
        pass


next_state_table = {
    IdleState: {UNDER50: DamagedState, DESTROYED: BrokenState},
    HitState: {UNDER50: DamagedState},
    DamagedState: {REPAIR: IdleState, DESTROYED: BrokenState},
    BrokenState: {REPAIR: IdleState}
}


class Barricade:
    image = None

    def __init__(self):
        self.x, self.y = 200, 35 + 200
        self.image = load_image('./resource/barricade/barricade.png')
        self.font = load_font('./resource/font/ENCR10B.TTF', 16)
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.max_hp = 300
        self.hp_amount = self.max_hp
        self.hp_rate = (self.hp_amount / self.max_hp)  # 체력 퍼센테이지
        self.chk_alive = True

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)
        self.hp_rate = (self.hp_amount / self.max_hp)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def get_bb(self):
        return self.x - self.bg.window_left - 25, self.y - 20, self.x - self.bg.window_left + 25, self.y + 20

    def set_background(self, bg):
        self.bg = bg
        pass

    def initialize(self):
        self.x = 200 #- self.bg.window_left
        self.max_hp = 300
        main_state.cost_BRCD_HP = 100

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())
        self.font.draw(self.x - self.bg.window_left - 60, self.y + 50,
                       '(HP : %i)' % self.hp_amount, (255, 0, 0))
