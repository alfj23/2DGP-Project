import game_framework
from pico2d import *
import main_state
from behavior_tree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
from droptank_bomb import Bomb
import game_world
import random
name = "droptank"

# droptank Speed

PIXEL_PER_METER = (10.0 / 0.4)  # 10 pixel = 30cm
RUN_SPEED_KMPH = 20
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# droptank Speed

TIME_PER_ACTION = 1.25  # 액션 당 시간
ACTION_PER_TIME = 1.25 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


# droptank Events
RELOAD, DIE, DRIVE, MARKING, FIRE = range(5) # 재장전/ 죽음 / 이동 / 조준 / 발사


# droptank States


class IdleState:

    @staticmethod
    def enter(droptank, event):
        droptank.frame = 0
        droptank.timer = 800
        if event == RELOAD:
            droptank.chk_reload = True
        pass

    @staticmethod
    def exit(droptank, event):
        pass

    @staticmethod
    def do(droptank):  # 사거리 400
        if droptank.hp <= 0:
            droptank.add_event(DIE)
        if droptank.timer == 0:
            droptank.chk_reload = False
            droptank.add_event(MARKING)
        if droptank.x - main_state.player.x > 400:
            droptank.add_event(DRIVE)
        droptank.frame = (droptank.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        if droptank.chk_reload:
            droptank.timer -= 1

    @staticmethod
    def draw(droptank):
        cx = droptank.x - droptank.bg.window_left
        droptank.image.clip_draw(int(droptank.frame) * 100, 240, 100, 80, cx, droptank.y)


class DeathState:

    @staticmethod
    def enter(droptank, event):
        droptank.frame = 0
        main_state.gold += droptank.gold
        main_state.left_wave_amount -= 1
        pass

    @staticmethod
    def exit(droptank, event):
        pass

    @staticmethod
    def do(droptank):
        droptank.frame = (droptank.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7
        if int(droptank.frame) % 7 == 6:
            game_world.remove_object(droptank)
            droptank.x = 2000

        pass

    @staticmethod
    def draw(droptank):
        cx = droptank.x - droptank.bg.window_left
        droptank.image.clip_draw(int(droptank.frame) * 100, 0, 100, 80, cx, droptank.y)
        pass


class DriveState:

    @staticmethod
    def enter(droptank, event):
        droptank.frame = 0
        droptank.velocity -= RUN_SPEED_PPS

    @staticmethod
    def exit(droptank, event):
        droptank.velocity = 0

    @staticmethod
    def do(droptank):
        if droptank.hp <= 0:
            droptank.add_event(DIE)
        if droptank.x - main_state.player.x <= droptank.atk_range:
            droptank.add_event(MARKING)
        else:
            droptank.frame = (droptank.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
            droptank.x += droptank.velocity * game_framework.frame_time
            droptank.x = clamp(0 + 40, droptank.x, 4000 - 40)

    @staticmethod
    def draw(droptank):
        cx = droptank.x - droptank.bg.window_left
        droptank.image.clip_draw(int(droptank.frame) * 100, 160, 100, 80, cx, droptank.y)


class AttackState:

    @staticmethod
    def enter(droptank, event):
        if droptank.hp <= 0:
            droptank.add_event(DIE)
        pass

    @staticmethod
    def exit(droptank, event):
        if event == RELOAD:
            droptank.fire_bomb()

    @staticmethod
    def do(droptank):
        if droptank.hp <= 0:
            droptank.add_event(DIE)
        droptank.frame = (droptank.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if int(droptank.frame) % 8 == 7:
            droptank.add_event(RELOAD)
            droptank.frame = 0


    @staticmethod
    def draw(droptank):
        cx = droptank.x - droptank.bg.window_left
        droptank.image.clip_draw(int(droptank.frame) * 100, 80, 100, 80, cx, droptank.y)


next_state_table = {
    IdleState: {DIE: DeathState, DRIVE: DriveState, MARKING: AttackState},
    DriveState: {DIE: DeathState, MARKING: AttackState},
    DeathState: {}, #MARKING: DeathState, DRIVE: DeathState, RELOAD: DeathState
    AttackState: {DIE: DeathState, DRIVE: DriveState, RELOAD: IdleState, FIRE: AttackState}
}

animation_name = ['IDLE', 'DRIVE', 'ATTACK', 'DIE']


class Droptank:
    def __init__(self):
        self.x, self.y = random.randint(1600, 3000), 40 + 200
        self.image = load_image('./resource/droptank/droptank.png')
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.hp = 400
        self.atk_range = 400
        self.font = load_font('./resource/font/ENCR10B.TTF', 16)
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
        pass

    def get_bb(self):
        return self.x - self.bg.window_left - 33, self.y - 25, self.x - self.bg.window_left + 32, self.y + 20

    def set_background(self, bg):
        self.bg = bg
        pass

    def fire_bomb(self):
        bomb = Bomb(self.x - self.bg.window_left, self.y)
        game_world.add_object(bomb, 1)
        pass

    def draw(self):
        self.cur_state.draw(self)
        self.font.draw(self.x - self.bg.window_left - 60, self.y + 50,
                       '(HP : %i)' % self.hp, (255, 0, 0))
        draw_rectangle(*self.get_bb())

