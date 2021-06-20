import sys

import pygame
from pygame.locals import *

from Tricorder import build_tricorder


def init():
    pygame.init()
    pygame.mixer.quit()
    pygame.display.set_caption("PyGame Demo")
    tricorder = build_tricorder()
    return tricorder


def game_loop(tricorder):
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


if __name__ == '__main__':
    t = init()
    game_loop(t)
