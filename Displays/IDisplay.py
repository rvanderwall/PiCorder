from abc import ABC, abstractmethod


#
# General Display constants
#
RED = (255,   0,   0)
RED_ORANGE = (255,   70,   0)
GREEN = (0,   255,   0)
BLUE = (0,     0, 255)
ORANGE = (255, 140,   0)
SF_YELLOW = (250, 225,  88)
BLACK = (0,     0,   0)
WHITE = (255, 255, 255)


class IDisplay(ABC):
    def __init__(self, font):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def render_image(self, image, position):
        pass

    @abstractmethod
    def render_text(self, text, position, size):
        pass

    @abstractmethod
    def render_lines(self, color, data):
        pass

    @abstractmethod
    def update(self):
        pass