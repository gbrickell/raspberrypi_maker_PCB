# adaptation for RPi Maker Kit PCB v5.0
# command:  python3 /home/pi/RPi_maker_kit5/displays/IPS_80x160_SPI/scrolling-text.py

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time

import ST7735


MESSAGE = "Hello World! How are you today?"

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

WIDTH = disp.width
HEIGHT = disp.height


img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))

draw = ImageDraw.Draw(img)

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)

size_x, size_y = draw.textsize(MESSAGE, font)

text_x = 160
text_y = (80 - size_y) // 2

t_start = time.time()

try:
    while True:
        x = (time.time() - t_start) * 100
        x %= (size_x + 160)
        draw.rectangle((0, 0, 160, 80), (0, 0, 0))
        draw.text((int(text_x - x), text_y), MESSAGE, font=font, fill=(255, 255, 255))
        disp.display(img)

except KeyboardInterrupt:
    print("  .... CTRL C interrupted!")
    print ("clearing display")
    disp.reset()
