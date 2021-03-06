from pico2d import *
import game_framework
import game_world
import main_state
import title_state
import world_build_state

__name__ = "pause_state"

class Pause_menu:
    def __init__(self):
        self.image = load_image('./resource/UI/pause_menu.png')
        self.font = load_font('./resource/font/ENCR10B.TTF', 18)

    def update(self):
        pass

    def draw(self):
        self.image.draw(800//2, 600//2)
        self.font.draw(380, 385, 'MENU', (0, 0, 0))
        self.font.draw(330, 320, 'X:Exit Game', (255, 255, 255))
        self.font.draw(310, 285, 'R:Restart Stage',(255, 255, 255))
        self.font.draw(310, 250, 'T:Back to title', (255, 255, 255))


pause_menu = None


def enter():
    global pause_menu
    pause_menu = Pause_menu()
    game_world.add_object(pause_menu, 2)

def exit():
    game_world.remove_object(pause_menu)


def update():
    pass


def draw():
    clear_canvas()
    main_state.draw()
    pause_menu.draw()
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.pop_state()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_x):
            game_framework.quit()

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_r):
            game_world.clear()
            world_build_state.droptanks.clear()
            world_build_state.soldiers.clear()
            if main_state.cleared_stage_count == 0:
                world_build_state.build_stage1()
            elif main_state.cleared_stage_count == 1:
                world_build_state.build_stage2()
            elif main_state.cleared_stage_count == 2:
                world_build_state.build_stage3()
            elif main_state.cleared_stage_count == 3:
                world_build_state.build_stage4()
            elif main_state.cleared_stage_count == 4:
                world_build_state.build_stage5()
            game_framework.change_state(main_state)

        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_t):
            main_state.chk_back_to_title = True
            main_state.cleared_stage_count = 0
            game_framework.pop_state()