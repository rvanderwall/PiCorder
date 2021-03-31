import sys
import pygame
from pygame.locals import *

#
# General Display constants
#
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#
# Tricorder Specific Constants
#
FPS = 30
MAX_X = 320
MAX_Y = 240
upper_left = (0, 0)
lower_right = (MAX_X, MAX_Y)


class Display:
    def __init__(self):
        self.surface = pygame.display.set_mode((MAX_X, MAX_Y))
        self.frame_rate = pygame.time.Clock()


class SensorIndicator:
    def __init__(self, name:str, pos:int, min:float, max:float):
        self.name = name
        self.min = min
        self.max = max
        self.position = pos
        self.reader = None
        self.slider = pygame.image.load('assets/slider.png')
        self.graph_top = 3
        self.graph_bottom = 200
        self.scale = (self.graph_bottom - self.graph_top) / (self.max - self.min)

    def set_reader(self, reader_func):
        self.reader = reader_func
        return self

    def draw(self, disp:Display):
        val = self.reader()
        scaled = self._scale(val)
        disp.surface.blit(self.slider, (self.position, scaled))

    def _scale(self, val):
        t = self.graph_bottom - self.scale * (val - self.min)
        return t


def get_temp():
    return 30.0


def get_pressure():
    return 980.0


def get_rh():
    return .45


def init():
    pygame.init()
    pygame.display.set_caption("PyGame Demo")
    return Display()


def get_indicators():
    indicators = []
    indicators.append(SensorIndicator("T", 55, -40.0, 120.0).set_reader(get_temp))
    indicators.append(SensorIndicator("HPA", 159, 280, 1280).set_reader(get_pressure))
    indicators.append(SensorIndicator("%RH", 262, 0, 1.00).set_reader(get_rh))
    return indicators


def game_loop(disp):
    sensor_array = get_indicators()
    while True:
        disp.surface.fill(BLACK)
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
        disp.frame_rate.tick(FPS)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    surface = init()
    game_loop(surface)
