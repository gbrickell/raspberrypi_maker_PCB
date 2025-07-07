#!/usr/bin/python
# TTP229_test02.py shows how the TTP229 touch keypad is used 
#  uses two of the spare GPIO poins onthe PCB
# Author : Enmore Green Limited
# Date   : 210511
# command to run this script:  python3 ./RPi_maker_PCB5/sensors/TTP229_touch_keypad/TTP229_test02.py
#  command above to be updated for the user's path to the code

import RPi.GPIO as GPIO
import time


"""No. of keys"""
inputKeys=16

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) 
""" SCL and SDO pin can be any pin """
SCLPin=18  #using a spare GPIO pin on the RPi Maker PCB PCB
SDOPin=15  #using a spare GPIO pin on the RPi Maker PCB PCB

"""
Set SCL pin as OUTPUT
Set SDO pin as INPUT
"""

GPIO.setup(SCLPin,GPIO.OUT)
GPIO.setup(SDOPin,GPIO.IN)

keyPressed=0

def getKey():
        button=0
        global keyPressed
        keyState=0
        time.sleep(0.05)

        """
        Sample the Clock pin 16 times and read the data pin,
        when touched data pin is recorded LOW.
        """
        for i in range(inputKeys):
                GPIO.output(SCLPin,GPIO.LOW)
                if not GPIO.input(SDOPin):
                        keyState=i+1
                GPIO.output(SCLPin, GPIO.HIGH)
                
        if (keyState>0 and keyState!=keyPressed):
                button=keyState
                keyPressed=keyState
        else:
                keyPressed=keyState
        return (button)
        
        

while True:
        key=getKey()
        if(key>0):
                print("key " + str(key) + " pressed")
        
