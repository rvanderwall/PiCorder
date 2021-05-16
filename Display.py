import pygame

from Assets import Assets
from ModeTransitions import DisplayMode
from Indicator import Indicator
from Records import Record

#
# General Display constants
#
RED = (255,   0,   0)
GREEN = (0,   255,   0)
BLUE = (0,     0, 255)
ORANGE = (255, 140,   0)
SF_YELLOW = (250, 225,  88)
BLACK = (0,     0,   0)
WHITE = (255, 255, 255)

#
# Tricorder display Constants
#
FPS = 30
WIDTH = 320
HEIGHT = 240
upper_left = (0, 0)
lower_right = (WIDTH, HEIGHT)


class Display:
    def __init__(self, assets: Assets):
        self._surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self._frame_rate = pygame.time.Clock()

        # Load assets
        self._font = assets.font

        self._scales = assets.scales
        self._grid = assets.grid
        self._slider_img = assets.slider_img
        self._logo = assets.logo
        self._lbl_vertical = False    # If labels are horizontal or vertical

    def clear(self):
        self._surface.fill(BLACK)

    def tick_display(self):
        self._frame_rate.tick(FPS)

    def update(self, mode, data_src):
        self.clear()
        if mode == DisplayMode.SPLASH:
            self._show_splash()
        elif isinstance(data_src, Record):
            if mode == DisplayMode.VIDEO:
                self._draw_image(data_src.image, 0, 0)
            elif mode == DisplayMode.TEXT:
                self._update_string_text(data_src.text)
        else:
            self._update_sensor_disp(mode, data_src)
        pygame.display.update()

    def _update_sensor_disp(self, mode, sensor_array):
        if mode == DisplayMode.SLIDER:
            self._update_sliders(sensor_array)
        elif mode == DisplayMode.GRAPH:
            self._update_graphs(sensor_array)
        elif mode == DisplayMode.TEXT:
            self._update_sensor_text(sensor_array)
        else:
            self._update_to_unknown(mode)

    def _update_sliders(self, sensor_array):
        self._surface.blit(self._scales, (0, 0))
        for sensor_type in sensor_array:
            indicator = sensor_array[sensor_type]
            assert isinstance(indicator, Indicator)
            self._draw_image(self._slider_img, *indicator.get_position())

    def _update_string_text(self, str_text):
        font_size = 15
        disp_font = pygame.font.Font(self._font, font_size)
        text = disp_font.render(str_text, True, SF_YELLOW)
        x_lbl_pos, y_lbl_pos = (20, 20)
        self._surface.blit(text, (x_lbl_pos, y_lbl_pos))

    def _update_sensor_text(self, sensor_array):
        font_size = 15
        disp_font = pygame.font.Font(self._font, font_size)
        lbl_idx = 0
        for sensor_type in sensor_array:
            indicator = sensor_array[sensor_type]
            assert isinstance(indicator, Indicator)
            lbl = f"{indicator.label} {indicator.cur_val:.2f}"
            label = disp_font.render(lbl, True, indicator.color)
            x_lbl_pos, y_lbl_pos = self._label_pos(lbl_idx)
            self._surface.blit(label, (x_lbl_pos, y_lbl_pos))
            lbl_idx += 1

    def _update_graphs(self, sensor_array):
        font_size = 15
        disp_font = pygame.font.Font(self._font, font_size)
        self._surface.blit(self._grid, (0, 0))
        lbl_idx = 0
        for sensor_type in sensor_array:
            indicator = sensor_array[sensor_type]
            assert isinstance(indicator, Indicator)
            self._draw_lines(indicator.color, indicator.get_history())

            lbl = f"{indicator.label} {indicator.cur_val:.2f}"
            label = disp_font.render(lbl, True, indicator.color)
            x_lbl_pos, y_lbl_pos = self._label_pos(lbl_idx)
            self._surface.blit(label, (x_lbl_pos, y_lbl_pos))
            lbl_idx += 1

    def _label_pos(self, lbl_num):
        if self._lbl_vertical:
            # Stack Vertically
            x_lbl_pos = 20
            y_lbl_pos = HEIGHT / 2 + 30
            y_lbl_pos += lbl_num * 20
        else:
            # Stack Horizontally
            x_lbl_pos = 20 + lbl_num * 65
            y_lbl_pos = 206

        return x_lbl_pos, y_lbl_pos

    def _update_to_unknown(self, mode):
        font_size = 15
        disp_font = pygame.font.Font(self._font, font_size)
        label = disp_font.render(f"Unknown mode: {mode}", True, SF_YELLOW)
        self._surface.blit(label, (10, 180))

    def _draw_image(self, img, x, y):
        self._surface.blit(img, (x, y))

    def _draw_lines(self, color, data):
        width = 3
        pygame.draw.lines(self._surface, color, False, data, width)

    def _show_splash(self):
        self.clear()
        self._surface.blit(self._logo, (90, 0))

        font_size = 33
        disp_font = pygame.font.Font(self._font, font_size)
        label = disp_font.render("StarFleet Tricorder TR-109", True, SF_YELLOW)
        self._surface.blit(label, (10, 180))
