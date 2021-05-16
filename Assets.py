import pygame


class Assets:
    def __init__(self):
        self.font = "assets/babs.otf"
        self.scales = pygame.image.load('./assets/background.png')
        self.grid = pygame.image.load('./assets/backgraph.png')
        self.slider_img = pygame.image.load('assets/slider.png')
        self.edith = pygame.image.load('./assets/Edith.jpeg')
        self.spock = pygame.image.load('./assets/spock.png')
        self.logo = pygame.image.load('assets/PicorderLogoSmall.png')
