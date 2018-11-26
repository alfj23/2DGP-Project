import game_framework
from pico2d import *
import main_state
import game_world
import random

__name__ = "rebel_soldier"
# soldier Speed

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# soldier Speed

TIME_PER_ACTION = 0.5  # 액션 당 시간
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

'''
# soldier Events

ATTACK, DIE, MOVE = range(3)

# soldier States


class IdleState:

    @staticmethod
    def enter(soldier, event):
        soldier.velocity = 0
        pass

    @staticmethod
    def exit(soldier, event):
        pass

    @staticmethod
    def do(soldier):
        if soldier.hp <= 0:
            soldier.add_event(DIE)
        soldier.frame = (soldier.frame + ACTION_PER_TIME*FRAMES_PER_ACTION*game_framework.frame_time) % 4
        pass

    @staticmethod
    def draw(soldier):
        cx = soldier.x - soldier.bg.window_left
        soldier.image.clip_draw(int(soldier.frame) * 40, 50, 40, 50, cx, soldier.y + 2)
        pass


class DeathState:

    @staticmethod
    def enter(soldier, event):
        soldier.frame = 0
        main_state.left_wave_amount -= 1
        main_state.gold += soldier.gold
        pass

    @staticmethod
    def exit(soldier, event):
        pass

    @staticmethod
    def do(soldier):
        if int(soldier.frame) % 22 == 21:
            game_world.remove_object(soldier)
            soldier.x = 2000
        soldier.frame = (soldier.frame + ACTION_PER_TIME * FRAMES_PER_ACTION * game_framework.frame_time) % 22
        pass

    @staticmethod
    def draw(soldier):
        cx = soldier.x - soldier.bg.window_left
        soldier.image.clip_draw(int(soldier.frame) * 52, 150, 48, 80, cx, soldier.y + 16)
        pass


class MoveState:

    @staticmethod
    def enter(soldier, event):
        soldier.velocity -= RUN_SPEED_PPS
        pass

    @staticmethod
    def exit(soldier, event):
        soldier.velocity = 0
        pass

    @staticmethod
    def do(soldier):
        if 0 < soldier.x - main_state.player.x <= soldier.atk_range \
                or 0 < soldier.x - main_state.barricade.x <= soldier.atk_range \
                or 0 < soldier.x - main_state.prisoner.x <= soldier.atk_range:
            soldier.add_event(ATTACK)
        if soldier.hp <= 0:
            soldier.add_event(DIE)
        else:
            soldier.frame = (soldier.frame + FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 12
            soldier.x += soldier.velocity * game_framework.frame_time
            soldier.x = clamp(0 + 17, soldier.x, 4000 - 17)
        pass

    @staticmethod
    def draw(soldier):
        cx = soldier.x - soldier.bg.window_left
        soldier.image.clip_draw(int(soldier.frame) * 33, 0, 33, 44, cx, soldier.y)
        pass


class AttackState:

    @staticmethod
    def enter(solider, event):
        solider.frame = 0
        pass

    @staticmethod
    def exit(solider, event):
        pass

    @staticmethod
    def do(soldier):
        if (soldier.x - main_state.player.x > soldier.atk_range
            or soldier.x - main_state.barricade.x > soldier.atk_range
            or soldier.x - main_state.prisoner.x > soldier.atk_range):
            soldier.add_event(MOVE)
        soldier.frame = (soldier.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 16
        if main_state.collide(main_state.player, soldier) and int(soldier.frame) % 16 == 15:
            main_state.player.hp_amount -= soldier.damage_amount
        elif main_state.collide(main_state.barricade, soldier) and int(soldier.frame) % 16 == 15:
            main_state.barricade.hp_amount -= soldier.damage_amount
        elif main_state.collide(main_state.prisoner, soldier) and int(soldier.frame) % 16  == 15:
            main_state.prisoner.hp_amount -= soldier.damage_amount
        pass

    @staticmethod
    def draw(soldier):
        cx = soldier.x - soldier.bg.window_left
        soldier.image.clip_composite_draw(int(soldier.frame) * 80, 100, 80, 50, 3.141592, 'v', cx, soldier.y + 2, 80, 50)
        pass


next_state_table = {
    IdleState: {ATTACK: AttackState, DIE: DeathState, MOVE: MoveState},
    MoveState: {ATTACK: AttackState, DIE: DeathState},
    DeathState: {},
    AttackState: {DIE: DeathState, MOVE: MoveState}
}
'''


class Soldier:
    def __init__(self):
        self.x, self.y = random.randint(1600, 4000), 32 + 200
        self.image = load_image('./resource/rebel_soldier/soldier.png')
        self.velocity = 0
        self.frame = random.randint(0, 11)
        self.hp = 200
        self.font = load_font('./resource/font/ENCR10B.TTF', 16)
        self.chk_reload = False
        self.gold = 100
        self.damage_amount = 2
        self.atk_range = 45

    def chk_range_player(self):
        pass

    def chk_range_barricade(self):
        pass

    def chk_range_prisoner(self):
        pass



    def update(self):
        pass

    def draw(self):
        self.font.draw(self.x - self.bg.window_left - 60, self.y + 50, '(HP : %i)' % self.hp, (255, 0, 0))
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - self.bg.window_left - 15, self.y - 18, self.x - self.bg.window_left + 12, self.y + 22

    def set_background(self, bg):
        self.bg = bg

