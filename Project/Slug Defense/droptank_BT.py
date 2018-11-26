from pico2d import *
import main_state
import random
from droptank_bomb import Bomb
import game_framework
import game_world
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode

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


class Droptank:
    def __init__(self):
        self.x, self.y = random.randint(1600, 3000), 40 + 200
        self.image = load_image('./resource/droptank/droptank.png')
        self.velocity = 0
        self.frame = 0
        self.hp = 400
        self.atk_range = 400
        self.font = load_font('./resource/font/ENCR10B.TTF', 16)
        self.chk_marking = False
        self.gold = 200
        self.build_behavior_tree()

    def build_behavior_tree(self):
        pass

    def chk_range_player(self):
        if self.x - main_state.player.x <= self.atk_range:
            self.velocity = 0
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass

    def chk_range_barricade(self):
        if self.x - main_state.barricade.x <= self.atk_range:
            self.velocity = 0
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass

    def chk_range_prisoner(self):
        if self.x - main_state.prisoner.x <= self.atk_range:
            self.velocity = 0
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass

    def move_forward(self):
        self.velocity = -RUN_SPEED_PPS
        return BehaviorTree.SUCCESS
        pass

    def fire_bomb(self):
        bomb = Bomb(self.x, self.y)
        bomb.set_background(main_state.map)
        game_world.add_object(bomb, 1)
        pass

    def update(self):
        self.bt.run()

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME *
                      game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.velocity * game_framework.frame_time
        pass

    def draw(self):
        self.image.clip_draw()
        self.font.draw(self.x - self.bg.window_left - 60, self.y + 50,
                       '(HP : %i)' % self.hp, (255, 0, 0))
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - self.bg.window_left - 33, self.y - 25, self.x - self.bg.window_left + 32, self.y + 20

    def set_background(self, bg):
        self.bg = bg
