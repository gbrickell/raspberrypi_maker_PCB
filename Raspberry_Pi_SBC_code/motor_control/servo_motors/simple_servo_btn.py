#!/usr/bin/python
#
# RPi PCB version of servo_btn.py - simple servo control with GPIO PWM and powered from RPi
# moves a SG90 servo with GPIO PWM from min to max position whenever a button is pressed
# SG90 servo has 3 wires: brown  -  GND
#                         red    -  5V supply
#                         orange -  PWM signal/control
#
# command:  python3 ./RPi_maker_PCB5/motor_control/servo_motors/simple_servo_btn.py
#

import time               # this imports the module to allow various time functions to be used
import RPi.GPIO as GPIO   # this imports the module to allow the GPIO pins to be easily utilised

# This code sets the RPi to use the BCM (Broadcom) pin numbers which is usually the default but is positively set here
GPIO.setmode(GPIO.BCM)

button_pin = 26  # this is the GPIO pin that one side of the tactile button 2 is connected to
                 # it could be any of the GPIO pins as long as this software is aligned to the hardware

pwm_pin = 24     # this is the GPIO pin used for servo control connected to the S1 3 pin male connector

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
# this is a special setting that indicates when a pin changes from LOW to HIGH ie when the button is pressed

GPIO.setup(pwm_pin, GPIO.OUT)  # set the GPIO PWM pin as an output
servo = GPIO.PWM(pwm_pin, 50)  # set PWM on the control GPIO pin with frequency 50Hz

# this is a function to indicate when the button is pressed 
def btn_pressed():
    # if button is pressed GPIO.input will report FALSE
    if not GPIO.input(button_pin):
        return 1

# set the min and max duty cycles for the servo
servo_mindc = 3   # needs to be less than 1ms pulses ie <5% duty cycle - see the support documentation for more details
servo_middc = 7.5 # needs to be 1.5ms pulses ie 7.5% duty cycle - see the support documentation for more details
servo_maxdc = 13  # needs to be more than 2ms pulses ie >10% duty cycle - see the support documentation for more details

servo.start(servo_middc)   # sets an initial duty cycle to move servo to the central position

print("Program running: press button 2 to move the servo from min to max once - CTRL C to stop")
try:    # this loop is not strictly necessary but it does allow the script to be easily stopped with CTRL-C
    while True:  # this is the loop that checks if a button is pressed and moves each servo arm if it is

        while not btn_pressed():
            pass                         # if the button is not pressed just loop endlessly

        # button 2 pressed so move servo between extremes.
        print("button 2 pressed - moving servo")
        servo.ChangeDutyCycle(servo_mindc)    # move servo to the min position
        time.sleep(1)
        servo.ChangeDutyCycle(servo_maxdc)    # move servo to the max position
        time.sleep(1)
        servo.ChangeDutyCycle(servo_middc)    # move servo back to the mid position
        time.sleep(1)
        print("press button 2 again to move the servo or CTRL C to stop")

finally:  # this code is run when the try is interrupted with a CTRL-C
    print(" ")
    print("Cleaning up the GPIO pins before stopping")
    print(" ")
    print(" ")
    print(" ")
    servo.stop()
    GPIO.cleanup()
    
# The cleanup command sets all the pins back to inputs which protects the
# Pi from accidental shorts-circuits if something metal touches the GPIO pins.

