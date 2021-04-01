import sys

import pygame
from pygame.locals import *

from Display import Display
from Inputs import Input
from Sensor import get_indicators


def init():
    pygame.init()
    pygame.display.set_caption("PyGame Demo")
    display = Display()
    display.show_splash()
    return display


def game_loop(disp):
    sensor_array = get_indicators()
    inputs = Input()
    while True:
        disp.clear()
        backgraph = pygame.image.load('./assets/backgraph.png')
        scales = pygame.image.load('./assets/background.png')

        disp.surface.blit(backgraph, (0, 0))
        disp.surface.blit(scales, (0, 0))
        for sensor in sensor_array:
            sensor.draw(disp)
        pygame.display.update()

        for event in pygame.event.get():
            print(event.type)
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            keys = inputs.get_inputs(event)

        disp.tick_display()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    surface = init()
    game_loop(surface)
