from pico2d import *
import random

global running

class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(800//2, 30)


class Player:
    def __init__(self):
        self.x, self.y = 0, 70
        self.frame = 0
        self.image = load_image('finaltest.png')
        self.dir = 0
        self.cannon = 0
        self.frame1 = 0

    def moving(self):
        if self.dir == 1 or self.dir == -1:
            self.frame = (self.frame + 1) % 18
            self.x += self.dir * 7
        elif self.dir == 0:
            self.frame = (self.frame + 1) % 3
            self.x = self.x - 0
        elif self.cannon == 1:
            self.frame1 = (self.frame1 + 1) % 23

    def draw(self):
        if self.dir == 0:
            self.image.clip_draw(self.frame * 80, 160, 80-3, 80, self.x, self.y)
        elif self.dir == 1 or self.dir == -1:
            self.image.clip_draw(self.frame * 80, 80, 80-3, 80, self.x, self.y)

        if self.cannon == 1:  # 포탄 발사
                self.image.clip_draw(self.frame1 * 140, 0, 140, 80, self.x+25, self.y)


class Cannon:
    def __init__(self):
        self.x, self.y = slug.x+40, slug.y+10
        self.frame = 0
        self.image = load_image('cannon_ball.png')
        self.shot = False

    def shoot(self):
        self.x += 10
        self.frame = (self.frame + 1) % 4
        if self.x >= 799-10:
            self.shot = False
            self.x = slug.x+40
            self.frame = 0
        print(self.x)

    def draw(self):
        if self.shot:
            self.image.clip_draw(self.frame * 40, 0, 40, 30, self.x, self.y)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:  # 우측화살표 키
                slug.dir = 1
            elif event.key == SDLK_LEFT:  # 좌측화살표 키
                slug.dir = -1
            elif event.key == SDLK_ESCAPE:  # ESC 키
                running = False
            elif event.key == SDLK_x:  # x키 공격
                slug.cannon = 1
                slug.dir = -2
                ball.shot = True

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                slug.dir = 0
            elif event.key == SDLK_LEFT:
                slug.dir = 0
            elif event.key == SDLK_x:
                slug.cannon = 0
                slug.dir = 0

# initialization code

running = True
open_canvas()
slug = Player()
grass = Grass()
ball = [Cannon() for i in range(10)]

# game main loop code

while running:
    handle_events()
    clear_canvas()
    get_events()
    slug.moving()
    grass.draw()
    slug.draw()
    for cannon in ball:
        cannon.shoot()
        cannon.draw()
    else:
        ball.shoot()
    update_canvas()

    delay(0.02)


# finalization code

close_canvas()
