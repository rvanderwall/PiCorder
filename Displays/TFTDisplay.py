from Logger import Logger
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
FPS = 30
WIDTH = 320
HEIGHT = 240
upper_left = (0, 0)
lower_right = (WIDTH, HEIGHT)


class TFT_Display(IDisplay):  # pylint: disable=camel-case
    def __init__(self, font):
        super().__init__(font)
        cs_pin = digitalio.DigitalInOut(board.CE0)
        dc_pin = digitalio.DigitalInOut(board.D25)
        reset_pin = digitalio.DigitalInOut(board.D24)

        # Config for display baudrate (default max is 24mhz):
        BAUDRATE = 24_000_000

        # Setup SPI bus using hardware SPI:
        spi = board.SPI()
        rotation = 90 # Normal
        rotation = 270 # Rotated for tricorder

        # Create the display:
        self._surface = ili9341.ILI9341(
            spi,
            rotation=rotation,  # 2.2", 2.4", 2.8", 3.2" ILI9341
            cs=cs_pin,
            dc=dc_pin,
            rst=reset_pin,
            baudrate=BAUDRATE,
        )
        self.width = WIDTH
        self.height = HEIGHT
        self._font = font
        self._manage_rotation()

    def _manage_rotation(self):
        if self._surface.rotation % 180 == 90:
            # we swap height/width to rotate it to landscape!
            self.height = self._surface.width
            self.width = self._surface.height
        else:
            # we swap height/width to rotate it to landscape!
            self.width = self._surface.width
            self.height = self._surface.height

    def clear(self):
        #  Clear display
        self._surface.fill(0)

    def clear2(self):
        image = Image.new("RGB", (self.width, self.height))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, self.width, self.height), outline=0, fill=BLACK)
        self._surface.image(image)

    def render_image(self, pil_image, position):
        print(f"disp = ({self.width},{self.height})")
        print(f"Size = ({pil_image.width},{pil_image.height})")
        if pil_image.width > self.width or pil_image.height > self.height:
            pil_image = self._scale_image(pil_image)

        # Display image.
        print(f"img: disp = ({self.width},{self.height})")
        print(f"img: img = ({pil_image.width},{pil_image.height})")
        print(f"img: pos = ({position[0]},{position[1]})")
        self._surface.image(pil_image, x=position[1], y=position[0])

    def render_text(self, text, position, size):
        (font_width, font_height) = self._font.getsize(text)
        image = Image.new("RGB", (font_width, font_height))
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), text, font=self._font, fill=SF_YELLOW)

        (font_width, font_height) = self._font.getsize(text)
        c_x = self.width // 2 - font_width // 2
        c_y = self.height // 2 - font_height // 2
        print(f"txt: disp = ({self.width},{self.height})")
        print(f"txt: center = ({c_x},{c_y})")
        print(f"txt: size = ({font_width},{font_height})")
        draw.text((0, 0), text, font=self._font, fill=SF_YELLOW)

        #self._surface.image(image, x=position[0], y=position[1])
        self._surface.image(image, x=position[0], y=position[1])


    def render_lines(self, color, data):
        pass

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
