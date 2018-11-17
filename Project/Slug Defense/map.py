from pico2d import *

class Map:
    def __init__(self):
        self.image = load_image('maaap.png')
        self.x, self.y = 0, 200

    def update(self):
        pass

    def get_bb(self):
        return self.x, self.y, self.x + 799, self.y + 15

    def draw(self):
        self.image.draw_to_origin(self.x - 2, self.y, 1600 * 1.367, 220 * 1.367)  # 맵 높이 300으로 늘리기 위해 배율을 1.367로 하였음.
        draw_rectangle(*self.get_bb())
