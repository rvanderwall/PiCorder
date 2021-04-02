from enum import Enum, unique
from Inputs import BUTTON_A, BUTTON_B, BUTTON_C


@unique
class Mode(Enum):
    INIT = -1
    ENV_SLIDER = 0
    ENV_GRAPH = 2

    LIGHT_SOUND_SLIDER = 3
    LIGHT_SOUND_GRAPH = 5

    PROXY_SWEEP = 6
    PROXY_RESET = 7

    POSITIONING_GRAPH = 8
    POSITIONING_3D = 9

    MOVIE_EDITH = 11
    MOVIE_SPOCK = 12


# Map from current mode to next mode given (button A, button B)
mode_transition = {Mode.ENV_SLIDER:  (Mode.LIGHT_SOUND_SLIDER, Mode.ENV_GRAPH),
                   Mode.ENV_GRAPH:   (Mode.LIGHT_SOUND_SLIDER, Mode.ENV_SLIDER),

                   Mode.LIGHT_SOUND_SLIDER: (Mode.PROXY_SWEEP, Mode.LIGHT_SOUND_GRAPH),
                   Mode.LIGHT_SOUND_GRAPH: (Mode.PROXY_SWEEP, Mode.LIGHT_SOUND_SLIDER),

                   Mode.PROXY_SWEEP: (Mode.POSITIONING_GRAPH, Mode.PROXY_RESET),
                   Mode.PROXY_RESET: (Mode.POSITIONING_GRAPH, Mode.PROXY_SWEEP),

                   Mode.POSITIONING_GRAPH: (Mode.MOVIE_EDITH, Mode.POSITIONING_3D),
                   Mode.POSITIONING_3D:    (Mode.MOVIE_EDITH, Mode.POSITIONING_GRAPH),

                   Mode.MOVIE_EDITH: (Mode.ENV_SLIDER, Mode.MOVIE_SPOCK),
                   Mode.MOVIE_SPOCK: (Mode.ENV_SLIDER, Mode.MOVIE_EDITH)}


class ModeMap:
    def __init__(self):
        self.current_mode = Mode.INIT

    def switch_mode(self, button):
        if button is None:
            return

        if button == BUTTON_C:
            self.current_mode = Mode.INIT
            return

        (mode_a, mode_b) = mode_transition[self.current_mode]
        if button == BUTTON_A:
            self.current_mode = mode_a
        elif button == BUTTON_B:
            self.current_mode = mode_b

    def show_mode(self):
        print(f"Current mode: {self.current_mode}")
