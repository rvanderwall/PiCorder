import pygame
from pygame.locals import *
import sys
from Display import Display
from Sensor import SensorIndicator, get_temp, get_pressure, get_rh


def init():
    pygame.init()
    pygame.display.set_caption("PyGame Demo")
    display = Display()
    display.show_splash()
    return display


def get_indicators():
    indicators = []
    indicators.append(SensorIndicator("T", 55, -40.0, 120.0).set_reader(get_temp))
    indicators.append(SensorIndicator("HPA", 159, 280, 1280).set_reader(get_pressure))
    indicators.append(SensorIndicator("%RH", 262, 0, 1.00).set_reader(get_rh))
    return indicators


def game_loop(disp):
    sensor_array = get_indicators()
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
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        disp.tick_display()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    surface = init()
    game_loop(surface)
