import game_framework
from pico2d import *
from cannon import Cannon
from slug_skill import Missile
import game_world
import main_state

__name__ = "player"
# Player Slug Drive Speed

PIXEL_PER_METER = (10.0 / 0.5)
RUN_SPEED_KMPH = 50.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Player Slug Action Speed

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 20


# Player Slug Events
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, FIRE_CANNON, FIRE_MISSILES, DISABLED, REPAIR = range(8)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_x): FIRE_CANNON,
    (SDL_KEYDOWN, SDLK_z): FIRE_MISSILES
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
        if event == REPAIR:
            player.hp_amount = player.max_hp

    @staticmethod
    def exit(player, event):
        if event == FIRE_CANNON:
            player.frame = 0
            player.check_fired = True
            player.fire_cannon()
        elif event == FIRE_MISSILES:
            player.fire_missile()
        elif event == DISABLED:
            player.timer = 1000

    @staticmethod
    def do(player):
        if player.hp_amount <= 0:
            player.add_event(DISABLED)
        if player.check_fired:
            player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 23
            if player.frame >= 22:
                player.check_fired = False
        else:
            player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3

    @staticmethod
    def draw(player):
        cx = player.x - player.bg.window_left
        if player.check_fired:
            player.image.clip_draw(int(player.frame) * 140, 80, 140, 80, cx + 40, player.y)
        else:
            player.image.clip_draw(int(player.frame) * 80, 240, 80 - 3, 80, cx, player.y)


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
    def exit(player, event):
        if event == FIRE_CANNON:
            player.frame = 0
            player.check_fired = True
            player.fire_cannon()
        elif event == FIRE_MISSILES:
            player.fire_missile()
        elif event == DISABLED:
            player.timer = 1000

    @staticmethod
    def do(player):
        if player.hp_amount <= 0:
            player.add_event(DISABLED)
        else:
            if player.check_fired:
                player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 23
                if player.frame >= 22:
                    player.check_fired = False
            else:
                player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 18

            player.x += player.velocity * game_framework.frame_time
            player.x = clamp(0+40, player.x, 1600 - 40)

    @staticmethod
    def draw(player):
        cx = player.x - player.bg.window_left
        if player.check_fired:
            player.image.clip_draw(int(player.frame) * 140, 80, 140, 80, cx + 40, player.y)
        else:
            player.image.clip_draw(int(player.frame) * 80, 160, 80, 80, cx, player.y)


class DamagedState:
    @staticmethod
    def enter(player, event):
        if event == DISABLED:
            player.event_que.clear()
            player.frame = 0

    @staticmethod
    def exit(player, event):
        if event == FIRE_MISSILES:
            player.fire_missile()

    @staticmethod
    def do(player):
        player.timer -= 1
        if player.timer == 0:
            player.add_event(REPAIR)
        player.frame = (player.frame + ACTION_PER_TIME * FRAMES_PER_ACTION * game_framework.frame_time) % 25

    @staticmethod
    def draw(player):
        cx = player.x - player.bg.window_left
        if int(player.frame) % 25 == 24:
            player.image.clip_draw(240, 240, 80, 80, cx, player.y)
        else:
            player.image.clip_draw(int(player.frame) * 120, 0, 120, 80, cx, player.y)


next_state_table = {
    IdleState: {RIGHT_UP: DriveState, LEFT_UP: DriveState, RIGHT_DOWN: DriveState, LEFT_DOWN: DriveState,
                FIRE_CANNON: IdleState, FIRE_MISSILES: IdleState, DISABLED: DamagedState},
    DriveState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
                 LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
                 FIRE_CANNON: DriveState, FIRE_MISSILES: DriveState, DISABLED: DamagedState},
    DamagedState: {REPAIR: IdleState, RIGHT_UP: DamagedState, RIGHT_DOWN: DamagedState, LEFT_UP: DamagedState,
                   LEFT_DOWN: DamagedState, FIRE_CANNON: DamagedState, FIRE_MISSILES: IdleState}
}


class Player:
    def __init__(self):
        self.y = 40 + 200
        self.image = load_image('./resource/slug/slug.png')
        self.cannon_sound = load_wav('./resource/sounds/semishoot.wav')
        self.cannon_sound.set_volume(20)
        self.dir, self.velocity, self.frame = 1, 0, 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.check_fired = False
        self.timer = 0.0
        self.damage_amount_of_cannon = 50
        self.damage_amount_of_skill = 300
        self.max_hp = 150
        self.hp_amount = self.max_hp
        self.hp_rate = self.hp_amount / self.max_hp

    def fire_cannon(self):
        self.cannon_sound.play(1)
        cannon = Cannon(self.x - self.bg.window_left - 10, self.y)
        game_world.add_object(cannon, 1)

    def fire_missile(self):
        if main_state.gold - main_state.store.cost_carpet_bombing >= 0:
            main_state.store.casting_skill()
            missiles = [Missile(1, 8), Missile(3, 9),Missile(5, 10), Missile(7, 11), Missile(9, 12), Missile(11, 13), Missile(13, 14), Missile(15, 15),
                        Missile(17, 16), Missile(19, 17), Missile(21, 18), Missile(23, 19), Missile(25, 20), Missile(27, 21),
                        Missile(29, 22), Missile(31, 23)]
            game_world.add_objects(missiles, 1)
            for missile in missiles:
                missile.set_background(main_state.map)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def get_bb(self):
        return self.x - self.bg.window_left - 20, self.y - 25, self.x - self.bg.window_left + 30, self.y + 20

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)
        self.hp_rate = self.hp_amount / self.max_hp

    def draw(self):
        self.cur_state.draw(self)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def set_background(self, bg):
        self.bg = bg
        self.x = self.bg.w / 2 - 400