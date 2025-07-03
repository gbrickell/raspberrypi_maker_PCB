# adaptation for RPi Maker PCB v5.0
# command:  python3 ./RPi_maker_PCB5/displays/IPS_80x160_SPI/framerate.py

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
import time
import math
import sys

from PIL import Image
from PIL import ImageDraw
import ST7735 as ST7735

SPI_SPEED_MHZ = 10  # Higher speed = higher framerate

if len(sys.argv) > 1:
    SPI_SPEED_MHZ = int(sys.argv[1])

print("""
framerate.py - Test LCD framerate.

Running at: {}MHz
""".format(SPI_SPEED_MHZ))

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
STEPS = WIDTH * 2
images = []

for step in range(STEPS):
    image = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 128))
    draw = ImageDraw.Draw(image)

    if step % 2 == 0:
        draw.rectangle((79, 0, 159, 79), (0, 128, 0))
    else:
        draw.rectangle((0, 0, 79, 79), (0, 128, 0))

    f = math.sin((float(step) / STEPS) * math.pi)
    offset_left = int(f * WIDTH)
    draw.ellipse((offset_left, 35, offset_left + 10, 45), (255, 0, 0))

    images.append(image)

count = 0
time_start = time.time()

try:
    while True:
        disp.display(images[count % len(images)])
        count += 1
        time_current = time.time() - time_start
        if count % 120 == 0:
            print("Time: {:8.3f},      Frames: {:6d},      FPS: {:8.3f}".format(
                time_current,
                count,
                count / time_current))

except KeyboardInterrupt:
    print("  .... CTRL C interrupted!")
    print ("clearing display")
    disp.reset()

