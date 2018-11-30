from pico2d import *
import game_world
import main_state
import game_framework
name = "droptank_bomb"
# bomb Speed

PIXEL_PER_METER = (10.0 / 0.15)
RUN_SPEED_KMPH = 10
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# bomb Speed

TIME_PER_ACTION = 0.5  # 액션 당 시간
ACTION_PER_TIME = 1 / TIME_PER_ACTION
FRAMES_PER_ACTION = 20

# bomb Events

LANDING, EXPLOSION = range(2)


class FiredState:

    @staticmethod
    def enter(bomb, event):
        bomb.velocity -= RUN_SPEED_PPS
        pass

    @staticmethod
    def exit(bomb, event):
        pass

    @staticmethod
    def do(bomb):  # 사거리 400
        bomb.x += bomb.velocity * game_framework.frame_time
        bomb.frame = (bomb.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 20

        if main_state.collide(bomb, main_state.barricade):
            game_world.remove_object(bomb)
            main_state.barricade.hp_amount -= bomb.damage_amount

        if main_state.collide(bomb, main_state.player):
            game_world.remove_object(bomb)
            main_state.player.hp_amount -= bomb.damage_amount

        if main_state.collide(bomb, main_state.prisoner):
            game_world.remove_object(bomb)
            main_state.prisoner.hp_amount -= bomb.damage_amount

    @staticmethod
    def draw(bomb):
        cx = bomb.x - bomb.bg.window_left
        bomb.image.clip_draw(int(bomb.frame) * 14, 40, 14, 14, cx - 40, bomb.y)
        if bomb.x < 0 + 14:
            game_world.remove_object(bomb)  # cannon 이 범위 벗어날 시 반환됨


class LandedState:
    @staticmethod
    def enter(bomb, event):
        pass

    @staticmethod
    def exit(bomb, event):
        pass

    @staticmethod
    def do(bomb):
        pass

    @staticmethod
    def draw(bomb):
        pass


class ExplodedState:
    @staticmethod
    def enter(bomb, event):
        pass

    @staticmethod
    def exit(bomb, event):
        pass

    @staticmethod
    def do(bomb):
        pass

    @staticmethod
    def draw(bomb):
        pass


next_state_table ={
    FiredState: {},
    LandedState: {},
    ExplodedState: {}
}

class Bomb:
    image = None

    def __init__(self, x=400, y=300, damage_amount=50,velocity=1):
        self.x, self.y,self.damage_amount, self.velocity = x, y,damage_amount, velocity
        self.frame = 0
        if Bomb.image == None:
            self.image = load_image('./resource/droptank/droptank_bomb.png')
        self.event_que = []
        self.cur_state = FiredState
        self.cur_state.enter(self, None)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def set_background(self, bg):
        self.bg = bg

    def get_bb(self):
        return self.x - self.bg.window_left - 47, self.y - 7, self.x - self.bg.window_left - 33, self.y + 7

    def draw(self):
        self.cur_state.draw(self)
        draw_rectangle(*self.get_bb())
