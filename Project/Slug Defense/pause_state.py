from pico2d import *
import game_framework
import game_world
import main_state

__name__ = "pause_state"

class Pause_menu:
    def __init__(self):
        self.image = load_image('pause_menu.png')
        self.font = load_font('ENCR10B.TTF', 30)

    def update(self):
        pass

    def draw(self):
        self.image.draw(800//2, 600//2)

pause_menu = None


def enter():
    global pause_menu
    pause_menu = Pause_menu()
    game_world.add_object(pause_menu, 1)


def exit():
    game_world.remove_object(pause_menu)
    pass


def update():
    pass


def draw():
    clear_canvas()
    main_state.draw()
    pause_menu.draw
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.pop_state()


def pause():
    pass


def resume():
    pass
