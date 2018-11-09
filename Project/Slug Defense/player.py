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
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION # 액션 마다 달라서 따로 빼놓음?
FRAMES_PER_ACTION = 23


# Player Slug Events
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, X, DISABLED, REPAIR = range(7)

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
        if player.hp <= 0:
            player.add_event(DISABLED)
        if player.check_cannon:
            player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 23
            if player.frame >= 22:
                player.check_cannon = False
        else:
            player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3



    @staticmethod
    def draw(player):
        if player.check_cannon:
            player.image.clip_draw(int(player.frame) * 140, 80, 140, 80, player.x + 40, player.y)
        else:
            player.image.clip_draw(int(player.frame) * 80, 240, 80 - 3, 80, player.x, player.y)


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
        if player.hp <= 0:
            player.add_event(DISABLED)

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
            player.image.clip_draw(int(player.frame) * 140, 80, 140, 80, player.x + 40, player.y)
        else:
            player.image.clip_draw(int(player.frame) * 80, 160, 80, 80, player.x, player.y)


class DamagedState:
    @staticmethod
    def enter(player, event):
        if event == DISABLED:
            player.timer = 1000
            player.frame = 0
        if event == RIGHT_DOWN:
            player.velocity += 0
        elif event == LEFT_DOWN:
            player.velocity -= 0
        elif event == RIGHT_UP:
            player.velocity -= 0
        elif event == LEFT_UP:
            player.velocity += 0
        pass

    @staticmethod
    def exit(player, event):
        player.hp = 200
        pass

    @staticmethod
    def do(player):
        player.timer -= 1
        if player.timer == 0:
            player.add_event(REPAIR)
        player.frame = (player.frame + ACTION_PER_TIME * FRAMES_PER_ACTION * game_framework.frame_time) % 25

        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 120, 0, 120, 80, player.x, player.y)
        pass


next_state_table = {
    IdleState: {RIGHT_UP: DriveState, LEFT_UP: DriveState,
                RIGHT_DOWN: DriveState, LEFT_DOWN: DriveState,
                X: IdleState, DISABLED: DamagedState
               },
    DriveState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
                 LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
                 X: DriveState, DISABLED: DamagedState
               },
    DamagedState: {REPAIR: IdleState}
}


class Player:
    def __init__(self):
        self.x, self.y = 1600 // 2, 40 + 200
        self.image = load_image('slug.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.check_cannon = False
        self.hp = 0  # 캐릭터 체력

    def fire_cannon(self):
        cannon = Cannon(self.x, self.y)
        game_world.add_object(cannon, 1)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def get_bb(self):
        return self.x -20, self.y -25, self.x + 30, self.y + 20

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())
        self.font.draw(self.x - 60, self.y + 50,
                       '(HP : %i)' % self.hp, (255, 0, 0))

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)