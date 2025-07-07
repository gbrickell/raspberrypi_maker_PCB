#!/usr/bin/python

# RPi PCBs PCB version of I2C_servo_btn.py - servo control using a PCA9685 I2C controller
# moves a SG90 servo on channel 0 from min to max position whenever a button is pressed
#
# command:  python3 ./RPi_maker_PCB5/motor_control/servo_motors/I2C_servo_btn.py

# CLI command to check I2C address:  i2cdetect -y -r 1
#

import time               # this imports the module to allow various time functions to be used
import RPi.GPIO as GPIO   # this imports the module to allow the GPIO pins to be easily utilised
GPIO.setwarnings(False)

import Adafruit_PCA9685   # this imports a library that supports the I2C servo control board (PCA9685)
# use i2cdetect -y 1 to check what is connected

# This code sets the RPi to use the BCM (Broadcom) pin numbers which is usually the default but is positively set here
GPIO.setmode(GPIO.BCM)

button_pin = 26  # this is the GPIO pin for button 2 that one side of the tactile button is connected to

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
# this is a special setting that indicates when a pin changes from LOW to HIGH ie when the button is pressed

# this is a function to indicate when the button is pressed 
def btn_pressed():
    # if button is pressed GPIO.input will report FALSE
    if not GPIO.input(button_pin):
        return 1

# Initialise the servo control board assuming it has its 
#  default address hex 40 (0x40) and is the only device on the bus
#  this can be checked by running "sudo i2cdetect -y 1"
#  for all recent RPi models the port# is 1 in the above 'detect' command - but for pre-Oct'12 models it is 0
pwm = Adafruit_PCA9685.PCA9685()
print("PCA9685 initialised")

# If for some reason the I2C device set up is not the default then use the following:
#    pwm = Adafruit_PCA9685.PCA9685(address=0x??, busnum=?)


pwm.set_pwm_freq(50)   # set the PWM frequency to 50Hz - as per the SG90 data sheet.
print("PWM frequency set")

# set the min and max servo pulse lengths

# min: 1ms pulse length ie should be 205 steps out of 4096 but fine tuned for the specific servo - see the support documentation for more details
servo_min = 150 

# max: 1.5ms pulse length ie should be 308 steps out of 4096 but fine tuned for the specific servo - see the support documentation for more details 
servo_mid = 350 

# mid: 2ms pulse length ie should be 410 steps out of 4096 but fine tuned for the specific servo - see the support documentation for more details
servo_max = 600 

print("Program running: press the button 2 to move the servo from min to max once - CTRL C to stop")
try:    # this loop is not strictly necessary but it does allow the script to be easily stopped with CTRL-C
    while True:  # this is the loop that checks if a button is pressed and moves each servo arm if it is

        while not btn_pressed():
            pass                         # if the button is not pressed just loop endlessly

        # button pressed so move servo on channel O between extremes.
        print("button pressed - moving servo on channel 0")
        pwm.set_pwm(0, 0, servo_min)
        time.sleep(1)
        pwm.set_pwm(0, 0, servo_max)
        time.sleep(1)
        pwm.set_pwm(0, 0, servo_mid)
        time.sleep(1)
        print("press the button 2 again to move the servo or CTRL C to stop")

finally:  # this code is run when the try is interrupted with a CTRL-C
    print(" ")
    print("Cleaning up the GPIO pins before stopping")
    print(" ")
    print(" ")
    print(" ")
    GPIO.cleanup()
    
# The cleanup command sets all the pins back to inputs which protects the
# Pi from accidental shorts-circuits if something metal touches the GPIO pins.

