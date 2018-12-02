from pico2d import *
import main_state
import random
from droptank_bomb import Bomb
import game_framework
import game_world
from behavior_tree import BehaviorTree, SelectorNode, SequenceNode, LeafNode

__name__ = "droptank"

# droptank Speed

PIXEL_PER_METER = (10.0 / 0.4)  # 10 pixel = 30cm
RUN_SPEED_KMPH = 20
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# droptank Speed

TIME_PER_ACTION = 1.2  # 액션 당 시간
ACTION_PER_TIME = 1.8 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Droptank:
    image = None
    def __init__(self, x=0, hp_amount=0,damage_amount=0, gold=0):
        self.x, self.y = x * PIXEL_PER_METER, 40 + 200
        if Droptank.image == None:
            Droptank.image = load_image('./resource/droptank/droptank.png')
        self.velocity = 0
        self.frame = 0
        self.hp_amount = hp_amount
        self.atk_range = 400
        self.font = load_font('./resource/font/ENCR10B.TTF', 16)
        self.chk_marking = False
        self.chk_firing = False
        self.chk_dying = False
        self.gold = gold
        self.timer = 800
        self.build_behavior_tree()
        self.num_of_frame = 0
        self.damage_amount = damage_amount

    def __getstate__(self):
        state = {'x': self.x, 'hp_amount': self.hp_amount, 'damage_amount': self.damage_amount, 'gold': self.gold}
        return state

    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)

    def build_behavior_tree(self):
        chk_range_player_node = LeafNode("chk_range_player", self.chk_range_player)
        chk_range_barricade_node = LeafNode("chk_range_barricade", self.chk_range_barricade)
        chk_range_prisoner_node = LeafNode("chk_range_prisoner", self.chk_range_prisoner)
        move_forward_node = LeafNode("move_forward", self.move_forward)
        marking_node = LeafNode("marking", self.marking)
        fire_bomb_node = LeafNode("fire_bomb", self.fire_bomb)
        attack_player_node = SequenceNode("attack_player")
        attack_player_node.add_children(chk_range_player_node, marking_node, fire_bomb_node)
        attack_barricade_node = SequenceNode("attack_barricade")
        attack_barricade_node.add_children(chk_range_barricade_node, marking_node, fire_bomb_node)
        attack_prisoner_node = SequenceNode("attack_prisoner")
        attack_prisoner_node.add_children(chk_range_prisoner_node, marking_node, fire_bomb_node)
        attack_node = SelectorNode("attack")
        attack_node.add_children(attack_player_node, attack_barricade_node, attack_prisoner_node)
        attack_move_node = SelectorNode("attack_move_node")
        attack_move_node.add_children(attack_node, move_forward_node)
        self.bt = BehaviorTree(attack_move_node)

    def chk_range_player(self):
        if 0 < self.x - main_state.player.x <= self.atk_range:
            self.velocity = 0
            if main_state.player.hp_amount <= 0:  # 플레이어 체력 0이하시 다음 우선 공격순위로 공격목표 변경
                return BehaviorTree.FAIL
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def chk_range_barricade(self):
        if 0 < self.x - main_state.barricade.x <= self.atk_range:
            self.velocity = 0
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def chk_range_prisoner(self):
        if 0 < self.x - main_state.prisoner.x <= self.atk_range:
            self.velocity = 0
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_forward(self):
        self.velocity = -RUN_SPEED_PPS
        self.chk_marking = False
        return BehaviorTree.SUCCESS

    def fire_bomb(self):
        self.chk_marking = False
        self.chk_firing = True
        if int(self.frame) % 8 == 7:
            bomb = Bomb(self.x, self.y, self.damage_amount)
            bomb.set_background(main_state.map)
            game_world.add_object(bomb, 1)
            self.timer = 200
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def marking(self):
        self.chk_marking = True
        self.chk_firing = False
        self.timer -= 1
        if self.timer <= 0:
            return BehaviorTree.SUCCESS
        elif self.x - main_state.player.x > self.atk_range:
            return BehaviorTree.FAIL
        else:
            return BehaviorTree.RUNNING

    def update(self):
        self.bt.run()

        if self.velocity == 0:
            if self.chk_marking:  # 아이들 애니메이션.
                self.num_of_frame = 2
            elif self.chk_firing:  # 공격 애니메이션.
                self.num_of_frame = 8

        else:  # 이동 애니메이션 출력
            self.num_of_frame = 3

        if self.hp_amount <= 0:  # 사망 애니메이션
            self.velocity = 0
            if not self.chk_dying:
                self.frame = 0
                self.chk_dying = True
            self.num_of_frame = 7
            if int(self.frame) % 7 == 6:
                game_world.remove_object(self)
                self.x = -100
                main_state.left_wave_amount -= 1
                main_state.gold += self.gold

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % self.num_of_frame
        self.x += self.velocity * game_framework.frame_time

    def draw(self):
        cx = self.x - self.bg.window_left
        if self.velocity == 0:
            if self.chk_marking:
                self.image.clip_draw(int(self.frame) * 100, 240, 100, 80, cx, self.y)
            elif self.chk_firing and not self.chk_dying:
                self.image.clip_draw(int(self.frame) * 100, 80, 100, 80, cx, self.y)
        else:
            self.image.clip_draw(int(self.frame) * 100, 160, 100, 80, cx, self.y)
        if self.chk_dying:
            self.image.clip_draw(int(self.frame) * 100, 0, 100, 80, cx, self.y)
        self.font.draw(self.x - self.bg.window_left - 60, self.y + 50,
                       '(HP : %i)' % self.hp_amount, (255, 0, 0))

    def get_bb(self):
        return self.x - self.bg.window_left - 33, self.y - 25, self.x - self.bg.window_left + 32, self.y + 20

    def set_background(self, bg):
        self.bg = bg

