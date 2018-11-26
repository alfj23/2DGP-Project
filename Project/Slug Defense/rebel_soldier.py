from pico2d import *
import game_framework
import main_state
import game_world
from behavior_tree import BehaviorTree, LeafNode, SelectorNode, SequenceNode
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


class Soldier:
    def __init__(self):
        self.x, self.y = random.randint(1600, 4000), 32 + 200
        self.image = load_image('./resource/rebel_soldier/soldier.png')
        self.velocity = 0
        self.frame = random.randint(0, 11)
        self.hp = 200
        self.atk_cool_time = 500
        self.font = load_font('./resource/font/ENCR10B.TTF', 16)
        self.chk_stabbing = False
        self.gold = 100
        self.damage_amount = 2
        self.atk_range = 45
        self.build_behavior_tree()
        self.num_of_frame = 0

    def build_behavior_tree(self):
        pass

    def chk_range_player(self):
        pass

    def chk_range_barricade(self):
        pass

    def chk_range_prisoner(self):
        pass

    def ready_to_atk(self):
        pass

    def attack(self):
        pass

    def move_forward(self):
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

