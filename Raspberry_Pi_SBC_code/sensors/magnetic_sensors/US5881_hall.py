#!/usr/bin/python
# RPi kits PCB - simple Hall effect sensor test program using a US5881 
#  with the signal wire connected to GPIO#18
#
# command: python3 ./RPi_maker_PCB5/sensors/magnetic_sensors/US5881_hall.py
#

##################################
######## various functions #######
##################################

def sensorCallback(channel):
  # Called if sensor output changes
  timestamp = time.time()
  stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
  if GPIO.input(channel):
    # No magnet
    print("Sensor HIGH - no south pole detected " + stamp)
  else:
    # Magnet
    print("Sensor LOW - magnet south pole detected " + stamp)

#################################
########## main code ############
#################################

import time                # these import the modules to allow various simple time/date functions to be used
import datetime
import RPi.GPIO as GPIO    # this imports the module to allow the GPIO pins to be easily utilised
# Tell GPIO library to use GPIO references
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

print("Setup GPIO pin as input on Maker Kit spare GPIO18")

# Set Switch GPIO as input
# Pull high by default
GPIO.setup(18 , GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(18, GPIO.BOTH, callback=sensorCallback, bouncetime=200)

# Get initial reading
sensorCallback(18)

try:    # this loop is not strictly necessary but it does allow the script to be easily stopped with CTRL-C

    while True:  # this is the loop that simply waits until the US5881 is triggered
        time.sleep(0.1)


finally:  # this code is run when the try is interrupted with a CTRL-C
    print(" ")
    print("Cleaning up the GPIO pins before stopping")
    print(" ")
    print(" ")
    print(" ")
    GPIO.cleanup()
    
# The cleanup command sets all the pins back to inputs which protects the
# Pi from accidental shorts-circuits if something metal touches the GPIO pins.