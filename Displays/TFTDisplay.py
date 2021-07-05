import numpy      # Not used here, but ensures its installed for driver
from Logger import Logger
from Assets import Assets
from Displays.IDisplay import IDisplay, SF_YELLOW
try:
    import digitalio
    import board
    from PIL import Image, ImageDraw, ImageFont
    import adafruit_rgb_display.ili9341 as ili9341
    from adafruit_rgb_display import color565
except Exception as ex:
    lg = Logger("Startup")
    lg.info(f"import fail: {ex}")


#
# https://github.com/adafruit/Adafruit_CircuitPython_RGB_Display/tree/main/adafruit_rgb_display
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
        self._current_background = None
        self._static_text = []
        self._curr_image_list = []

    def clear(self):
        self._lgr.info("TFT: Clearing display with fill") if self._verbose else None
        self._surface.fill(0)
        self._static_text = []
        self._current_background = None
        self._curr_image_list = []

    def render_background(self, image):
        self._lgr.info("TFT: Add Background") if self._verbose else None
        if image == self._current_background:
            return
        self.render_static_image(image, (0, 0))
        self._current_background = image

    def render_dynamic_images(self, images):
        if len(images) == len(self._curr_image_list):
            for idx in range(len(images)):
                cur_image = self._curr_image_list[idx]
                new_image = images[idx]
                if cur_image[1] != new_image[1]:
                    self._replace_image(cur_image, new_image)
        else:
            # Clear out any existing images
            for img in self._curr_image_list:
                self._replace_image(img, None)

            for img in images:
                self._replace_image(None, img)

        self._curr_image_list = images

    def _replace_image(self, cur_image, new_image):
        if cur_image is not None:
            image = cur_image[0]
            position = cur_image[1]
            x, y = self._rotate(position[0], position[1], image.height)
            self._clear_area((x, y), (image.width, image.height))

        if new_image is not None:
            image = new_image[0]
            position = new_image[1]
            self.render_static_image(image, position)

    def render_static_image(self, pil_image, position):
        self._lgr.info("TFT: Add image") if self._verbose else None
        if pil_image.width > self.width or pil_image.height > self.height:
            pil_image = self._scale_image(pil_image)

        # Display image.
        x, y = self._rotate(position[0], position[1], pil_image.height)
        # self._lgr.info(f"TFT: img: disp = ({self.width},{self.height})")
        # self._lgr.info(f"TFT: img: img = ({pil_image.width},{pil_image.height})")
        # self._lgr.info(f"TFT: img: pos = ({x},{y})")
        self._surface.image(pil_image, x=x, y=y)

    def render_static_text(self, text, position, font_size=18):
        self._lgr.info("TFT: Render static text") if self._verbose else None
        if text in self._static_text:
            return
        self._static_text.append(text)
        self.render_dynamic_text(text, position, SF_YELLOW, font_size)

    def render_dynamic_text(self, text, position, color, font_size=18):
        self._lgr.info("TFT: Render dynamic text") if self._verbose else None
        if font_size > 18:
            font = self.large_font
        else:
            font = self._font

        (font_width, font_height) = font.getsize(text)
        image = Image.new("RGB", (font_width, font_height))
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), text, font=font, fill=color)

        x, y = self._rotate(position[0], position[1], font_height)
        # self._lgr.info(f"TFT: txt: disp = ({self.width},{self.height})")
        # self._lgr.info(f"TFT: txt: txt = ({font_width},{font_height}) ['{text}']")
        # self._lgr.info(f"TFT: txt: pos = ({x},{y})")
        self._surface.image(image, x=x, y=y)

    def render_lines(self, line_data):
        self._lgr.info(f"TFT: Render {len(line_data)} lines") if self._verbose else None
        image = Image.new("RGB", (self.width, self.height))
        image = Image.blend(image, self._current_background, alpha=1)
        draw = ImageDraw.Draw(image)
        for line in line_data:
            color = line[0]
            data = line[1]
            # draw.point(data, fill=color)
            for point in data:
                x, y = point
                draw.line((x,y,x+1,y), fill=color, width=3)
        self.render_static_image(image, (0, 0))

    def update(self):
        pass

    def _rotate(self, x, y, image_height):
        """
            The TFT display has (0, 0) in the lower left, regardless of
            rotation.  X is up/down, Y is left/right with the way the display
            is mounted.
            images/text are painted with x,y at the lower left corner
            when rotation is 270
            x, y are intended to be upper, left
        :param x:
        :param y:
        :return: new x, y
        """
        if self._surface.rotation == 90:
            # we swap height/width to rotate it to landscape!
            return y, x
        if self._surface.rotation == 270:
            # we swap height/width to rotate it to landscape!
            return self.height - y - image_height, x
        else:
            return x, y

    def _scale_image(self, pil_image):
        self._lgr.info("TFT: scale image") if self._verbose else None
        image_ratio = pil_image.width / pil_image.height
        screen_ratio = self.width / self.height
        if screen_ratio > image_ratio:
            scaled_width = pil_image.width * self.height // pil_image.height
            scaled_height = self.height
        else:
            scaled_width = self.width
            scaled_height = pil_image.height * self.width // pil_image.width
        image = pil_image.resize((scaled_width, scaled_height), Image.BICUBIC)
        # self._lgr.info(f"TFT: scale: disp = ({self.width},{self.height})")
        # self._lgr.info(f"TFT: scale: pil = ({pil_image.width},{pil_image.height}) [{image_ratio}]")
        # self._lgr.info(f"TFT: scale: img = ({image.width},{image.height}) [{image_ratio}]")
        return image

    def _crop_image(self, image):
        # Crop and center the image
        x = image.width // 2 - self.width // 2
        y = image.height // 2 - self.height // 2
        image = image.crop((x, y, x + self.width, y + self.height))
        return image

    def _clear_area(self, pos, size, color=0):
        self._lgr.info("TFT: Clearing display area") if self._verbose else None
        self._surface.fill_rectangle(pos[0], pos[1], size[0], size[1], color)

