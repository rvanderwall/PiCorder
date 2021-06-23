# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Be sure to check the learn guides for more usage information.

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!

Author(s): Melissa LeBlanc-Williams for Adafruit Industries
"""

import time
from datetime import datetime
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.ili9341 as ili9341


WIDTH = 320
HEIGHT = 240
BAUDRATE = 64_000_000


def log(msg):
    t = datetime.now()
    print(f"{t}: {msg}")

log("Done with imports")

def setup():
    # Configuration for CS and DC pins (these are PiTFT defaults):
    cs_pin = digitalio.DigitalInOut(board.CE0)
    dc_pin = digitalio.DigitalInOut(board.D25)
    reset_pin = digitalio.DigitalInOut(board.D24)
    log("Done setting pins")

    # Config for display baudrate (default max is 24mhz):

    # Setup SPI bus using hardware SPI:
    spi = board.SPI()
    log("Done setting up SPI")

    # Create the display:
    rotation = 270
    disp = ili9341.ILI9341(
        spi,
        rotation=rotation,  # 2.2", 2.4", 2.8", 3.2" ILI9341
        cs=cs_pin,
        dc=dc_pin,
        rst=reset_pin,
        baudrate=BAUDRATE,
    )
    log(f"Done getting display: ({disp.width}, {disp.height})")
    return disp


def clear(disp):
    #  Clear display
    disp.fill(0)
    log("Done clearing display")


def rotate(disp):
    # Make sure to create image with mode 'RGB' for full color.
    if disp.rotation % 180 == 90:
        height = disp.width  # we swap height/width to rotate it to landscape!
        width = disp.height
    else:
        width = disp.width  # we swap height/width to rotate it to landscape!
        height = disp.height


def crop():
    # Crop and center the image
    x = scaled_width // 2 - width // 2
    y = scaled_height // 2 - height // 2
    image = image.crop((x, y, x + width, y + height))


def rescale(image):
    # Scale the image to the smaller screen dimension
    image_ratio = image.width / image.height
    screen_ratio = WIDTH / HEIGHT
    if screen_ratio > image_ratio:
        scaled_width = image.width * HEIGHT // image.height
        scaled_height = HEIGHT
    else:
        scaled_width = WIDTH
        scaled_height = image.height * WIDTH // image.width

    return image.resize((scaled_width, scaled_height), Image.BICUBIC)

def show_box(disp):
    image = Image.new('RGB', (10, 10))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 10, 10), fill=(255, 0, 0))
    disp.image(image, x=10, y=150)
    log("Done painting box")

def show_image(disp):
    # Create blank image for drawing.
    image = Image.new("RGB", (WIDTH, HEIGHT))
    log("Done loading image")

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)
    log("Done getting draw object")

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=(0, 0, 0))
    log("Done with fill Rect")

    image = Image.open("blinka.jpg")

    if True:
        image_l = Image.open("../assets/PicorderLogoSmall.png")
        log("Done loading PNG")
        log(f"size_l = ({image_l.width},{image_l.height})")
        image_l = image_l.convert('RGB')
        log("Done converting")
        log(f"size_l = ({image_l.width},{image_l.height})")
        disp.image(image_l)
        log("Done displaying logo")

    if False:
        image_e = Image.open("../assets/Edith.jpeg")
        log(f"size_e = ({image_e.width},{image_e.height})")
        image_e = rescale(image_e)
        log(f"size_e = ({image_e.width},{image_e.height})")
        disp.image(image_e)
        log("Done displaying edith")

def show_text(disp, text):
    log("Start displaying text")
    FONTSIZE = 24
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', FONTSIZE)
    (font_width, font_height) = font.getsize(text)

    #image = Image.new("RGB", (WIDTH, HEIGHT))
    image = Image.new("RGB", (font_width, font_height))
    draw = ImageDraw.Draw(image)

    x = (WIDTH - font_width) // 2
    y = (HEIGHT - font_height) // 2
    x = 10
    y = 150
    #draw.text((WIDTH // 2 - font_width // 2, HEIGHT // 2 - font_height // 2),
    #          text, font=font, fill=(255, 255, 0))
    
    draw.text((0, 0), text, font=font, fill=(255, 255, 0))

    log(f"Before image ({x},{y})")
    log(f"size = ({image.width},{image.height})")
    disp.image(image, x=x, y=y)
    log("After image")
    

def main():
    disp = setup()
    clear(disp)
    #show_image(disp)
    show_text(disp, "Hello")
    #show_text(disp, "Goodbye")
    #while True:
    #     show_text(disp, str(datetime.now().second))
    show_box(disp)


if __name__ == "__main__":
    main()
