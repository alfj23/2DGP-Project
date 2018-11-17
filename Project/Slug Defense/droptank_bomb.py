from pico2d import *
import game_world
import main_state
import game_framework

# bomb Speed

PIXEL_PER_METER = (10.0 / 0.15)
RUN_SPEED_KMPH = 30
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# bomb Speed

TIME_PER_ACTION = 1.5  # 액션 당 시간
ACTION_PER_TIME = 1.25 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

class IdleState:

    @staticmethod
    def enter(cannon, event):
        cannon.velocity += RUN_SPEED_PPS
        pass

    @staticmethod
    def exit(cannon, event):
        pass

    @staticmethod
    def do(cannon):  # 사거리 400
        cannon.x += cannon.velocity * game_framework.frame_time
        cannon.frame = (cannon.frame + FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 4

        for droptank in main_state.droptanks:
            if main_state.collide(cannon, droptank):
                droptank.hp -= cannon.damage
                game_world.remove_object(cannon)
                break
        pass

    @staticmethod
    def draw(cannon):
        cannon.image.clip_draw(int(cannon.frame) * 40, 0, 40, 30, cannon.x + 30, cannon.y + 10)
        if cannon.x > 1600 - 20:
            game_world.remove_object(cannon)  # cannon 이 범위 벗어날 시 반환됨

class Bomb:
    image = None

    def __init__(self, x=800, y=200, velocity=0.5):
        self.x, self.y, self.velocity = x, y, velocity
        self.frame = 0
        self.damage_amount = 100
        if Bomb.image == None:
            self.image = load_image('droptank_bomb.png')
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def update(self):
        self.cur_state.do(self)
        self.x -= self.velocity
        self.frame = (self.frame + 1) % 20

        if main_state.collide(self, main_state.barricade):
            game_world.remove_object(self)
            main_state.barricade.hp -= self.damage_amount

        if main_state.collide(self, main_state.player):
            game_world.remove_object(self)
            main_state.player.hp -= self.damage_amount



    def get_bb(self):
        return self.x - 47, self.y - 7, self.x - 33, self.y + 7

    def draw(self):
        self.cur_state.draw(self)
        self.image.clip_draw(self.frame * 14, 40, 14, 14, self.x-40, self.y)
        draw_rectangle(*self.get_bb())
        if self.x < 0 + 14:
            game_world.remove_object(self)  # cannon 이 범위 벗어날 시 반환됨
