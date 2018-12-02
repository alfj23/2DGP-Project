from pico2d import *
__name__ = "map"


class Map:
    def __init__(self):
        self.image = load_image('./resource/map/maaap.png')
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.w = self.image.w
        self.h = 220 * 1.367


    def set_center_object(self, player):
        self.center_object = player

    def update(self):
        self.window_left = clamp(0, int(self.center_object.x) - self.canvas_width // 2, self.w - self.canvas_width)
        self.window_bottom = clamp(0, int(self.center_object.y) - self.canvas_height // 2, self.h - self.canvas_height)
        pass

    def get_bb(self):
        return self.window_left - 1600, self.window_bottom + 200, self.window_left + 1600, self.window_bottom + 215

    def draw(self):
        #self.image.draw_to_origin(self.x - 2, self.y, 1600 * 1.367, 220 * 1.367)  # 맵 높이 300으로 늘리기 위해 배율을 1.367로 하였음.
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom,
                                      self.canvas_width, self.canvas_height - 300, -2, 200)
        #draw_rectangle(*self.get_bb())
