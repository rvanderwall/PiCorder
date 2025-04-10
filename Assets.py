import pygame
from PIL import Image, ImageFont


class Assets:
    def __init__(self):
        self.font = "assets/babs.otf"
        self.large_font = None
        self.char_width = 9

        self.scales = pygame.image.load('./assets/background.png')
        self.grid = pygame.image.load('./assets/backgraph.png')
        self.slider_img = pygame.image.load('assets/slider.png')
        self.edith = pygame.image.load('./assets/Edith.jpeg')
        self.spock = pygame.image.load('./assets/spock.png')

        self.logo = pygame.image.load('assets/PicorderLogoSmall.png')
        self.logo_txt = "StarFleet Tricorder TR-109"
        self.logo_position = (90, 0)   # Upper left corner
        self.txt_position = (10, 180)

    def set_tft_mode(self):
        font_size = 22
        # self.large_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', font_size)
        self.large_font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', font_size)

        font_size = 15
        # self.font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', font_size)
        self.font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', font_size)
        self.char_width = 10

        self.scales = Image.open('./assets/background.png').convert('RGB')
        self.grid = Image.open('./assets/backgraph.png').convert('RGB')
        self.slider_img = Image.open('assets/slider.png').convert('RGB')
        self.edith = Image.open('./assets/Edith.jpeg')
        self.spock = Image.open('./assets/spock.png').convert('RGB')

        self.logo = Image.open('assets/PicorderLogoSmall.png').convert('RGB')
        self.logo_txt = "StarFleet Tricorder TR-109"
        self.logo_position = (90, 0)
        self.txt_position = (0, 180)
