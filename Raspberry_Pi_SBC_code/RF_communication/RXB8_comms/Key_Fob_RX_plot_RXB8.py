#!/usr/bin/python
# Key_Fob_RX_plot_RXB8.py 
# RPi PCBs PCB RF comms test routine

# Basic RF code receiver using the RXB8 
# used with the key fob buttons to receive and plot the A and B button signals
# the script will run for MAX_DURATION seconds and then stop
# Note: only run this script with the RPi assembly directly connected to a screen etc so that the 
# plot processes will automatically run in a separate X-window  

# Command to run:  python3 ./RPi_maker_PCB5/RF_communication/RXB8_comms/Key_Fob_RX_plot_RXB8.py
## edit the command above to change pi to your userId and to adjust 
## the file path depending upon where you have stored this file
#

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
from datetime import datetime
import matplotlib.pyplot as pyplot
import time               # this imports the time module to allow various time functions to be used
import RPi.GPIO as GPIO   # this imports the whole GPIO module to allow control of the GPIO pins including PWM commands

# This code sets the RPi to use the BCM (Broadcom) pin numbers which is usually the default but is positively set here
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

RX_red_pin = 22   # this is the GPIO pin that the RED RGB LED is connected to on the Maker PCB PCB 

RX_green_pin = 27 # this is the GPIO pin that the GREEN RGB LED is connected to on the Maker PCB PCB 

RX_blue_pin = 17  # this is the GPIO pin that the BLUE RGB LED is connected to on the Maker PCB PCB 

TX_red_pin = 16     # this is the GPIO pin that the RED LED is connected to on the Maker PCB PCB 

TX_amber_pin = 14   # this is the GPIO pin that the AMBER LED is connected to on the Maker PCB PCB

TX_green_pin = 15  # this is the GPIO pin that the GREEN LED is connected to on the Maker PCB PCB 

GPIO.setup(RX_red_pin, GPIO.OUT)    # this sets the RX RED GPIO pin to be an output 'type' i.e. it will 
                                    # apply about 3.3V to the pin when it is set HIGH (True)
GPIO.setup(RX_green_pin, GPIO.OUT)  # this sets the RX GREEN GPIO pin to be an output 'type' i.e. it will 
                                    # apply about 3.3V to the pin when it is set HIGH (True)
GPIO.setup(RX_blue_pin, GPIO.OUT)   # this sets the RX BLUE GPIO pin to be an output 'type' i.e. it will 
                                    # apply about 3.3V to the pin when it is set HIGH (True)

GPIO.setup(TX_red_pin, GPIO.OUT)    # this sets the TX RED GPIO pin to be an output 'type' i.e. it will 
                                    # apply about 3.3V to the pin when it is set HIGH (True)
GPIO.setup(TX_green_pin, GPIO.OUT)  # this sets the TX GREEN GPIO pin to be an output 'type' i.e. it will 
                                    # apply about 3.3V to the pin when it is set HIGH (True)
GPIO.setup(TX_amber_pin, GPIO.OUT)  # this sets the TX BLUE GPIO pin to be an output 'type' i.e. it will 
                                    # apply about 3.3V to the pin when it is set HIGH (True)

# Start the Pulse Width Modulation (PWM) software on each of the LED GPIO control pins which will allow the
#  brightness of the LEDs to be controllable: a quite high frequency is needed for LEDs to avoid visible flicker
pwmRXred = GPIO.PWM(RX_red_pin, 500)      # this sets a frequency of 500 i.e. 500 cycles per second
pwmRXred.start(0)                         # this sets an inital Duty Cycle of 0% i.e. off all the time
pwmRXgreen = GPIO.PWM(RX_green_pin, 500)  # this sets a frequency of 500 i.e. 500 cycles per second
pwmRXgreen.start(0)                       # this sets an inital Duty Cycle of 0% i.e. off all the time
pwmRXblue = GPIO.PWM(RX_blue_pin, 500)    # this sets a frequency of 500 i.e. 500 cycles per second
pwmRXblue.start(0)                        # this sets an inital Duty Cycle of 0% i.e. off all the time

pwmTXred = GPIO.PWM(TX_red_pin, 500)      # this sets a frequency of 500 i.e. 500 cycles per second
pwmTXred.start(0)                         # this sets an inital Duty Cycle of 0% i.e. off all the time
pwmTXgreen = GPIO.PWM(TX_green_pin, 500)  # this sets a frequency of 500 i.e. 500 cycles per second
pwmTXgreen.start(0)                       # this sets an inital Duty Cycle of 0% i.e. off all the time
pwmTXblue = GPIO.PWM(TX_amber_pin, 500)   # this sets a frequency of 500 i.e. 500 cycles per second
pwmTXblue.start(0)                        # this sets an inital Duty Cycle of 0% i.e. off all the time

buzzer_pin = 12
GPIO.setup(buzzer_pin, GPIO.OUT)

print("program running")
pwmTXgreen.ChangeDutyCycle(100)
pwmRXred.ChangeDutyCycle(100) 
time.sleep(2)  # pause for 2 seconds just so the LEDs can be seen

pwmRXred.ChangeDutyCycle(0)
pwmRXblue.ChangeDutyCycle(100)
RECEIVED_SIGNAL = [[], []]  #[[time of reading], [signal reading]]
MAX_DURATION = 5
RECEIVE_PIN = 18       # either of the data pins on the C218D001C RF board
                       # the two middle pins are bridged together as 'alternates'

GPIO.setup(RECEIVE_PIN, GPIO.IN)
time.sleep(2)  # pause for 2 seconds just so the LEDs can be seen
# 0.1 second beep x3 
beep(3, 0.1)
print("press a key fob button several times now ")

cumulative_time = 0
beginning_time = datetime.now()
print ('**Started recording**')
while cumulative_time < MAX_DURATION:
    time_delta = datetime.now() - beginning_time
    RECEIVED_SIGNAL[0].append(time_delta)
    RECEIVED_SIGNAL[1].append(GPIO.input(RECEIVE_PIN))
    cumulative_time = time_delta.seconds
print( '**Ended recording**')
pwmRXblue.ChangeDutyCycle(0)
pwmRXgreen.ChangeDutyCycle(100)
print (str(len(RECEIVED_SIGNAL[0])) + ' samples recorded')

print ('**Processing results**')
for i in range(len(RECEIVED_SIGNAL[0])):
    RECEIVED_SIGNAL[0][i] = RECEIVED_SIGNAL[0][i].seconds + RECEIVED_SIGNAL[0][i].microseconds/1000000.0

print ('**Plotting results**')
pyplot.plot(RECEIVED_SIGNAL[0], RECEIVED_SIGNAL[1])
pyplot.axis([0, MAX_DURATION, -1, 2])
pyplot.show()
print ("plot finished")
pwmRXred.ChangeDutyCycle(0)
pwmRXgreen.ChangeDutyCycle(0)
pwmRXblue.ChangeDutyCycle(0)
pwmTXred.ChangeDutyCycle(0)
pwmTXgreen.ChangeDutyCycle(0)
pwmTXblue.ChangeDutyCycle(0)

pwmRXred.stop
pwmRXgreen.stop
pwmRXblue.stop
pwmTXred.stop
pwmTXgreen.stop
pwmTXblue.stop

GPIO.cleanup()
print ("all done")
