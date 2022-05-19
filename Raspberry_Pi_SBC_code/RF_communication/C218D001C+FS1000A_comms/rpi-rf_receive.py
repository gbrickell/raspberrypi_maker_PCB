#!/usr/bin/env python3
# rpi-rf_receive.py 
# RPi kits PCB RF comms test routine
# this version for use with the C218D001C receiver module

# Command to run:  python3 ./RPi_maker_kit5/RF_communication/C218D001C+FS1000A_comms/rpi-rf_receive.py
## edit the command above to change pi to your userId and to adjust 
## the file path depending upon where you have stored this file
#

# adapted version of original script from rpi-rf Python library at https://github.com/milaq/rpi-rf
# used with the key fob buttons A & B to receive and display the A and B button signals
# output now includes a 'clean' 24 character binary code and filters out non-Key Fob codes that are 'in the air'

####################################################################
#  basic buzzer functions
#  only does something if the 'installed' parameter is 'yes'
#  and assumes the buzzer pin is already set as an OUTPUT
####################################################################

def buzz(frequency, length):	 #function "buzz" is fed the pitch (frequency) and duration (length in seconds)
    # allow for a 'silent' duration
    if(frequency==0):
        time.sleep(length)
        return
    period = 1.0 / frequency 		     #in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
    delayValue = period / 2		         #calcuate the time for half of the wave
    numCycles = int(length * frequency)	 #the number of waves to produce is the duration times the frequency
	
    for i in range(numCycles):		   #start a loop from 0 to the variable "cycles" calculated above
        GPIO.output(buzzer_pin, True)  #set buzzer pin to high
        time.sleep(delayValue)		   #wait with buzzer pin high
        GPIO.output(buzzer_pin, False) #set buzzer pin to low
        time.sleep(delayValue)		   #wait with buzzer pin low

def beep(number, length):  # simple function for beep length and on/off for 'number' times at standard beep frequency 1200Hz
    for i in range(1, number+1):
        #print ("beep: " + str(i))
        buzz(1200, length)
        time.sleep(length)




###################
#  main code
###################

import argparse
import signal
import sys
import time
import logging

from rpi_rf import RFDevice

import RPi.GPIO as GPIO   # this imports the whole GPIO module to allow control of the GPIO pins including PWM commands

# This code sets the RPi to use the BCM (Broadcom) pin numbers which is usually the default but is positively set here
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

rfdevice = None

buzzer_pin = 12
GPIO.setup(buzzer_pin, GPIO.OUT)

# pylint: disable=unused-argument
def exithandler(signal, frame):
    rfdevice.cleanup()
    sys.exit(0)

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )

parser = argparse.ArgumentParser(description='Receives a decimal code via a 433/315MHz GPIO device')
parser.add_argument('-g', dest='gpio', type=int, default=18,
                    help="GPIO pin (Default: 18)")
args = parser.parse_args()

signal.signal(signal.SIGINT, exithandler)
rfdevice = RFDevice(args.gpio)
rfdevice.enable_rx()
timestamp = None
logging.info("Listening for Key Fob codes on GPIO " + str(args.gpio))
while True:
    if rfdevice.rx_code_timestamp != timestamp:
        timestamp = rfdevice.rx_code_timestamp
        code = bin(int(rfdevice.rx_code))[2:].zfill(24)
        # filter out the non-Key Fob codes
        if rfdevice.rx_proto == 1 and rfdevice.rx_pulselength < 480 and rfdevice.rx_pulselength > 457:
            # 0.1 second beep x3 
            beep(1, 0.1)
            logging.info(str(rfdevice.rx_code) + " - " + str(code) +
                         " [pulselength " + str(rfdevice.rx_pulselength) +
                         ", protocol " + str(rfdevice.rx_proto) + "]")
        # 0.1 second beep x3 
        #beep(1, 0.1)
        #logging.info(str(rfdevice.rx_code) + " - " + str(code) +
        #                 " [pulselength " + str(rfdevice.rx_pulselength) +
        #                 ", protocol " + str(rfdevice.rx_proto) + "]")

    time.sleep(0.01)
rfdevice.cleanup()
