import sys

import pygame
from pygame.locals import *

from Inputs import Input, KBInput, BUTTON_QUIT
from Tricorder import build_tricorder, TricorderMode


def init():
    pygame.init()
    pygame.mixer.quit()
    pygame.display.set_caption("PyGame Demo")
    tricorder = build_tricorder()
    return tricorder


def pg_game_loop(tricorder):
    input = Input(tricorder.logger)
    while True:
        tricorder.update_sensors()
        tricorder.update_display()

        event_list = pygame.event.get()
        for event in event_list:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            key = input.get_button_press(event)
            tricorder.process_button_press(key)

        tricorder.refresh()


def game_loop(tricorder):
    kb = KBInput(tricorder.logger)
    while True:
        tricorder.update_sensors()
        tricorder.update_display()

        btn_press = kb.get_button_press()
        if btn_press == BUTTON_QUIT:
            pygame.quit()
            sys.exit()

        tricorder.process_button_press(btn_press)
        tricorder.refresh()


if __name__ == '__main__':
    t = init()
    if t.mode == TricorderMode.LAPTOP:
        pg_game_loop(t)
    else:
        game_loop(t)
