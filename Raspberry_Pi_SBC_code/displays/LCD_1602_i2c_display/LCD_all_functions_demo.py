#!/usr/bin/python
# RPi PCBs PCB version of LCD_all_functions_demo2.py runs through a large sequence of display functions
#     with 3 second gaps between each item
# On a 16×2 LCD, the rows are numbered 1 – 2, while the columns are numbered 0 – 15. 

# command to run this demo:  python3 ./RPi_maker_PCB5/displays/LCD_1602_i2c_display/LCD_all_functions_demo.py

#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# function to return the CPU temperature
#
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# Return CPU temperature as a character string                                     
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))


#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# main code
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

import os

# CLI command to check I2C address:  i2cdetect -y -r 1
#
import I2C_LCD_driver
from time import *
import socket

mylcd = I2C_LCD_driver.lcd()

print ("displaying the Hello World text")
mylcd.lcd_display_string("Hello World!", 2, 2) # display at row 2 column 2
sleep(3)
mylcd.lcd_clear()

CPU_temp = getCPUtemperature()
print ("displaying the CPU temperature")
mylcd.lcd_display_string("CPU temperature", 1, 0) # display at row 1 column 0
mylcd.lcd_display_string(str(CPU_temp) + " degC", 2, 1) # display at row 2 column 1
sleep(3)
mylcd.lcd_clear()


# clear the screen
print ("clearing the screen")
mylcd.lcd_display_string("This is how you", 1)
sleep(2)
mylcd.lcd_clear()
mylcd.lcd_display_string("clear the screen", 1)
sleep(2)
mylcd.lcd_clear()
sleep(3)

# backlight on/off
print ("turning the backlight off")
mylcd.backlight(0)
sleep(3)
print ("turning the backlight on")
mylcd.backlight(1)
sleep(3)
mylcd.lcd_clear()

# blinking text
print ("displaying Hello World as blinking text")
for i in range (0,5):  # 5 loops to blink on/off at 1 second intervals
    mylcd.lcd_display_string(u"Hello world!")
    sleep(0.5)
    mylcd.lcd_clear()
    sleep(0.5)
sleep(3)
mylcd.lcd_clear()

# display current IP address and then the host name
print ("displaying the current IP address")
testIP = "8.8.8.8"
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect((testIP, 0))
ipaddr = s.getsockname()[0]
host = socket.gethostname()
mylcd.lcd_display_string("IP Address:", 1) 
mylcd.lcd_display_string(ipaddr, 2)   
sleep(5)
mylcd.lcd_clear()
print ("displaying the current host name")
mylcd.lcd_display_string("Host name:", 1) 
mylcd.lcd_display_string(host, 2)   
sleep(3)
mylcd.lcd_clear()

# scroll text right to left continuously
print ("displaying text scrolled right to left for a number of times")
str_pad = " " * 16
my_long_string = "This is a string that needs to scroll right to left"
my_long_string = str_pad + my_long_string
for loops in range (0, 2):   # do the scrolling 10 times
    print ("Loop: " + str(loops))
    for i in range (0, len(my_long_string)):
        lcd_text = my_long_string[i:(i+16)]
        mylcd.lcd_display_string(lcd_text,1)
        sleep(0.28)
        mylcd.lcd_display_string(str_pad,1)     
sleep(3)
mylcd.lcd_clear()

# scroll text left to right continuously
print ("displaying text scrolled left to right for a number of times")
padding = " " * 16
my_long_string = "This is a string that needs to scroll left to right"
padded_string = my_long_string + padding
for loops in range (0, 2):   # do the scrolling 10 times
    print ("Loop: " + str(loops))
    for i in range (0, len(my_long_string)):
        lcd_text = padded_string[((len(my_long_string)-1)-i):-i]
        mylcd.lcd_display_string(lcd_text,1)
        sleep(0.28)
        mylcd.lcd_display_string(padding[(15+i):i], 1)
sleep(3)
mylcd.lcd_clear()

# CUSTOM CHARACTERS
# You can create any pattern you want and print it to the display as a custom character. 
# Each character is an array of 5 x 8 pixels. 
# Up to 8 custom characters can be defined and stored in the LCD’s memory. 
# This custom character generator - https://omerk.github.io/lcdchargen/ will help you 
#   create the required bit array for any defined custom character of your own.

# example 1: display a single custom character
#  - the following code generates a “<” character:
print ("displaying a single custom character that looks like >")
fontdata1 = [      
        [ 0b00010, 
          0b00100, 
          0b01000, 
          0b10000, 
          0b01000, 
          0b00100, 
          0b00010, 
          0b00000 ],
]
mylcd.lcd_load_custom_chars(fontdata1)
mylcd.lcd_write(0x80)
mylcd.lcd_write_char(0)
sleep(3)
mylcd.lcd_clear()

# example 2: display multiple custom character
#  - the following code displays a large right pointing arrow (→) to the screen:
print ("displaying multiple custom characters that look like →")
fontdata1 = [
        # char(0) - Upper-left character
        [ 0b00000, 
          0b00000, 
          0b00000, 
          0b00000, 
          0b00000, 
          0b00000, 
          0b11111, 
          0b11111 ],

        # char(1) - Upper-middle character
        [ 0b00000, 
          0b00000, 
          0b00100, 
          0b00110, 
          0b00111, 
          0b00111, 
          0b11111, 
          0b11111 ],
        
        # char(2) - Upper-right character
        [ 0b00000, 
          0b00000, 
          0b00000, 
          0b00000, 
          0b00000, 
          0b00000, 
          0b10000, 
          0b11000 ],
        
        # char(3) - Lower-left character
        [ 0b11111, 
          0b11111, 
          0b00000, 
          0b00000, 
          0b00000, 
          0b00000, 
          0b00000, 
          0b00000 ],
       
        # char(4) - Lower-middle character
        [ 0b11111, 
          0b11111, 
          0b00111, 
          0b00111, 
          0b00110, 
          0b00100, 
          0b00000, 
          0b00000 ],
        
        # char(5) - Lower-right character
        [ 0b11000, 
          0b10000, 
          0b00000, 
          0b00000, 
          0b00000, 
          0b00000, 
          0b00000, 
          0b00000 ],
]

mylcd.lcd_load_custom_chars(fontdata1)

mylcd.lcd_write(0x80)
mylcd.lcd_write_char(0)
mylcd.lcd_write_char(1)
mylcd.lcd_write_char(2)

mylcd.lcd_write(0xC0)
mylcd.lcd_write_char(3)
mylcd.lcd_write_char(4)
mylcd.lcd_write_char(5)
sleep(3)
mylcd.lcd_clear()

print ("displaying the CPU temp continuously")
# now continuously loop showing the CPU temp
try:  # this try loop is not strictly necessary but it does allow the script to be easily stopped with CTRL-C    

    while True:
        CPU_temp = getCPUtemperature()
        mylcd.lcd_display_string("CPU temperature", 1, 0) # display at row 1 column 0
        mylcd.lcd_display_string(str(CPU_temp) + " degC", 2, 1) # display at row 2 column 1
        sleep(3)
        mylcd.lcd_clear()


finally:  # this code is run when the try is interrupted with a CTRL-C
    print(" ")

    print ("end of demonstration program")
    mylcd.lcd_clear()
    mylcd.lcd_display_string("End of demo!", 2, 2) # display at row 2 column 2
    sleep(5)
    mylcd.lcd_clear()
    mylcd.backlight(0)


