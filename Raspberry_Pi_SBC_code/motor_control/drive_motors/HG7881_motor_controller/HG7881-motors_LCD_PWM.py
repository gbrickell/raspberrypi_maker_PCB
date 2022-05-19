#!/usr/bin/python

# RPi kits PCB version of HG7881 motor controller

# command to run:  python3 ./RPi_maker_kit5/motor_control/drive_motors/HG7881_motor_controller/HG7881-motors_LCD_PWM.py
# PWM test version
#  N.B. it is important not to 'mix' PWM and simple on/off as this seems to confuse the HG7881

########################################################
## generic LCD display function
########################################################
def lcddisp(text1, text2, stime):
    mylcd.lcd_clear()
    mylcd.lcd_display_string(text1, 1, 0)   # display at row 1 column 0
    mylcd.lcd_display_string(text2, 2, 0)   # display at row 2 column 0
    time.sleep(stime)  # short pause to make sure the display above is 'seen'

#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# Raspberry Pi generic set of HG7881 of on/off motor functions 
# 
#  N.B. depending upon how the motors are connected the motor direction
#    signals to the A1B or B1B pins may need to be reversed
#
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

def Aforward_pwm(dutycycleA):   # PWM speed control
    print ("forward " + str(dutycycleA))
    # Motor A - M1
    # set A1A with the PWM dutycycle
    pwm_A1A.start(100-dutycycleA)    # inverse for some reason????
    # set A1B ON i.e. HIGH for forward motion
    GPIO.output(A1B, 1)

def Bforward_pwm(dutycycleB):   # PWM speed control
    # Motor B - M2
    # set B1A with the PWM dutycycle
    pwm_B1A.start(100-dutycycleB)   # inverse for some reason????
    # set B1B ON i.e. HIGH for forward motion
    GPIO.output(B1B, 1)

def Abackward_pwm(dutycycleA):   # PWM speed control
    print ("backward " + str(dutycycleA))
    # Motor A - M1
    # set A1A with the PWM dutycycle
    pwm_A1A.start(dutycycleA)
    # set A1B OFF i.e. LOW for backward motion
    GPIO.output(A1B, 0)

def Bbackward_pwm(dutycycleB):   # PWM speed control
    # Motor B - M2
    # set B1A with the PWM dutycycle
    pwm_B1A.start(dutycycleB)
    # set B1B OFF i.e. LOW for backward motion 
    GPIO.output(B1B, 0)

def Astop():
    print ("stop A")
    GPIO.output(A1B, 0)
    pwm_A1A.start(0)
    print ("motor A set to stop")
    lcddisp("Driving motors:", "motor A off", 3)

def Bstop():
    print ("stop B")
    GPIO.output(B1B, 0)
    pwm_B1A.start(0)
    print ("motor B set to stop")
    lcddisp("Driving motors:", "motor B off", 2)

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

# set the various PWM parameters
# How many times to turn the GPIO pin on and off each second 
Frequency = 20

# Set the GPIO Pin modes
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(A1A, GPIO.OUT)
GPIO.setup(A1B, GPIO.OUT)
GPIO.setup(B1A, GPIO.OUT)
GPIO.setup(B1B, GPIO.OUT)
pwm_A1A = GPIO.PWM(A1A, Frequency)  # set the A1A pin as a software set PWM pin
pwm_B1A = GPIO.PWM(B1A, Frequency)  # set the B1A pin as a software set PWM pin



##########################
###     motor tests    ###
##########################

print ("*** driving motors A + B through a fwd/back cycle continuously - press CTRL C to exit ***")

try:           # this loop is not strictly necessary but it does allow the script to be easily stopped with CTRL-C
    while True:  # this is the loop that continuously runs the motor test cycle

        # Turn all motors off
        Astop()
        Bstop()

        # motor A forwards 25%
        Aforward_pwm(25)
        print ("motor A forward 25%")
        lcddisp("Driving motors:", "motor A fwd 25%", 0)
        # Run the motor for 3 seconds
        time.sleep(3)

        # Turn motor A off
        Astop()

        # motor B forwards 25%
        Bforward_pwm(25)
        print ("motor B forward 25%")
        lcddisp("Driving motors:", "motor B fwd 25%", 0)
        # Run the motor for 3 seconds
        time.sleep(3)

        # Turn motor B off
        Bstop()

        # motor A forwards 75%
        Aforward_pwm(75)
        print ("motor A forward 75%")
        lcddisp("Driving motors:", "motor A fwd 75%", 0)
        # Run the motor for 3 seconds
        time.sleep(3)

        # Turn motor A off
        Astop()

        # motor B forwards 75%
        Bforward_pwm(75)
        print ("motor B forward 75%")
        lcddisp("Driving motors:", "motor B fwd 75%", 0)
        # Run the motor for 3 seconds
        time.sleep(3)

        # Turn motor B off
        Bstop()

        # motor A backwards 25%
        Abackward_pwm(25)
        print ("motor A backward 25%")
        lcddisp("Driving motors:", "motor A back 25%", 0)
        # Run the motors for 3 seconds
        time.sleep(3)

        # Turn motor A off
        Astop()

        # motor B backwards 25%
        Bbackward_pwm(25)
        print ("motor B backward 25%")
        lcddisp("Driving motors:", "motor B back 25%", 0)
        # Run the motors for 3 seconds
        time.sleep(3)

        # Turn motor B off
        Bstop()

        # motor A backwards 75%
        Abackward_pwm(75)
        print ("motor A backward 75%")
        lcddisp("Driving motors:", "motor A back 75%", 0)
        # Run the motors for 3 seconds
        time.sleep(3)

        # Turn motor A off
        Astop()

        # motor B backwards 75%
        Bbackward_pwm(75)
        print ("motor B backward 75%")
        lcddisp("Driving motors:", "motor B back 75%", 0)
        # Run the motors for 3 seconds
        time.sleep(3)

        # Turn motor B off
        Bstop()

except KeyboardInterrupt:   # this code is run when the 'try' loop is interrupted with a CTRL-C
    print(" ")
    print("Cleaning up the GPIO pins before stopping")
    print(" ")
    print(" ")
    print(" ")

    # Reset the GPIO pins (which will also turn off the motors)
    GPIO.cleanup()
    print ("GPIO cleaned up")
    lcddisp("Driving motors:", "GPIO cleaned up", 3)

    lcddisp("Program ended", " ", 3)
    mylcd.lcd_clear()  # clear LCD screen
    mylcd.backlight(0) # turn off LCD backlight

# The cleanup command sets all the pins back to inputs which protects the
# Pi from accidental shorts-circuits if something metal touches the GPIO pins.
   