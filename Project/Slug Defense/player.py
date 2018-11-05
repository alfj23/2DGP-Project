import game_framework
from pico2d import *
from cannon import Cannon

import game_world

# Player Slug Drive Speed

PIXEL_PER_METER = (10.0 / 0.5)
RUN_SPEED_KMPH = 60.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Player Slug Action Speed

TIME_PER_ACTION = 0.5  # 액션 당 시간
ACTION_PER_TIME = 1.0  # 액션 마다 달라서 따로 빼놓음?
FRAMES_PER_ACTION = 23


# Player Slug Events
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, X = range(5)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_x): X
}

# Player Slug States


class IdleState:

    @staticmethod
    def enter(player, event):
        if event == RIGHT_DOWN:
            player.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            player.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            player.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            player.velocity += RUN_SPEED_PPS

    @staticmethod
    def exit(player, event):
        if event == X:
            player.frame = 0
            player.check_cannon = True
            player.fire_cannon()

    @staticmethod
    def do(player):
        if player.check_cannon:
            player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 23
            if player.frame >= 22:
                player.check_cannon = False
        else:
            player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3



    @staticmethod
    def draw(player):
        if player.check_cannon:
            player.image.clip_draw(int(player.frame) * 140, 0, 140, 80, player.x + 40, player.y)
        else:
            player.image.clip_draw(int(player.frame) * 80, 160, 80 - 3, 80, player.x, player.y)

class DriveState:

    @staticmethod
    def enter(player, event):
        if event == RIGHT_DOWN:
            player.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            player.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            player.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            player.velocity += RUN_SPEED_PPS
        player.dir = clamp(-1, player.velocity, 1)

    @staticmethod
    def exit(player, event):  # 왜 나가는지 event를 통해서 알려줄 수 있음.
        if event == X:
            player.frame = 0
            player.check_cannon = True
            player.fire_cannon()

    @staticmethod
    def do(player):
        if player.check_cannon:
            player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 23
            if player.frame >= 22:
                player.check_cannon = False
        else:
            player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 18

        player.x += player.velocity * game_framework.frame_time
        player.x = clamp(40, player.x, 1600 - 40)

    @staticmethod
    def draw(player):
        if player.check_cannon:
            player.image.clip_draw(int(player.frame) * 140, 0, 140, 80, player.x + 40, player.y)
        else:
            player.image.clip_draw(int(player.frame) * 80, 80, 80 - 3, 80, player.x, player.y)


next_state_table = {
    IdleState: {RIGHT_UP: DriveState, LEFT_UP: DriveState,
                RIGHT_DOWN: DriveState, LEFT_DOWN: DriveState,
                X: IdleState
               },
    DriveState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
                 LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
                 X: DriveState
               }
}


class Player:
    def __init__(self):
        self.x, self.y = 1600 // 2, 70
        self.image = load_image('finaltest.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.check_cannon = False
        self.hp = 200  # 캐릭터 체력

    def fire_cannon(self):
        cannon = Cannon(self.x, self.y)
        game_world.add_object(cannon, 1)

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