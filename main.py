import sys

import pygame
from pygame.locals import *

from Inputs import get_mode_select, KeyboardInput, ButtonInput, BUTTON_QUIT
from Tricorder import build_tricorder


def init():
    pygame.init()
    pygame.mixer.quit()
    pygame.display.set_caption("Tricorder")
    hw_mode = get_mode_select()
    return build_tricorder(hw_mode)


def pg_game_loop(tricorder):
    inp = KeyboardInput(tricorder.logger)
    tricorder.refresh()
    while True:
        tricorder.update_sensors()
        tricorder.update_display()

        event_list = pygame.event.get()
        for event in event_list:
            key = inp.get_button_press(event)
            if event.type == QUIT or key == BUTTON_QUIT:
                pygame.quit()
                sys.exit()

            tricorder.process_button_press(key)

        tricorder.refresh()


def game_loop(tricorder):
    kb = ButtonInput(tricorder.logger)
    tricorder.refresh()
    while True:
        tricorder.update_sensors()
        tricorder.update_display()

        btn_press = kb.get_button_press()
        if btn_press == BUTTON_QUIT:
            pygame.quit()
            sys.exit()

        tricorder.process_button_press(btn_press)
        tricorder.refresh()


def main():
    t = init()
    if t.mode.TFT:
        # Can't use pygame loop without display
        game_loop(t)
    else:
        pg_game_loop(t)


if __name__ == '__main__':
    main()

