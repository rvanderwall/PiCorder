import sys

import pygame
from pygame.locals import *

from Inputs import KBInput, BUTTON_QUIT
from Tricorder import build_tricorder, TricorderMode


def init():
    pygame.init()
    pygame.mixer.quit()
    pygame.display.set_caption("PyGame Demo")
    tricorder = build_tricorder()
    return tricorder


def pg_game_loop(tricorder):
    while True:
        tricorder.update_sensors()
        tricorder.update_display()

        event_list = pygame.event.get()
        print(f"Event list = {event_list}")
        for event in event_list:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            tricorder.process_inputs(event)

        tricorder.refresh()


def game_loop(tricorder):
    kb = KBInput(tricorder.logger)

    while True:
        tricorder.update_sensors()
        tricorder.update_display()

        btn_press = kb.current_button()
        print(f"Event = {btn_press}")
        tricorder.process_inputs(btn_press)
        tricorder.refresh()

        if btn_press == BUTTON_QUIT:
            pygame.quit()
            sys.exit()


if __name__ == '__main__':
    t = init()
    if t.mode == TricorderMode.LAPTOP:
        pg_game_loop(t)
    else:
        game_loop(t)
