from enum import Enum, unique
from math import sin, cos
import time
import pygame
from Display import Display
from Display import RED, SF_YELLOW, WHITE


@unique
class SENSOR_TYPES(Enum):
    TEMP = 1
    PRESSURE = 2
    HUMIDITY = 3


def get_sensor_array():
    sensor_array = {
        SENSOR_TYPES.TEMP:     (Sensor("T", -40.0, 120.0).set_pos(55).set_color(RED)
                                .set_reader(get_temp)),
        SENSOR_TYPES.PRESSURE: (Sensor("HPA", 280, 1280).set_pos(159).set_color(SF_YELLOW)
                                .set_reader(get_pressure)),
        SENSOR_TYPES.HUMIDITY: (Sensor("%RH", 0, 1.00).set_pos(262).set_color(WHITE)
                                .set_reader(get_rh))}
    return sensor_array


class Sensor:
    def __init__(self, name:str, min:float, max:float):
        self.name = name
        self.min = min
        self.max = max
        self.reader = None

        # Rendering attributes
        self.position = 0
        self.graph_top = 3
        self.graph_bottom = 200
        self.graph_offset = 15
        self.scale = (self.graph_bottom - self.graph_top) / (self.max - self.min)

        self.slider = pygame.image.load('assets/slider.png')

        self.color = RED
        self.num_points = 290
        self.cur_val = 0
        self.cur_scaled = 0
        self.history = []
        mid = self._scale((max + min) / 2)
        for _ in range(self.num_points):
            self.history.append(mid)

    def set_pos(self, pos):
        self.position = pos
        return self

    def set_color(self, color):
        self.color = color
        return self

    def set_reader(self, reader_func):
        self.reader = reader_func
        return self

    def update_value(self):
        val = self.reader()
        self.cur_val = val
        self.cur_scaled = self._scale(val)
        self.history.append(self.cur_scaled)
        self.history.pop(0)

    def render_as_pointer(self, disp:Display):
        disp.surface.blit(self.slider, (self.position, self.cur_scaled))

    def render_as_graph(self, disp: Display):
        width = 3
        data = []
        for x in range(len(self.history)):
            data.append((x+self.graph_offset, self.history[x]))
        pygame.draw.lines(disp.surface, self.color, False, data, width)

    def _scale(self, val):
        t = self.graph_bottom - self.scale * (val - self.min)
        return t


def get_temp():
    ts = time.time() * 10
    return 30.0 + 5 * sin(ts / 10)


def get_pressure():
    ts = time.time() * 10
    return 980.0 + 50 * cos(ts / 20)


def get_rh():
    return .45

