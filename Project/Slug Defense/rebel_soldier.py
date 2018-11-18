import game_framework
from pico2d import *
import main_state
import game_world
import random

# soldier Speed

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 15
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# soldier Speed

TIME_PER_ACTION = 1.5  # 액션 당 시간
ACTION_PER_TIME = 1.25 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


# soldier Events



# soldier States


class IdleState:

    @staticmethod
    def enter(solider, event):
        pass

    @staticmethod
    def exit(solider, event):
        pass

    @staticmethod
    def do(solider):  # 사거리 400
       pass

    @staticmethod
    def draw(solider):
       pass


class DeathState:

    @staticmethod
    def enter(solider, event):
        pass

    @staticmethod
    def exit(solider, event):
        pass

    @staticmethod
    def do(solider):
        pass

    @staticmethod
    def draw(solider):
        pass


class MoveState:

    @staticmethod
    def enter(solider, event):
       pass

    @staticmethod
    def exit(solider, event):
       pass

    @staticmethod
    def do(solider):
        pass

    @staticmethod
    def draw(solider):
        pass


class AttackState:

    @staticmethod
    def enter(solider, event):
        pass

    @staticmethod
    def exit(solider, event):
        pass

    @staticmethod
    def do(solider):
        pass

    @staticmethod
    def draw(solider):
        pass


next_state_table = {
    IdleState: {},
    MoveState: {},
    DeathState: {},
    AttackState: {}
}

class Droptank:
    def __init__(self):
        self.x, self.y = random.randint(1600, 3000), 40 + 200
        self.image = load_image('rebel_soldier_moving.png')
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = MoveState #IdleState
        self.cur_state.enter(self, None)
        self.hp = 400
        self.font = load_font('ENCR10B.TTF', 16)
        self.chk_reload = False
        self.gold = 200

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def get_bb(self):
        return self.x - 17, self.y - 22, self.x + 17, self.y + 22

    def draw(self):
        self.cur_state.draw(self)
        self.font.draw(self.x - 60, self.y + 50,
                       '(HP : %i)' % self.hp, (255, 0, 0))
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
       pass