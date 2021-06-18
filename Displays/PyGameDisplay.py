import pygame
from Displays.IDisplay import IDisplay, BLACK, SF_YELLOW


#
# Tricorder display Constants
#
FPS = 30
WIDTH = 320
HEIGHT = 240
upper_left = (0, 0)
lower_right = (WIDTH, HEIGHT)


class PyGameDisplay(IDisplay):
    def __init__(self, font):
        super().__init__(font)
        self._surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self._font = font

    def clear(self):
        self._surface.fill(BLACK)

    def render_image(self, image, position):
        self._surface.blit(image, position)

    def render_lines(self, color, data):
        width = 3
        pygame.draw.lines(self._surface, color, False, data, width)

    def render_text(self, text, position, size=15):
        disp_font = pygame.font.Font(self._font, size)
        label = disp_font.render(text, True, SF_YELLOW)
        self.render_image(label, position)

    def update(self):
        pygame.display.update()
