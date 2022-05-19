#!/usr/bin/python

# RPi kits PCB version of HG7881 motor controller

# command to run:  python3 ./RPi_maker_kit5/motor_control/drive_motors/HG7881_motor_controller/HG7881-motors_LCD_on_off.py
# simple on/off test version
#  N.B. it is important not to 'mix' PWM and simple on/off as this seems to confuse the HG7881

#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# Raspberry Pi generic set of HG7881 of on/off motor functions 
# 
#  N.B. depending upon how the motors are connected the motor direction
#    signals to the A1B or B1B pins may need to be reversed
#
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

def resetGPIO():
    GPIO.cleanup()
    GPIO.setup(A1A, GPIO.OUT)
    GPIO.setup(A1B, GPIO.OUT)
    GPIO.setup(B1A, GPIO.OUT)
    GPIO.setup(B1B, GPIO.OUT)


def Afwd():   
    print ("forward ")
    # Motor A - M1
    # set A1A HIGH   ## see next
    GPIO.output(A1A, 0)  # inverse for some reason????
    # set A1B ON i.e. HIGH for forward motion
    GPIO.output(A1B, 1)

def Bfwd():   
    # Motor B - M2
    # set B1A HIGH   ## see next
    GPIO.output(B1A, 0)  # inverse for some reason????
    # set B1B ON i.e. HIGH for forward motion
    GPIO.output(B1B, 1)

def Aback():   
    print ("backward ")
    # Motor A - M1
    # set A1A HIGH
    GPIO.output(A1A, 1)
    # set A1B OFF i.e. LOW for backward motion
    GPIO.output(A1B, 0)

def Bback():   
    # Motor B - M2
    # set B1A HIGH
    GPIO.output(B1A, 1)
    # set B1B OFF i.e. LOW for backward motion 
    GPIO.output(B1B, 0)

def Astop():
    print ("stop A")
    GPIO.output(A1B, 0)
    GPIO.output(A1A, 0)   


def Bstop():
    print ("stop B")
    GPIO.output(B1B, 0)
    GPIO.output(B1A, 0)


#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+ 
#
# main code
#
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# import the LCD driver code, initalise the LCD and clear the screen
import I2C_LCD_driver
mylcd = I2C_LCD_driver.lcd()
mylcd.lcd_clear()       # clear LCD screen

import RPi.GPIO as GPIO # Import the GPIO Library
import time             # Import the Time library

# Set the GPIO modes
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# HG7881 pin setup code
# Define Outputs from RPi to HG7881 - variable names are as per the HG7881 pin labels
A1A = 9    # motor A - PWM power setting or simple on/off
A1B = 10   # motor A - HIGH/LOW for Fwd/Rev
B1A = 8    # motor B - PWM power setting or simple on/off
B1B = 11   # motor B - HIGH/LOW for Fwd/Rev

# Set the GPIO Pin mode
resetGPIO()

# set the various PWM parameters
# How many times to turn the GPIO pin on and off each second 
Frequency = 20

# Turn all motors off - 
Astop()
Bstop()
print ("both motors set to stop")
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("motors setup:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("both motors off", 2, 0)   # display at row 2 column 0
time.sleep(3)

# motor A forwards
Afwd()
print ("motor A forward")
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("motor A fwd", 2, 0)   # display at row 2 column 0
# Run the motor for 3 seconds
time.sleep(3)

# Turn motor A off
Astop()
print ("both motors set to stop")
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("motor A off", 2, 0)   # display at row 2 column 0
time.sleep(3)

# motor B forwards
Bfwd()
print ("motor B forward")
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("motor B fwd", 2, 0)   # display at row 2 column 0
# Run the motor for 3 seconds
time.sleep(3)

# Turn motor B off
Bstop()
print ("both motors set to stop")
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("motor B off", 2, 0)   # display at row 2 column 0
time.sleep(3)

# motor A backwards 
Aback()
print ("motor A backward")
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("motor A back", 2, 0)   # display at row 2 column 0
# Run the motors for 3 seconds
time.sleep(3)

# Turn motor A off
Astop()
print ("both motors set to stop")
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("motor A off", 2, 0)   # display at row 2 column 0
time.sleep(3)

# motor B backwards
#Aback()
Bback()
print ("motor B backward")
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("motor B back", 2, 0)   # display at row 2 column 0
# Run the motors for 3 seconds
time.sleep(3)

# Turn motor B off
Bstop()
print ("both motors set to stop")
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("motor B off", 2, 0)   # display at row 2 column 0
time.sleep(3)

# Reset the GPIO pins (which will also turn off the motors)
GPIO.cleanup()
print ("GPIO cleaned up")
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("GPIO cleaned up", 2, 0)   # display at row 2 column 0
time.sleep(3)

mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Program ended", 1, 1)     # display at row 1 column 1
time.sleep(3)
mylcd.lcd_clear()  # clear LCD screen
mylcd.backlight(0) # turn off LCD backlight


