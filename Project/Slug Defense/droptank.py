import game_framework
from pico2d import *

# droptank Speed

PIXEL_PER_METER = (10.0 / 0.5)
RUN_SPEED_KMPH = 20
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# droptank Speed

TIME_PER_ACTION = 2.0  # 액션 당 시간
ACTION_PER_TIME = 1.0
FRAMES_PER_ACTION = 8

# droptank States


class IdleState:

    @staticmethod
    def enter(droptank, event):
        pass

    @staticmethod
    def exit(droptank, event):
        pass

    @staticmethod
    def do(droptank): # 사거리 800
        if droptank.x <= 800:
            droptank.chk_range = True
            droptank.velocity = 0
            droptank.frame = (droptank.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if droptank.x > 800:
            droptank.velocity = RUN_SPEED_PPS
            droptank.frame = (droptank.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
            droptank.x -= droptank.velocity * game_framework.frame_time
        pass

    @staticmethod
    def draw(droptank):
        if droptank.chk_range == False:
            droptank.image.clip_draw(int(droptank.frame) * 100, 160, 100, 80, droptank.x, droptank.y)
        else:
            droptank.image.clip_draw(int(droptank.frame) * 100, 80, 100, 80, droptank.x, droptank.y)
        pass


class DieState:

    @staticmethod
    def enter(droptank, event):
        pass

    @staticmethod
    def exit(droptank, event):
        pass

    @staticmethod
    def do(droptank):
        pass

    @staticmethod
    def draw(droptank):
        pass


class Droptank:
    def __init__(self):
        self.x, self.y = 1600 - 100, 40
        self.image = load_image('EnemyTank_M_I_F.png')
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.chk_range = False
        self.hp = 400

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self, event):
       pass