import pygame
from PIL import Image, ImageDraw, ImageFont


class Assets:
    def __init__(self):
        self.font = "assets/babs.otf"
        self.scales = pygame.image.load('./assets/background.png')
        self.grid = pygame.image.load('./assets/backgraph.png')
        self.slider_img = pygame.image.load('assets/slider.png')
        self.edith = pygame.image.load('./assets/Edith.jpeg')
        self.spock = pygame.image.load('./assets/spock.png')
        self.logo = pygame.image.load('assets/PicorderLogoSmall.png')
        self.logo_txt = "StarFleet Tricorder TR-109"
        self.logo_position = (90, 0)  # PyGame
        self.txt_position = (10, 180)

    # self.logo = Image.open('assets/PicorderLogoSmall.png')

    def set_tft_mode(self):
        FONTSIZE = 22
        self.font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', FONTSIZE)
        self.scales = Image.open('./assets/background.png').convert('RGB')
        self.grid = Image.open('./assets/backgraph.png').convert('RGB')
        self.slider_img = Image.open('assets/slider.png').convert('RGB')
        self.edith = Image.open('./assets/Edith.jpeg')
        self.spock = Image.open('./assets/spock.png').convert('RGB')
        self.logo = Image.open('assets/PicorderLogoSmall.png').convert('RGB')
        self.logo_txt = "StarFleet Tricorder TR-109"
        self.logo_position = (96, 50) #TFT
        self.txt_position = (0, 0)
