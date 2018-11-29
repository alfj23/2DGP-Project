from pico2d import *
import game_world
import main_state
import world_build_state
import game_framework

#missile Speed

PIXEL_PER_METER = (10.0 / 0.15)
RUN_SPEED_KMPH = 40
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

#missile Action Speed

TIME_PER_ACTION = 0.1  # 액션 당 시간
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

#missile event
EXPLORE = range(1)

class FallingState:
    @staticmethod
    def enter(missile, event):
        pass

    @staticmethod
    def exit(missile,event):
        pass

    @staticmethod
    def do(missile):
        pass

    @staticmethod
    def draw(missile):
        pass


class ExploringState:
    @staticmethod
    def enter(missile, event):
        pass

    @staticmethod
    def exit(missile, event):
        pass

    @staticmethod
    def do(missile):
        pass

    @staticmethod
    def draw(missile):
        pass


next_state_table = {
    FallingState: {EXPLORE: ExploringState},
    ExploringState: {}
}


class Missile:
    m_image = None  # missile image
    e_image = None  # explosion image

    def __init__(self, x=0, y=0):
        if Missile.m_image == None:
            self.m_image = load_image('./resource/skill/skill_missile')
        if Missile.e_image == None:
            self.e_image = load_image('./resource/skill/skill_explosion')
        self.x, self.y = x * PIXEL_PER_METER, y * PIXEL_PER_METER
        self.velocity = 0
        self.frame = 0
        self.damage_amount = main_state.player.damage_amount_of_skill
        self.event_que = []
        self.cur_state = FallingState
        self.cur_state.enter(self, None)
        pass

    def add_event(self, event):
        self.event_que.insert(0, event)

    def set_background(self, bg):
        pass

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)
        pass

    def get_bb(self):
        return
        pass

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())
        pass