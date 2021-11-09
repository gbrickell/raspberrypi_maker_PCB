# adaptation for RPi Maker Kit PCB v5.0
# command:  python3 /home/pi/RPi_maker_kit5/displays/IPS_80x160_SPI/image.py /home/pi/RPi_maker_kit5/displays/IPS_80x160_SPI/cat.jpg

# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import sys
import time

from PIL import Image
import ST7735 as ST7735

print("image.py - Display an image on the LCD.")

if len(sys.argv) < 2:
    print("Usage: {} <image_file>".format(sys.argv[0]))
    sys.exit(1)

image_file = sys.argv[1]

# Create ST7735 LCD display class customised for RPI Maker Kit v5.0
disp = ST7735.ST7735(
    port=0,
    cs=0,            # using SPI CE0
    dc=15,           # connected to a spare GPIO#15
    backlight=18,    # connected to a spare GPIO#18
    rst = 14,        # connected to a spare GPIO#14
    rotation=90,
    spi_speed_hz=4000000
)

WIDTH = disp.width
HEIGHT = disp.height

# Initialize display.
disp.begin()

# Load an image.
print('Loading image: {}...'.format(image_file))
image = Image.open(image_file)

# Resize the image
image = image.resize((WIDTH, HEIGHT))

# Draw the image on the display hardware.
print('Drawing image')

disp.display(image)

time.sleep(5)
print ("clearing display")

disp.reset()
