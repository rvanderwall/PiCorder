import pygame
from Display import Display


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

