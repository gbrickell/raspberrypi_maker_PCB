#!/usr/bin/python
# RPi PCBs PCB - simple object detection triggered by movement sensed by a RCWL-0516 microwave sensor
#
# command: python3 ./RPi_maker_PCB5/sensors/object_detection/microwave_detection/microwave_detect01.py
#

import time                # this imports the module to allow various simple time functions to be used
import RPi.GPIO as GPIO    # this imports the module to allow the GPIO pins to be easily utilised
import os                  # this imports the module to allow direct CLI commands to be run
from builtins import input # allows compatibility for input between Python 2 & 3

# This code sets the RPi to use the BCM (Broadcom) pin numbers which is usually the default but is positively set here
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)   # avoids various warning messages about GPIO pins being already in use

sense_pin = 23   # this is the GPIO input pin that the usual PIR OUT pin is connected to, which is a 
                 #  simple way to connect the sensor to the PCB as the 3 main pins are aligned similarly

GPIO.setup(sense_pin, GPIO.IN)   # this sets the input GPIO pin from the PIR to be an input 'type' i.e. it will register  
                               #  either HIGH or LOW depending upon whether it sees a c. 3.3V at the pin 

# initialise some control variables
Current_State  = 0      # simple variable to indicate the detection state
trigger_interval = 3    # minimum interval in seconds between detections to allow the electronics to reset
                        # the default on the electronics is 2 seconds

# get the current date and time in a specified format
# as this string will be used in output
now = time.strftime("%Y-%m-%d_%H.%M.%S")   # this creates a string in a designated format e.g. YYYY-mm-dd_HH.MM.SS


print (now + " - program running : using a RCWL-0516 physical movement detection to print an output - type CTRL-C to stop")
try:    # this loop is not strictly necessary but it does allow the script to be easily stopped with CTRL-C

    #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    # wait a short period for the RCWL-0516 module electronic to settle 
    #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    print ("Waiting for RCWL-0516 electronics to initially settle ...")
 
    # Initial mini loop to wait until until microwave sensor output is 0 ie the electronics have settled
    while GPIO.input(sense_pin) == 1:
        Current_State  = 0    
    print ("  Ready - starting detection loop at: " + time.strftime('%a %d %b %Y %H:%M:%S %Z'))
    print ("**********************************************************************")

    while True:  # this is the loop that checks if the RCWL-0516 is triggered

        #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        # check for movement detection
        #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        # Read RCWL-0516 state from the input GPIO pin
        Current_State = GPIO.input(sense_pin)
        #print (" Current State = " + str(Current_State))  # debug output usually commented out

        if Current_State == 1:
            #RCWL-0516 is triggered 
            print ("  RCWL-0516 movement detected at: " + time.strftime('%a %d %b %Y %H:%M:%S %Z'))
            print ("**********************************************************************")
            time.sleep(trigger_interval)
            print (" waited " + str(trigger_interval) + " seconds to let the electronics reset")
            print (" Looking for a movement to be detected")
            Current_State  = 0

        time.sleep(0.5)  # this is just a short pause so that the processor is not monopolised by this loop


finally:  # this code is run when the try is interrupted with a CTRL-C
    print(" ")
    print("Cleaning up the GPIO pins before stopping")
    print(" ")
    print(" ")
    print(" ")
    GPIO.cleanup()
    
# The cleanup command sets all the pins back to inputs which protects the
# Pi from accidental shorts-circuits if something metal touches the GPIO pins.

