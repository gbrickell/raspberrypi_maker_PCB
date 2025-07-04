#!/usr/bin/python
# TTP229_test01.py shows how the TTP229 touch keypad is used 
#  uses two of the spare GPIO poins onthe PCB
# Author : Enmore Green Limited
# Date   : 210511
# command to run this script:  python3 ./RPi_maker_PCB5/sensors/TTP229_touch_keypad/TTP229_test01.py
#  command above to be updated for the user's path to the code


import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
SCLPin=18
SDOPin=15

HALF_BIT_TIME=.001
CHARACTER_DELAY=5*HALF_BIT_TIME

NUM_BITS=16

GPIO.setup(SCLPin,GPIO.OUT)
GPIO.setup(SDOPin,GPIO.IN)

GPIO.output(SCLPin,GPIO.HIGH)
time.sleep(HALF_BIT_TIME)
oldKey=18

try:
    while True:
        button=1
        time.sleep(CHARACTER_DELAY)


        while button < 17:
            print_button=button
            if (print_button==17):
                print_button=1

            GPIO.output(SCLPin,GPIO.LOW)
            time.sleep(HALF_BIT_TIME)
            keyval=GPIO.input(SDOPin)
            if not keyval and not pressed:
                pressed=True
                if(oldKey!=button) :
                    print(print_button)
                    oldKey=button
            GPIO.output(SCLPin,GPIO.HIGH)
            time.sleep(HALF_BIT_TIME)

            button+=1

        pressed=False

except KeyboardInterrupt:
    pass
    GPIO.cleanup()


