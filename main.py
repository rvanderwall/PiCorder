import sys

import pygame
from pygame.locals import *

from Display import Display
from Inputs import Input
from Sensor import get_sensor_array


def init():
    pygame.init()
    pygame.display.set_caption("PyGame Demo")
    display = Display()
    display.show_splash()
    return display


def game_loop(disp):
    sensor_array = get_sensor_array()
    inputs = Input()
    while True:
        for sensor_type in sensor_array:
            sensor = sensor_array[sensor_type]
            sensor.update_value()

        disp.update(sensor_array)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            key = inputs.get_inputs(event)
            disp.switch_display_modes(key)

        disp.tick_display()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    surface = init()
    game_loop(surface)
