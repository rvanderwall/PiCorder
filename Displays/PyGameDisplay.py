import pygame
from Assets import Assets
from Displays.IDisplay import IDisplay, BLACK, SF_YELLOW
from Logger import Logger

#
# Tricorder display Constants
#


class PyGameDisplay(IDisplay):
    def __init__(self, logger: Logger, assets: Assets):
        super().__init__(logger, assets)
        self.FPS = 5
        self.width = 320
        self.height = 240
        self._surface = pygame.display.set_mode((self.width, self.height))
        self._upper_left = (0, 0)
        self._static_text = []

    def clear(self):
        self._surface.fill(BLACK)
        self._static_text = []

    def render_background(self, image):
        self._surface.blit(image, (0, 0))

    def render_dynamic_images(self, images):
        for img in images:
            image = img[0]
            position = img[1]
            self._surface.blit(image, position)

    def render_static_image(self, image, position):
        self._surface.blit(image, position)

    def render_lines(self, color, data):
        width = 3
        pygame.draw.lines(self._surface, color, False, data, width)

    def render_dynamic_text(self, text, position, color, font_size=15):
        self._lgr.info(f"Render dynamic text {text}, {position}") if self._verbose else None
        row_height = 20
        row_size = (self.width - position[0], row_height)
        self._clear_area(position, row_size)
        disp_font = pygame.font.Font(self._font, font_size)
        label = disp_font.render(text, True, color)
        self.render_static_image(label, position)

    def render_static_text(self, text, position, font_size=15):
        self._lgr.info(f"Render static text {text}, {position}") if self._verbose else None
        if text in self._static_text:
            return
        self._static_text.append(text)
        disp_font = pygame.font.Font(self._font, font_size)
        label = disp_font.render(text, True, SF_YELLOW)
        self.render_static_image(label, position)

    def update(self):
        pygame.display.update()

    def _clear_area(self, position, size):
        self._lgr.info(f"Clear area {position}, {size}") if self._verbose else None
        rect = pygame.Rect(position[0], position[1], size[0], size[1])
        pygame.draw.rect(self._surface, BLACK, rect)
