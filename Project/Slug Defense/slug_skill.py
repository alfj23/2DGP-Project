from pico2d import *
import game_world
import main_state
import world_build_state
import game_framework

#missile Speed

PIXEL_PER_METER = (10.0 / 0.20)
RUN_SPEED_KMPH = 30
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

#missile Action Speed

TIME_PER_ACTION = 0.1  # 액션 당 시간
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

#missile event
EXPLORE = range(1)

class FallingState:
    @staticmethod
    def enter(missile, event):
        missile.velocity -= RUN_SPEED_PPS

    @staticmethod
    def exit(missile, event):
        pass

    @staticmethod
    def do(missile):
        missile.y += missile.velocity * game_framework.frame_time
        missile.frame = (missile.frame + FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 13
        if main_state.collide(main_state.map, missile):
            missile.add_event(EXPLORE)

    @staticmethod
    def draw(missile):
        cx = missile.x - missile.bg.window_left
        missile.image.clip_draw(int(missile.frame)*40, 0, 40, 100, cx, missile.y)


class ExploringState:
    @staticmethod
    def enter(missile, event):
        missile.frame = 0
        missile.velocity = 0
        missile.explode()

    @staticmethod
    def exit(missile, event):
        pass

    @staticmethod
    def do(missile):
        missile.frame = (missile.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 24
        if int(missile.frame) % 24 == 23:
            game_world.remove_object(missile)
        for droptank in world_build_state.droptanks:
            if main_state.collide(droptank, missile):
                if droptank.hp_amount > 0:
                    droptank.hp_amount -= missile.damage_amount

        for soldier in world_build_state.soldiers:
            if main_state.collide(soldier, missile):
                if soldier.hp_amount > 0:
                    soldier.hp_amount -= missile.damage_amount

    @staticmethod
    def draw(missile):
        cx = missile.x - missile.bg.window_left
        missile.image.clip_draw(int(missile.frame)*150, 100, 150, 160, cx, missile.y)


next_state_table = {
    FallingState: {EXPLORE: ExploringState},
    ExploringState: {}
}


class Missile:
    image = None
    bgm = None

    def __init__(self, x=0, y=0):
        if Missile.image == None:
            Missile.image = load_image('./resource/skill/skill.png')
        if Missile.bgm == None:
            Missile.bgm = load_wav('./resource/sounds/explode.wav')
            Missile.bgm.set_volume(20)
        self.x, self.y = x * PIXEL_PER_METER, y * PIXEL_PER_METER
        self.velocity = 0
        self.frame = 0
        self.damage_amount = main_state.player.damage_amount_of_skill
        self.event_que = []
        self.cur_state = FallingState
        self.cur_state.enter(self, None)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def set_background(self, bg):
        self.bg = bg

    def explode(self):
        self.bgm.play(1)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def get_bb(self):
        return self.x - 50 - self.bg.window_left, self.y - 60, self.x + 50 - self.bg.window_left, self.y + 30

    def draw(self):
        self.cur_state.draw(self)