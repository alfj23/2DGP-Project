import game_framework
from pico2d import *

import game_world

# POW Speed

PIXEL_PER_METER = (10.0 / 0.15)
RUN_SPEED_KMPH = 0.01
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# POW Speed

TIME_PER_ACTION = 1.0 # 액션 당 시간
ACTION_PER_TIME = 1.0  # 액션 마다 달라서 따로 빼놓음?
FRAMES_PER_ACTION = 13


# POW Events
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, X = range(5)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_x): X
}

# POW States


class IdleState:

    @staticmethod
    def enter(prisoner, event):
        pass

    @staticmethod
    def exit(prisoner, event):
        pass

    @staticmethod
    def do(prisoner):
        if prisoner.dir == 1:
            prisoner.velocity += RUN_SPEED_PPS
            if prisoner.x >= 180 - 1:
                prisoner.velocity = -1
                prisoner.dir = -1
        elif prisoner.dir == -1:
            prisoner.velocity -= RUN_SPEED_PPS
            if prisoner.x <= 20 + 1:
                prisoner.velocity = 1
                prisoner.dir = 1
        prisoner.frame = (prisoner.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 13

        prisoner.x += prisoner.velocity * game_framework.frame_time
        prisoner.x = clamp(0 + 20, prisoner.x, 200 - 20)
        print(prisoner.velocity)
        pass

    @staticmethod
    def draw(prisoner):
        if prisoner.dir == 1:
            prisoner.image.clip_draw(int(prisoner.frame) * 50, 0, 50, 50, prisoner.x, prisoner.y)
        else:
            prisoner.image.clip_draw(int(prisoner.frame) * 50, 50, 50, 50, prisoner.x, prisoner.y)
        pass


class WatchState:

    @staticmethod
    def enter(prisoner, event):
        pass

    @staticmethod
    def exit(prisoner, event):
        pass

    @staticmethod
    def do(prisoner):
        pass

    @staticmethod
    def draw(prisoner):
        pass


next_state_table = {
    IdleState: {},
    WatchState: {}
}


class Pow:
    def __init__(self):
        self.x, self.y = 100, 60
        self.image = load_image('P_O_W.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

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
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)