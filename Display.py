import pygame
from time import sleep

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
MAX_X = 320
MAX_Y = 240
upper_left = (0, 0)
lower_right = (MAX_X, MAX_Y)


class Display:
    def __init__(self):
        self.surface = pygame.display.set_mode((MAX_X, MAX_Y))
        self.frame_rate = pygame.time.Clock()

    def clear(self):
        self.surface.fill(BLACK)

    def tick_display(self):
        self.frame_rate.tick(FPS)

    def show_splash(self):
        self.surface.fill(BLACK)
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
