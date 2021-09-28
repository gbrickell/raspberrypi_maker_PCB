#!/usr/bin/python
# RPi kits PCB version of hello_world.py that just displays "Hello World"
# On a 16×2 LCD, the rows are numbered 1 – 2, while the columns are numbered 0 – 15. 
# So to print “Hello World!” at the first column of the top row, you would use: 
# mylcd.lcd_display_string(“Hello World!”, 1, 0).

# command to run this demo:  python3 /home/pi/RPi_maker_kit5/displays/LCD_1602_i2c_display/hello_world.py

# CLI command to check I2C address:  i2cdetect -y -r 1
#
import I2C_LCD_driver
from time import *

mylcd = I2C_LCD_driver.lcd()

mylcd.lcd_display_string("Hello World!", 2, 2) # display at row 2 column 2

sleep(10)
mylcd.lcd_clear()
mylcd.backlight(0)
