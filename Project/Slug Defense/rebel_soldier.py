from pico2d import *
import game_framework
import main_state
import game_world
from behavior_tree import BehaviorTree, LeafNode, SelectorNode, SequenceNode
import random

__name__ = "rebel_soldier"
# soldier Speed

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 12
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# soldier Speed

TIME_PER_ACTION = 0.5  # 액션 당 시간
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Soldier:
    def __init__(self):
        self.x, self.y = random.randint(1200, 1600), 32 + 200
        self.image = load_image('./resource/rebel_soldier/soldier.png')
        self.velocity = 0
        self.frame = random.randint(0, 11)
        self.hp_amount = 200
        self.atk_cool_time = 300
        self.font = load_font('./resource/font/ENCR10B.TTF', 16)
        self.chk_stabbing = False
        self.chk_ready_to_atk = False
        self.chk_dying = False
        self.gold = 100
        self.damage_amount = 2
        self.atk_range = 35
        self.build_behavior_tree()
        self.num_of_frame = 0

    def build_behavior_tree(self):
        chk_range_player_node = LeafNode("chk_range_player", self.chk_range_player)
        chk_range_barricade_node = LeafNode("chk_range_barricade", self.chk_range_barricade)
        chk_range_prisoner_node = LeafNode("chk_range_prisoner", self.chk_range_prisoner)
        ready_to_atk_node = LeafNode("ready_to_atk", self.ready_to_atk)
        stabbing_node = LeafNode("stabbing", self.stabbing)
        move_forward_node = LeafNode("move_forward", self.move_forward)
        atk_player_node = SequenceNode("atk_player")
        atk_player_node.add_children(chk_range_player_node, ready_to_atk_node, stabbing_node)
        atk_barricade_node = SequenceNode("atk_barricade")
        atk_barricade_node.add_children(chk_range_barricade_node, ready_to_atk_node, stabbing_node)
        atk_prisoner_node = SequenceNode("atk_prisoner")
        atk_prisoner_node.add_children(chk_range_prisoner_node, ready_to_atk_node, stabbing_node)
        attack_node = SelectorNode("attack")
        attack_node.add_children(atk_prisoner_node, atk_barricade_node, atk_player_node)
        attack_move_node = SelectorNode("attack_move")
        attack_move_node.add_children(attack_node, move_forward_node)
        self.bt = BehaviorTree(attack_move_node)

    def chk_range_player(self):
        if main_state.barricade.hp_amount <= 0:
            return BehaviorTree.FAIL
        elif 0 < self.x - main_state.player.x < self.atk_range:
            self.velocity = 0
            return BehaviorTree.SUCCESS
        else:
            return  BehaviorTree.FAIL

    def chk_range_barricade(self):
        if 0 < self.x - main_state.barricade.x < self.atk_range:
            self.velocity = 0
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def chk_range_prisoner(self):
        if 0 < self.x - main_state.prisoner.x < self.atk_range:
            self.velocity = 0
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def ready_to_atk(self):
        self.chk_ready_to_atk = True
        self.chk_stabbing = False
        self.atk_cool_time -= 1
        if self.atk_cool_time <= 0:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def stabbing(self):
        atk_objects = [main_state.prisoner, main_state.barricade, main_state.player]
        self.chk_stabbing = True
        self.chk_ready_to_atk = False
        if int(self.frame) % 16 == 15:
            for atk_object in atk_objects:
                if main_state.collide(self, atk_object):
                    atk_object.hp_amount -= self.damage_amount
                    self.atk_cool_time = 300
                    return BehaviorTree.SUCCESS
        else:
            BehaviorTree.RUNNING

    def move_forward(self):
        self.chk_ready_to_atk = self.chk_stabbing = False
        self.velocity = -RUN_SPEED_PPS
        return BehaviorTree.SUCCESS

    def update(self):
        self.bt.run()

        if self.velocity == 0:
            if self.chk_ready_to_atk:
                self.num_of_frame = 4
            elif self.chk_stabbing:
                self.num_of_frame = 16
        else:
            self.num_of_frame = 12
        if self.hp_amount <= 0:
            if not self.chk_dying:
                self.frame = 0
                self.chk_dying = True
            self.velocity = 0
            self.num_of_frame = 22
            if int(self.frame) % 22 == 21:
                game_world.remove_object(self)
                self.x = -100
                main_state.left_wave_amount -= 1
                main_state.gold += self.gold

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)\
                     % self.num_of_frame
        self.x += self.velocity * game_framework.frame_time

    def draw(self):
        cx = self.x - self.bg.window_left
        if self.velocity == 0:
            if self.chk_ready_to_atk:
                self.image.clip_draw(int(self.frame) * 40, 50, 40, 50, cx, self.y)
            elif self.chk_stabbing:
                self.image.clip_composite_draw(int(self.frame) * 80, 100, 80, 50, 3.141592, 'v', cx, self.y + 2, 80, 50)
        else:
            self.image.clip_draw(int(self.frame) * 33, 0, 33, 44, cx, self.y)
        if self.hp_amount <= 0:
            self.image.clip_draw(int(self.frame) * 52, 150, 48, 80, cx, self.y + 16)

        self.font.draw(self.x - self.bg.window_left - 60, self.y + 50, '(HP : %i)' % self.hp_amount, (255, 0, 0))
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - self.bg.window_left - 15, self.y - 18, self.x - self.bg.window_left + 12, self.y + 22

    def set_background(self, bg):
        self.bg = bg

