import pygame

from Assets import Assets
from ModeTransitions import DisplayMode
from Indicator import Indicator, Indicator3D
from Logger import Logger
from Records import Record

try:
    import digitalio
    import board
    from PIL import Image, ImageDraw
    import adafruit_rgb_display.ili9341 as ili9341
    DISPLAY_MODE = "TFT"
    lg = Logger("Startup")
    lg.info("Entering TFT display mode")
except:
    DISPLAY_MODE = "WINDOW"
    lg = Logger("Startup")
    lg.info("Entering WINDOW display mode")


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


class TFT_Display:
    def __init__(self):
        cs_pin = digitalio.DigitalInOut(board.CE0)
        dc_pin = digitalio.DigitalInOut(board.D25)
        reset_pin = digitalio.DigitalInOut(board.D24)

        # Config for display baudrate (default max is 24mhz):
        BAUDRATE = 24000000

        # Setup SPI bus using hardware SPI:
        spi = board.SPI()

        # Create the display:
        self._surface = ili9341.ILI9341(
            spi,
            rotation=90,  # 2.2", 2.4", 2.8", 3.2" ILI9341
            cs=cs_pin,
            dc=dc_pin,
            rst=reset_pin,
            baudrate=BAUDRATE,
        )
        self.width = WIDTH
        self.height = HEIGHT
        self._manage_rotation()

    def _manage_rotation(self):
        if self._surface.rotation % 180 == 90:
            self.height = self._surface.width  # we swap height/width to rotate it to landscape!
            self.width = self._surface.height
        else:
            self.width = self._surface.width  # we swap height/width to rotate it to landscape!
            self.height = self._surface.height

    def clear(self):
        image = Image.new("RGB", (self.width, self.height))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, self.width, self.height), outline=0, fill=(0, 0, 0))
        self._surface.image(image)

    def render_image(self, image, position):
        # Scale the image to the smaller screen dimension
        image_ratio = image.width / image.height
        screen_ratio = self.width / self.height
        if screen_ratio < image_ratio:
            scaled_width = image.width * self.height // image.height
            scaled_height = self.height
        else:
            scaled_width = self.width
            scaled_height = image.height * self.width // image.width
        image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

        # Crop and center the image
        x = scaled_width // 2 - self.width // 2
        y = scaled_height // 2 - self.height // 2
        image = image.crop((x, y, x + self.width, y + self.height))

        # Display image.
        self._surface.image(image)


class WindowDisplay:
    def __init__(self):
        self._surface = pygame.display.set_mode((WIDTH, HEIGHT))

    def clear(self):
        self._surface.fill(BLACK)

    def render_image(self, image, position):
        self._surface.blit(image, position)

    def draw_lines(self, color, data):
        width = 3
        pygame.draw.lines(self._surface, color, False, data, width)


class Display:
    def __init__(self, assets: Assets):
        if DISPLAY_MODE == "TFT":
            self._display = TFT_Display()
        else:
            self._display = WindowDisplay()

        self._frame_rate = pygame.time.Clock()

        # Load assets
        self._font = assets.font

        self._scales = assets.scales
        self._grid = assets.grid
        self._slider_img = assets.slider_img
        self._logo = assets.logo
        self._lbl_vertical = False    # If labels are horizontal or vertical

    def clear(self):
        self._display.clear()

    def tick_display(self):
        self._frame_rate.tick(FPS)

    def update(self, mode, data_src):
        self.clear()
        if mode == DisplayMode.SPLASH:
            self._show_splash()
        elif isinstance(data_src, Record):
            if mode == DisplayMode.VIDEO:
                self._display.render_image(data_src.image, (0, 0))
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
        self._display.render_image(self._scales, (0, 0))
        for sensor_type in sensor_array:
            indicator = sensor_array[sensor_type]
            assert isinstance(indicator, Indicator)
            self._display.render_image(self._slider_img, indicator.get_position())

    def _update_string_text(self, str_text):
        font_size = 15
        disp_font = pygame.font.Font(self._font, font_size)
        text = disp_font.render(str_text, True, SF_YELLOW)
        x_lbl_pos, y_lbl_pos = (20, 20)
        self._display.render_image(text, (x_lbl_pos, y_lbl_pos))

    def _update_sensor_text(self, sensor_array):
        font_size = 15
        disp_font = pygame.font.Font(self._font, font_size)
        lbl_idx = 0
        for sensor_type in sensor_array:
            indicator = sensor_array[sensor_type]
            if isinstance(indicator, Indicator3D):
                lbl = f"{indicator.label} {indicator.cur_val}"
                self._lbl_vertical = True
            else:
                assert isinstance(indicator, Indicator)
                self._lbl_vertical = False
                lbl = f"{indicator.label} {indicator.cur_val:.2f}"
            label = disp_font.render(lbl, True, indicator.color)
            x_lbl_pos, y_lbl_pos = self._label_pos(lbl_idx)
            self._display.render_image(label, (x_lbl_pos, y_lbl_pos))
            lbl_idx += 1

    def _update_graphs(self, sensor_array):
        font_size = 15
        disp_font = pygame.font.Font(self._font, font_size)
        self._display.render_image(self._grid, (0, 0))
        lbl_idx = 0
        for sensor_type in sensor_array:
            indicator = sensor_array[sensor_type]
            assert isinstance(indicator, Indicator)
            self._display.draw_lines(indicator.color, indicator.get_history())

            lbl = f"{indicator.label} {indicator.cur_val:.2f}"
            label = disp_font.render(lbl, True, indicator.color)
            x_lbl_pos, y_lbl_pos = self._label_pos(lbl_idx)
            self._display.render_image(label, (x_lbl_pos, y_lbl_pos))
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
        self._display.render_image(label, (10, 180))

    def _show_splash(self):
        self.clear()
        self._display.render_image(self._logo, (90, 0))

        font_size = 33
        disp_font = pygame.font.Font(self._font, font_size)
        label = disp_font.render("StarFleet Tricorder TR-109", True, SF_YELLOW)
        self._display.render_image(label, (10, 180))
