import game_framework
import pico2d
import start_state
import title_state
import main_state
import pause_state
__name__ = "mygame"
pico2d.open_canvas(800, 600)
game_framework.run(title_state)
pico2d.close_canvas()