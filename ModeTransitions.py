from enum import Enum, unique
from Inputs import BUTTON_A, BUTTON_B, BUTTON_C


@unique
class Mode(Enum):
    INIT = -1
    ENV_SLIDER = 0
    ENV_TEXT = 1
    ENV_LIGHT_SOUND = 2

    PROXY_SWEEP = 3
    PROXY_RESET = 4

    POSITIONING_GRAPH = 5
    POSITIONING_3D = 6
    POSITIONING_TEXT = 7

    MOVIE_EDITH = 8
    MOVIE_SPOCK = 9

# Map from current mode to next mode given (button A, button B)
mode_transition = {}
mode_transition[Mode.ENV_SLIDER]      = (Mode.PROXY_SWEEP, Mode.ENV_TEXT)
mode_transition[Mode.ENV_TEXT]        = (Mode.PROXY_SWEEP, Mode.ENV_LIGHT_SOUND)
mode_transition[Mode.ENV_LIGHT_SOUND] = (Mode.PROXY_SWEEP, Mode.ENV_SLIDER)

mode_transition[Mode.PROXY_SWEEP] = (Mode.POSITIONING_GRAPH, Mode.PROXY_RESET)
mode_transition[Mode.PROXY_RESET] = (Mode.POSITIONING_GRAPH, Mode.PROXY_SWEEP)

mode_transition[Mode.POSITIONING_GRAPH] = (Mode.MOVIE_EDITH, Mode.POSITIONING_3D)
mode_transition[Mode.POSITIONING_3D]    = (Mode.MOVIE_EDITH, Mode.POSITIONING_TEXT)
mode_transition[Mode.POSITIONING_TEXT]  = (Mode.MOVIE_EDITH, Mode.POSITIONING_GRAPH)

mode_transition[Mode.MOVIE_EDITH] = (Mode.ENV_SLIDER, Mode.MOVIE_SPOCK)
mode_transition[Mode.MOVIE_SPOCK] = (Mode.ENV_SLIDER, Mode.MOVIE_EDITH)


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
