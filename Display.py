import pygame
from time import sleep

from ModeTransitions import ModeMap, Mode

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
# Tricorder Specific Constants
#
FPS = 30
WIDTH = 320
HEIGHT = 240
upper_left = (0, 0)
lower_right = (WIDTH, HEIGHT)


class Display:
    def __init__(self):
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.frame_rate = pygame.time.Clock()
        self.mode_mapper = ModeMap()
        self.scales = pygame.image.load('./assets/background.png')
        self.grid = pygame.image.load('./assets/backgraph.png')
        self.font = "assets/babs.otf"

    def switch_display_modes(self, button):
        self.mode_mapper.switch_mode(button)
        self.mode_mapper.show_mode()

    def clear(self):
        self.surface.fill(BLACK)

    def tick_display(self):
        self.frame_rate.tick(FPS)

    def update(self, sensor_array):
        self.clear()
        mode = self.mode_mapper.current_mode
        if mode == Mode.ENV_SLIDER:
            self._update_env_slider(sensor_array)
        elif mode == Mode.ENV_GRAPH:
            self._update_env_graph(sensor_array)
        elif mode == Mode.MOVIE_EDITH:
            self._edith_movie()
        elif mode == Mode.MOVIE_SPOCK:
            self._spock_movie()
        else:
            self._update_to_unknown(mode)
        pygame.display.update()

    def _update_env_slider(self, sensor_array):
        self.surface.blit(self.scales, (0, 0))
        for sensor_type in sensor_array:
            sensor = sensor_array[sensor_type]
            sensor.render_as_pointer(self)

    def _update_env_graph(self, sensor_array):
        font_size = 15
        disp_font = pygame.font.Font(self.font, font_size)
        self.surface.blit(self.grid, (0, 0))
        y_pos = HEIGHT / 2 + 30
        for sensor_type in sensor_array:
            sensor = sensor_array[sensor_type]
            sensor.render_as_graph(self)
            lbl = f"{sensor.name} {sensor.cur_val:.2f}"
            label = disp_font.render(lbl, True, sensor.color)
            self.surface.blit(label, (20, y_pos))
            y_pos += 15

    def _edith_movie(self):
        edith = pygame.image.load('./assets/Edith.jpeg')
        self.surface.blit(edith, (0, 0))

    def _spock_movie(self):
        spock = pygame.image.load('./assets/spock.png')
        self.surface.blit(spock, (0, 0))

    def _update_to_unknown(self, mode):
        font_size = 25
        disp_font = pygame.font.Font(self.font, font_size)
        label = disp_font.render(f"Unknown mode: {mode}", True, SF_YELLOW)
        self.surface.blit(label, (10, 180))

    def show_splash(self):
        self.clear()
        logo = pygame.image.load('assets/PicorderLogoSmall.png')
        self.surface.blit(logo, (90, 0))

        font = "assets/babs.otf"
        font_size = 33
        disp_font = pygame.font.Font(font, font_size)
        label = disp_font.render("StarFleet Tricorder TR-109", True, SF_YELLOW)
        self.surface.blit(label, (10, 180))

        pygame.display.update()
        for i in range(2):
            pygame.event.get()
            sleep(1)

        # Start off in basic mode.
        self.mode_mapper.current_mode = Mode.ENV_SLIDER
