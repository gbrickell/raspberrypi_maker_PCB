# adaptation for RPi Maker Kit PCB v5.0
# command:  python3 /home/pi/RPi_maker_kit5/displays/IPS_80x160_SPI/gif.py /home/pi/RPi_maker_kit5/displays/IPS_80x160_SPI/deployrainbows.gif

# Copyright (c) 2014 Adafruit Industries
# Author: Phil Howard, Tony DiCola
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
from PIL import Image
import ST7735
import time
import sys

print("gif.py - Display a gif on the LCD.")

if len(sys.argv) > 1:
    image_file = sys.argv[1]
else:
    print("Usage: {} <filename.gif>".format(sys.argv[0]))
    sys.exit(0)

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

# Initialize display.
disp.begin()

width = disp.width
height = disp.height

# Load an image.
print('Loading gif: {}...'.format(image_file))
image = Image.open(image_file)

print('Drawing gif, press Ctrl+C to exit!')

frame = 0

try:
    while True:
        try:
            image.seek(frame)
            disp.display(image.resize((width, height)))
            frame += 1
            time.sleep(0.05)

        except EOFError:
            frame = 0

except KeyboardInterrupt:
    print("  .... CTRL C interrupted!")
    print ("clearing display")
    disp.reset()
