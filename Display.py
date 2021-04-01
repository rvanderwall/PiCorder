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

    def switch_display_modes(self, button):
        self.mode_mapper.switch_mode(button)
        self.mode_mapper.show_mode()

    def clear(self):
        self.surface.fill(BLACK)

    def tick_display(self):
        self.frame_rate.tick(FPS)

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
