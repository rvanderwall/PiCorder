from math import sin, cos
from time import sleep
import os
import sys

import pygame
from pygame.locals import *

#
# General Display constants
#
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
SF_YELLOW = (250, 225, 88)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#
# Display Specific Constants
#
FPS = 30
MAX_X = 320
MAX_Y = 240
upper_left = (0, 0)
lower_right = (MAX_X, MAX_Y)

COUNTER = 0

class IndicatorSensor:
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

    def draw(self, surface):
        val = self.reader()
        scaled = self._scale(val)
        surface.blit(self.slider, (self.position, scaled))

    def _scale(self, val):
        t = self.graph_bottom - self.scale * (val - self.min)
        return t


class GraphSensor:
    def __init__(self, name:str, min:float, max:float, color:tuple):
        self.name = name
        self.color = color
        self.min = min
        self.max = max
        self.graph_top = 3
        self.graph_bottom = 200
        self.offset = 15
        self.num_points = 290
        self.scale = (self.graph_bottom - self.graph_top) / (self.max - self.min)
        self.reader = None
        self.history = []
        mid = self._scale((max + min) / 2)
        for _ in range(self.num_points):
            self.history.append(mid)

    def set_reader(self, reader_func):
        self.reader = reader_func
        return self

    def draw(self, surface):
        val = self.reader()
        scaled = self._scale(val)
        self.history.append(scaled)
        self.history.pop(0)
        data = []
        for x in range(len(self.history)):
            data.append((x+self.offset, self.history[x]))
        pygame.draw.lines(surface, self.color, False, data, 3)

    def _scale(self, val):
        t = self.graph_bottom - self.scale * (val - self.min)
        return t


def get_temp():
    return 30.0 + 5 * sin(COUNTER / 10)


def get_pressure():
    return 980.0 + 50 * cos(COUNTER / 20)


def get_rh():
    return .45


def init():
    pygame.init()
    pygame.display.set_caption("PyGame Demo")
    return


def get_graphs():
    graphs = []
    graphs.append(GraphSensor("T", -40.0, 120.0, RED).set_reader(get_temp))
    graphs.append(GraphSensor("HPA", 280.0, 1280, SF_YELLOW).set_reader(get_pressure))
    graphs.append(GraphSensor("%RH", 0.0, 1.00, WHITE).set_reader(get_rh))
    return graphs


def get_indicators():
    indicators = []
    indicators.append(IndicatorSensor("T", 55, -40.0, 120.0).set_reader(get_temp))
    indicators.append(IndicatorSensor("HPA", 159, 280, 1280).set_reader(get_pressure))
    indicators.append(IndicatorSensor("%RH", 262, 0, 1.00).set_reader(get_rh))
    return indicators


def show_splash(surface):
    surface.fill(BLACK)
    logo = pygame.image.load('assets/PicorderLogoSmall.png')
    surface.blit(logo, (90, 0))
    font = "assets/babs.otf"
    font_size = 33
    disp_font = pygame.font.Font(font, font_size)
    label = disp_font.render("StarFleet Tricorder TR-109", True, SF_YELLOW)
    surface.blit(label, (10, 180))
    pygame.display.update()
    for i in range(2):
        pygame.event.get()
        sleep(1)


def game_loop():
    global COUNTER
    surface = pygame.display.set_mode((MAX_X, MAX_Y))
    show_splash(surface)
    frame_rate = pygame.time.Clock()
    indicator_array = get_indicators()
    graph_array = get_graphs()
    grid = pygame.image.load('./assets/backgraph.png')
    scales = pygame.image.load('./assets/background.png')
    # ek_movie = pygame.movie.Movie('./asset/ekmd.mov')

    do_indicators = False
    do_graphs = True
    do_vid = False

    while True:
        COUNTER += 1
        if do_indicators:
            surface.fill(BLACK)
            surface.blit(scales, (0, 0))
            for sensor in indicator_array:
                sensor.draw(surface)
            pygame.display.update()

        if do_graphs:
            surface.fill(BLACK)
            surface.blit(grid, (0, 0))
            for graph in graph_array:
                graph.draw(surface)
            pygame.display.update()

        if do_vid:
            os.system("omxplayer assets/ekmd.mov")

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                print(f"Pressed {event.key} key")

        frame_rate.tick(FPS)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    init()
    game_loop()
