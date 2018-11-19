import game_framework
from pico2d import *
import main_state
import game_world
import random

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
        soldier.image.clip_draw(int(soldier.frame) * 40, 50, 40, 50, soldier.x, soldier.y + 2)
        pass


class DeathState:

    @staticmethod
    def enter(soldier, event):
        soldier.frame = 0
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
        soldier.image.clip_draw(int(soldier.frame) * 52, 150, 48, 80, soldier.x, soldier.y + 16)
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
        if 0 < soldier.x - main_state.player.x <= soldier.atk_range:
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
        soldier.image.clip_draw(int(soldier.frame) * 33, 0, 33, 44, soldier.x, soldier.y)
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
        if soldier.x - main_state.player.x > soldier.atk_range or soldier.x - main_state.player.x < 0:
            print(soldier.x - main_state.player.x)
            soldier.add_event(MOVE)
        soldier.frame = (soldier.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 16
        if main_state.collide(main_state.player, soldier) and int(soldier.frame) % 16 == 15:
            main_state.player.hp -= soldier.damage_amount
        pass

    @staticmethod
    def draw(soldier):
        soldier.image.clip_composite_draw(int(soldier.frame) * 80, 100, 80, 50, 3.141592, 'v', soldier.x, soldier.y + 2, 80, 50)
        pass


next_state_table = {
    IdleState: {ATTACK: AttackState, DIE: DeathState, MOVE: MoveState},
    MoveState: {ATTACK: AttackState, DIE: DeathState},
    DeathState: {},
    AttackState: {DIE: DeathState, MOVE: MoveState}
}


class Soldier:
    def __init__(self):
        self.x, self.y = random.randint(400, 800), 32 + 200
        self.image = load_image('soldier.png')
        self.velocity = 0
        self.frame = random.randint(0, 11)
        self.event_que = []
        self.cur_state = MoveState
        self.cur_state.enter(self, None)
        self.hp = 300
        self.font = load_font('ENCR10B.TTF', 16)
        self.chk_reload = False
        self.gold = 100
        self.damage_amount = 2
        self.atk_range = 45


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
        return self.x - 15, self.y - 18, self.x + 12, self.y + 22

    def draw(self):
        self.cur_state.draw(self)
        self.font.draw(self.x - 60, self.y + 50,
                       '(HP : %i)' % self.hp, (255, 0, 0))
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass