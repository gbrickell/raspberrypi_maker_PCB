#!/usr/bin/python

# RPi kits PCB version of I2C_2servo_btn.py - servo control using a PCA9685 I2C controller
# moves servos on channels 0 and 15 from min to max position whenever each button is pressed
#
# command:  python3 ./RPi_maker_PCB5/motor_control/servo_motors/I2C_2servo_btn.py
#

import time               # this imports the module to allow various time functions to be used
import RPi.GPIO as GPIO   # this imports the module to allow the GPIO pins to be easily utilised
GPIO.setwarnings(False)

import Adafruit_PCA9685   # this imports a library that interfaces with the I2C servo control board (PCA9685)
                          #   and provides a set of PWM (pulse width modulation) functions the board can supply
# use i2cdetect -y 1 to check what is connected

# This code sets the RPi to use the BCM (Broadcom) pin numbers which is usually the default but is positively set here
GPIO.setmode(GPIO.BCM)

btn1_pin = 7   # this is the GPIO pin that one side of the tactile button 1 is connected to

btn2_pin = 26  # this is the GPIO pin that one side of the tactile button 2 is connected to

GPIO.setup(btn1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
# this is a special setting that indicates when a pin changes from LOW to HIGH ie when the button is pressed
GPIO.setup(btn2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
# this is a special setting that indicates when a pin changes from LOW to HIGH ie when the button is pressed

# this is a function to indicate when either button 1 or 2 is pressed 
def btn_pressed(btnpin1, btnpin2):
    # if either button is pressed its GPIO.input will report FALSE
    if not GPIO.input(btnpin1):
        #print("button 1 pressed") # remove the # in front of the print to uncomment this debug output
        return 1
    if not GPIO.input(btnpin2):
        #print("button 2 pressed") # remove the # in front of the print to uncomment this debug output
        return 2

# Initialise the servo control board assuming it has its 
#  default address hex 40 (0x40) and is the only device on the bus
#  this can be checked by running "sudo i2cdetect -y 1"
#  for all recent RPi models the port# is 1 in the above 'detect' command - but for pre-Oct'12 models it is 0
pwm = Adafruit_PCA9685.PCA9685()

# If for some reason the I2C device set up is not the default then use the following:
#    pwm = Adafruit_PCA9685.PCA9685(address=0x??, busnum=?)


pwm.set_pwm_freq(50)   # set the PWM frequency to 50Hz - as per the SG90 data sheet.

# set the min and max servo pulse lengths

# min: 1ms pulse length ie should be 205 steps out of 4096 but fine tuned for the specific servo - see the support documentation for more details
servo1_min = 130   # channel 0 left hand servo

# mid: 1.5ms pulse length ie should be 308 steps out of 4096 but fine tuned for the specific servo - see the support documentation for more details 
servo1_mid = 350   # channel 0 left hand servo

# max: 2ms pulse length ie should be 410 steps out of 4096 but fine tuned for the specific servo - see the support documentation for more details
servo1_max = 580   # channel 0 left hand servo

# min: 1ms pulse length ie should be 205 steps out of 4096 but fine tuned for the specific servo - see the support documentation for more details
servo2_min = 160   # channel 15 right hand servo

# mid: 1.5ms pulse length ie should be 308 steps out of 4096 but fine tuned for the specific servo - see the support documentation for more details 
servo2_mid = 365   # channel 15 right hand servo

# max: 2ms pulse length ie should be 410 steps out of 4096 but fine tuned for the specific servo - see the support documentation for more details
servo2_max = 615   # channel 15 right hand servo

print("Program running: press a button to move a servo from min to max once - CTRL C to stop")
try:    # this loop is not strictly necessary but it does allow the script to be easily stopped with CTRL-C
    while True:  # this is the loop that checks if a button is pressed and moves each servo arm if it is
        btn_state = btn_pressed(btn1_pin, btn2_pin)
        #print("button state: " + str(btn_state))  # remove the # in front of the print to uncomment this debug output
        while btn_pressed(btn1_pin, btn2_pin) != 1 and btn_pressed(btn1_pin, btn2_pin) != 2 :
            pass                         # if neither button pressed just loop endlessly

        if btn_state == 1:  # button 1 pressed so move servo on channel O between extremes.
            print("button 1 pressed - moving servo on channel 0")
            pwm.set_pwm(0, 0, servo1_min)
            time.sleep(1)
            pwm.set_pwm(0, 0, servo1_max)
            time.sleep(1)
            pwm.set_pwm(0, 0, servo1_mid)
            time.sleep(1)

        if btn_state == 2:  # button 2 pressed so move servo on channel 15 between extremes.
            print("button 2 pressed - moving servo on channel 15")
            pwm.set_pwm(15, 0, servo2_min)
            time.sleep(1)
            pwm.set_pwm(15, 0, servo2_max)
            time.sleep(1)
            pwm.set_pwm(15, 0, servo2_mid)
            time.sleep(1)

        print("press button 1 or 2 again to move the servos or CTRL C to stop")

finally:  # this code is run when the try is interrupted with a CTRL-C
    print(" ")
    print("Cleaning up the GPIO pins before stopping")
    print(" ")
    print(" ")
    print(" ")
    GPIO.cleanup()
    
# The cleanup command sets all the pins back to inputs which protects the
# Pi from accidental shorts-circuits if something metal touches the GPIO pins.


