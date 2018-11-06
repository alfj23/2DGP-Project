import game_framework
from pico2d import *
import main_state
from droptank_bomb import  Bomb
import game_world
# droptank Speed

PIXEL_PER_METER = (10.0 / 0.5)
RUN_SPEED_KMPH = 20
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# droptank Speed

TIME_PER_ACTION = 1.5  # 액션 당 시간
ACTION_PER_TIME = 1.25 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


# droptank Events



# droptank States


class IdleState:

    @staticmethod
    def enter(droptank, event):
        pass

    @staticmethod
    def exit(droptank):
        droptank.fire_bomb()
        pass

    @staticmethod
    def do(droptank): # 사거리 800
        if droptank.hp <= 0:
            droptank.chk_die = True
        if droptank.chk_die == False:
            if droptank.x - main_state.player.x <= 400:
                droptank.chk_range = True
                droptank.velocity = 0
                droptank.frame = (droptank.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
            elif droptank.x - main_state.player.x > 400:
                droptank.chk_range = False
                droptank.velocity = RUN_SPEED_PPS
                droptank.frame = (droptank.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
                droptank.x -= droptank.velocity * game_framework.frame_time
        elif droptank.chk_die:
            droptank.frame = (droptank.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7
            droptank.chk_time = True
            if droptank.chk_time:
                game_world.remove_object(droptank)
            pass

    @staticmethod
    def draw(droptank):
        if droptank.chk_range:
            droptank.image.clip_draw(int(droptank.frame) * 100, 80, 100, 80, droptank.x, droptank.y)
        else:
            droptank.image.clip_draw(int(droptank.frame) * 100, 160, 100, 80, droptank.x, droptank.y)
        if droptank.chk_die:
            droptank.image.clip_draw(int(droptank.frame) * 100, 0, 100, 80, droptank.x, droptank.y)

class Droptank:
    def __init__(self):
        self.x, self.y = 1600 - 100, 40
        self.image = load_image('droptank.png')
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.chk_range = False
        self.chk_die = False
        self.hp = 400
        self.chk_atk = False
        self.chk_time = False
        self.font = load_font('ENCR10B.TTF', 16)

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
        return self.x - 33, self.y - 30, self.x + 32, self.y + 20

    def fire_bomb(self):
        bomb = Bomb(self.x, self.y)
        game_world.add_object(bomb, 1)
        pass

    def draw(self):
        self.cur_state.draw(self)
        self.font.draw(self.x - 60, self.y + 50,
                       '(HP : %i)' % self.hp, (255, 0, 0))
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
       pass