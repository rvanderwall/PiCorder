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
from PIL import Image, ImageDraw
import adafruit_rgb_display.ili9341 as ili9341

def log(msg):
    t = datetime.now()
    print(f"{t}: {msg}")

log("Done with imports")

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)
log("Done setting pins")

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()
log("Done setting up SPI")


# Create the display:
disp = ili9341.ILI9341(
    spi,
    rotation=270,  # 2.2", 2.4", 2.8", 3.2" ILI9341
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)
log("Done getting display")

#  Clear display
disp.fill(0)
log("Done clearing display")


# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
if disp.rotation % 180 == 90:
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
else:
    width = disp.width  # we swap height/width to rotate it to landscape!
    height = disp.height

width = 320
height = 240
image = Image.new("RGB", (width, height))
log("Done loading image")


# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
log("Done getting draw object")

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
log("Done with fill Rect")

#disp.image(image)
log("Done displaying")

image = Image.open("blinka.jpg")
image_l = Image.open("../assets/PicorderLogoSmall.png")
image_e = Image.open("../assets/Edith.jpeg")
log("Done loading PNG")

def rescale(image):
    # Scale the image to the smaller screen dimension
    image_ratio = image.width / image.height
    screen_ratio = width / height
    if screen_ratio > image_ratio:
        scaled_width = image.width * height // image.height
        scaled_height = height
    else:
        scaled_width = width
        scaled_height = image.height * width // image.width

    return image.resize((scaled_width, scaled_height), Image.BICUBIC)

# Crop and center the image
#x = scaled_width // 2 - width // 2
#y = scaled_height // 2 - height // 2
# image = image.crop((x, y, x + width, y + height))

log(f"pixel = {image.getpixel((0,0))}")
log(f"size = ({image.width},{image.height})")
image = image_l.convert('RGB')
log("Done converting")
log(f"size = ({image.width},{image.height})")

# Display image.
disp.image(image)
log("Done displaying")

time.sleep(5)

log(f"size = ({image_e.width},{image_e.height})")
image_e = rescale(image_e)
log(f"size = ({image_e.width},{image_e.height})")
disp.image(image_e)
