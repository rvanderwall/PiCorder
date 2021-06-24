from Logger import Logger
from Assets import Assets
from Displays.IDisplay import IDisplay, SF_YELLOW, BLACK
try:
    import digitalio
    import board
    from PIL import Image, ImageDraw, ImageFont
    import adafruit_rgb_display.ili9341 as ili9341
except Exception as ex:
    lg = Logger("Startup")
    lg.info(f"import fail: {ex}")


#
# Tricorder display Constants
#


class TFT_Display(IDisplay):  # pylint: disable=camel-case
    def __init__(self, logger: Logger, assets: Assets):
        super().__init__(logger, assets)
        cs_pin = digitalio.DigitalInOut(board.CE0)
        dc_pin = digitalio.DigitalInOut(board.D25)
        reset_pin = digitalio.DigitalInOut(board.D24)

        # Config for display baudrate (default max is 24mhz):
        BAUDRATE = 24_000_000
        self.FPS = 30

        # Setup SPI bus using hardware SPI:
        spi = board.SPI()
        # rotation = 90  # Normal
        rotation = 270   # Rotated for tricorder

        # Create the display:
        self._surface = ili9341.ILI9341(
            spi,
            rotation=rotation,  # 2.2", 2.4", 2.8", 3.2" ILI9341
            cs=cs_pin,
            dc=dc_pin,
            rst=reset_pin,
            baudrate=BAUDRATE,
        )

        # display X is up.down and Y is left/right
        # surface shape = (240, 320)
        self.width, self.height = self._surface.height, self._surface.width

        self.large_font = assets.large_font
        self.current_background = None
        self._static_text = []

    def clear(self):
        self._lgr.info("TFT: Clearing display with fill")
        self._surface.fill(0)
        self._static_text = []

    def clear2(self):
        self._lgr.info("TFT: Clearing display with draw")
        image = Image.new("RGB", (self.width, self.height))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, self.width, self.height), outline=0, fill=BLACK)
        self._surface.image(image)
        self._static_text = []

    def render_background(self, image):
        self._lgr.info("TFT: Add Background")
        if image == self.current_background:
            return
        self.render_image(image, (0, 0))
        self.current_background = image

    def render_image(self, pil_image, position):
        self._lgr.info("TFT: Add image")
        if pil_image.width > self.width or pil_image.height > self.height:
            pil_image = self._scale_image(pil_image)

        # Display image.
        x, y = self._rotate(position[0], position[1])
#        self._lgr.info(f"TFT: img: disp = ({self.width},{self.height})")
#        self._lgr.info(f"TFT: img: img = ({pil_image.width},{pil_image.height})")
#        self._lgr.info(f"TFT: img: pos = ({x},{y})")
        self._surface.image(pil_image, x=x, y=y)

    def render_static_text(self, text, position, font_size=18):
        self._lgr.info("TFT: Render static text")
        if text in self._static_text:
            return
        self._static_text.append(text)
        self.render_dynamic_text(text, position, font_size)

    def render_dynamic_text(self, text, position, font_size=18):
        self._lgr.info("TFT: Render dynamic text")
        if font_size > 18:
            font = self.large_font
        else:
            font = self._font

        (font_width, font_height) = font.getsize(text)
        image = Image.new("RGB", (font_width, font_height))
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), text, font=font, fill=SF_YELLOW)

        x, y = self._rotate(position[0], position[1])
        self._lgr.info(f"TFT: txt: disp = ({self.width},{self.height})")
        self._lgr.info(f"TFT: txt: txt = ({font_width},{font_height})")
        self._lgr.info(f"TFT: txt: pos = ({x},{y})")
        self._surface.image(image, x=x, y=y)

    def render_lines(self, color, data):
        pass

    def update(self):
        pass

    def _rotate(self, x, y):
        """
            The TFT display has (0, 0) in the lower left, regardless of
            rotation.  X is up/down, Y is left/right with the way the display
            is mounted.
            images/text are painted with x,y at the lower left corner
            when rotation is 270
        :param x:
        :param y:
        :return: new x, y
        """
        if self._surface.rotation == 90:
            # we swap height/width to rotate it to landscape!
            return y, x
        if self._surface.rotation == 270:
            # we swap height/width to rotate it to landscape!
            return self.height - y, x
        else:
            return x, y

    def _scale_image(self, pil_image):
        image_ratio = pil_image.width / pil_image.height
        screen_ratio = self.width / self.height
        if screen_ratio < image_ratio:
            scaled_width = pil_image.width * self.height // pil_image.height
            scaled_height = self.height
        else:
            scaled_width = self.width
            scaled_height = pil_image.height * self.width // pil_image.width
        image = pil_image.resize((scaled_width, scaled_height), Image.BICUBIC)
        return image

    def _crop_image(self, image):
        # Crop and center the image
        x = image.width // 2 - self.width // 2
        y = image.height // 2 - self.height // 2
        image = image.crop((x, y, x + self.width, y + self.height))
        return image

    def _clear_area(self, position, size):
        pass
