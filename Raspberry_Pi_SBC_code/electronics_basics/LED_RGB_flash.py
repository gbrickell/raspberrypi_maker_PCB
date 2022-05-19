# RPi kits PCB version of LED_RGB_flash.py that alternates on/off for the individual red, green & blue LEDs within a combined RGB LED
# this script introduces the use of pulse width modulation (PWM) a technique used to control a variety of 
# devices (motors, servos as well as LEDs) essentially by switching them on and off very very fast
# PWM has 2 main parameters:
#  - Frequency: the number of time per second that a pulse is generated
#  - Duty Cycle: the % of time during a single cycle that the signal is high
# for more information see https://pythonhosted.org/RPIO/pwm_py.html
#   and https://en.wikipedia.org/wiki/Pulse-width_modulation
#
# command to run this script:  python3 ./RPi_maker_kit5/electronic_basics/LED_RGB_flash.py

import RPi.GPIO as GPIO   # this imports the whole GPIO module to allow control of the GPIO pins including PWM commands
import time               # this imports the time module to allow various time functions to be used
GPIO.setwarnings(False)

# This code sets the RPi to use the BCM (Broadcom) pin numbers which is usually the default but is positively set here
GPIO.setmode(GPIO.BCM)

red_positive_pin = 22  # this is the GPIO pin that the RED RGB leg (via the resistor) is connected to
                       # it could be any of the GPIO pins as long as this software is aligned to the hardware 

green_positive_pin = 27  # this is the GPIO pin that the GREEN RGB leg (via the resistor) is connected to
                         # it could be any of the GPIO pins as long as this software is aligned to the hardware

blue_positive_pin = 17   # this is the GPIO pin that the BLUE RGB leg (via the resistor) is connected to
                         # it could be any of the GPIO pins as long as this software is aligned to the hardware


GPIO.setup(red_positive_pin, GPIO.OUT)  # this sets the RED GPIO pin to be an output 'type' i.e. it will 
                                        # apply about 3.3V to the pin when it is set HIGH (True)

GPIO.setup(green_positive_pin, GPIO.OUT)  # this sets the GREEN GPIO pin to be an output 'type' i.e. it will 
                                          # apply about 3.3V to the pin when it is set HIGH (True)

GPIO.setup(blue_positive_pin, GPIO.OUT)   # this sets the BLUE GPIO pin to be an output 'type' i.e. it will 
                                          # apply about 3.3V to the pin when it is set HIGH (True)

# Start the Pulse Width Modulation (PWM) software on each of the LED GPIO control pins which will allow the
#  brightness of the LEDs to be controllable: a quite high frequency is needed for LEDs to avoid visible flicker

pwmRed = GPIO.PWM(red_positive_pin, 500)      # this sets a frequency of 500 i.e. 500 cycles per second
pwmRed.start(0)                               # this sets an inital Duty Cycle of 0% i.e. off all the time

pwmGreen = GPIO.PWM(green_positive_pin, 500)  # this sets a frequency of 500 i.e. 500 cycles per second
pwmGreen.start(0)                             # this sets an inital Duty Cycle of 0% i.e. off all the time

pwmBlue = GPIO.PWM(blue_positive_pin, 500)    # this sets a frequency of 500 i.e. 500 cycles per second
pwmBlue.start(0)                              # this sets an inital Duty Cycle of 0% i.e. off all the time

###########
# main code
###########

print (" ")
print ("program running - RGB LED colours should be alternating: CTRL-C to stop ")
print (" ")


try:           # this loop is not strictly necessary but it does allow the script to be easily stopped with CTRL-C
    while True:  # this is the loop that continuously flashes the LED on and off every 1.5 seconds
        pwmRed.ChangeDutyCycle(100)             # red LED switched to 100% (fully on) by changing the Duty Cycle
        pwmGreen.ChangeDutyCycle(0)             # green LED switched to 0% (off) by changing the Duty Cycle
        pwmBlue.ChangeDutyCycle(0)              # blue LED switched to 0% (off) by changing the Duty Cycle
        time.sleep(1.5)                         # delay 1.5 seconds 
        pwmRed.ChangeDutyCycle(0)               # red LED switched to 0% (off) by changing the Duty Cycle
        pwmGreen.ChangeDutyCycle(100)           # green LED switched to 100% (fully on) by changing the Duty Cycle
        pwmBlue.ChangeDutyCycle(0)              # blue LED switched to 0% (off) by changing the Duty Cycle
        time.sleep(1.5)                         # delay 1.5 seconds before looping back
        pwmRed.ChangeDutyCycle(0)               # red LED switched to 0% (off) by changing the Duty Cycle
        pwmGreen.ChangeDutyCycle(0)             # green LED switched to 0% (off) by changing the Duty Cycle
        pwmBlue.ChangeDutyCycle(100)            # blue LED switched to 100% (fully on) by changing the Duty Cycle
        time.sleep(1.5)                         # delay 1.5 seconds before looping back


finally:  # this code is run when the try is interrupted with a CTRL-C
    print(" ")
    print("Cleaning up the GPIO pins before stopping")
    print(" ")
    print(" ")
    print(" ")
    GPIO.cleanup()
    
# The cleanup command sets all the pins back to inputs which protects the
# Pi from accidental shorts-circuits if something metal touches the GPIO pins.
    