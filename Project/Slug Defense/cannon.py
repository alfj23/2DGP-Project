from pico2d import *
import game_world
import main_state
import game_framework
__name__ = "cannon"
# cannon Speed

PIXEL_PER_METER = (10.0 / 0.15)
RUN_SPEED_KMPH = 40
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# cannnon Speed

TIME_PER_ACTION = 0.1  # 액션 당 시간
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4


class IdleState:

    @staticmethod
    def enter(cannon, event):
        cannon.velocity += RUN_SPEED_PPS
        pass

    @staticmethod
    def exit(cannon, event):
        pass

    @staticmethod
    def do(cannon):
        cannon.x += cannon.velocity * game_framework.frame_time
        cannon.frame = (cannon.frame + FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 4

        for droptank in main_state.droptanks:
            if main_state.collide(cannon, droptank):

                if droptank.hp > 0:
                    droptank.hp -= cannon.damage_amount
                    game_world.remove_object(cannon)
                break
        for soldier in main_state.soldiers:
            if main_state.collide(cannon, soldier):

                if soldier.hp > 0:
                    soldier.hp -= cannon.damage_amount
                    game_world.remove_object(cannon)
                break
        pass

    @staticmethod
    def draw(cannon):
        cannon.image.clip_draw(int(cannon.frame) * 40, 0, 40, 30, cannon.x + 30, cannon.y + 10)
        if cannon.x > 1600 - 20:
            game_world.remove_object(cannon)  # cannon 이 범위 벗어날 시 반환됨


class Cannon:
    image = None

    def __init__(self, x=400, y=300, velocity=3):
        self.x, self.y, self.velocity = x, y, velocity
        self.frame = 0
        self.damage_amount = main_state.player.damage_amount_of_cannon
        if Cannon.image == None:
            self.image = load_image('./slug/cannon_ball.png')
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def update(self):
        self.cur_state.do(self)

    def get_bb(self):
        return self.x + 10, self.y, self.x + 45, self.y + 20

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())

