#!/usr/bin/python
# RPi kits PCB RF comms test routine
# file name: switch_socket.py
# simple 'raw' OOK code send with STX882 tranmission board to an Energenie green button socket
#
# command to run: python3 ./RPi_maker_kit5/RF_communication/SRX882+STX882_comms/switch_socket02.py
## edit the command above to change pi to your userId and to adjust 
## the file path depending upon where you have stored this file

#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#  basic buzzer functions
#  only does something if the 'installed' parameter is 'yes'
#  and assumes the buzzer pin is already set as an OUTPUT
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

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

#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# this is a function to indicate when a button is pressed 
#
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

def btn_pressed(pin):
    # if button is pressed GPIO.input will report FALSE
    if not GPIO.input(pin):
        return 1

#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# function to transmit a specific code using the 'raw' GPIO pins
#
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

def transmit_raw_code(code):
    '''Transmit a chosen raw code string using the GPIO transmitter pin'''

    for t in range(NUM_ATTEMPTS):
        for i in code:
            if i == '0':
                GPIO.output(TRANSMIT_PIN, True)
                time.sleep(short_delay)
                GPIO.output(TRANSMIT_PIN, False)
                time.sleep(long_delay)
            elif i == '1':
                GPIO.output(TRANSMIT_PIN, True)
                time.sleep(long_delay)
                GPIO.output(TRANSMIT_PIN, False)
                time.sleep(short_delay)
            else:
                continue
        GPIO.output(TRANSMIT_PIN, False)
        time.sleep(extended_delay)
	

#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# main code 
#
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


import time # Import the Time library 
import RPi.GPIO as GPIO # Import the GPIO Library 

# Set the GPIO modes 
GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)

RX_red_pin = 22   # this is the GPIO pin that the RED RGB LED is connected to on the Maker Kit PCB 

RX_green_pin = 27 # this is the GPIO pin that the GREEN RGB LED is connected to on the Maker Kit PCB 

RX_blue_pin = 17  # this is the GPIO pin that the BLUE RGB LED is connected to on the Maker Kit PCB 

TX_red_pin = 16     # this is the GPIO pin that the RED LED is connected to on the Maker Kit PCB 

TX_amber_pin = 20   # this is the GPIO pin that the AMBER LED is connected to on the Maker Kit PCB

TX_green_pin = 21  # this is the GPIO pin that the GREEN LED is connected to on the Maker Kit PCB 

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
GPIO.setup(TX_amber_pin, GPIO.OUT)  # this sets the TX AMBER GPIO pin to be an output 'type' i.e. it will 
                                    # apply about 3.3V to the pin when it is set HIGH (True)

#  all colours initially set to 0 i.e. off
GPIO.output(RX_red_pin, False)
GPIO.output(RX_green_pin, False)
GPIO.output(RX_blue_pin, False)

GPIO.output(TX_red_pin, False)
GPIO.output(TX_amber_pin, False)
GPIO.output(TX_green_pin, False)

# set up the button on the RF transmission breadboard
button_pin = 7     # this is the GPIO pin that one side of the tactile button 1 is connected to
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
# this is a special setting that 'pulls the pin up' when not pressed so 
#  it can indicate when a pin changes from HIGH to LOW ie when the button is pressed


# set up the Energenie socket that is to be switched on/off
# a socket 'house code' and 'device code' must have been previously 'set' with the socket in its learning mode
# separate software is available to do this

# using hex 'abcde' as an example, i.e. binary 1010 1011 1100 1101 1110 - the first set of 20 digits are the 'house code'
# control code 0111 - the first 3 digits (011) is the device ref, then either 1 or 0 is on/off and then a trailing stop bit 0
skttest01_house_on  = '1010101111001101111001110'   # house code is abcde, device code is 011
skttest01_house_off = '1010101111001101111001100'   # house code is abcde, device code is 011


# set the 'raw' pin control parameters
short_delay = 0.00045    # period of time for short duration 'pulse'
long_delay = 0.00090     # period of time for long duration 'pulse'
extended_delay = 0.0096  # period of time for a 'gap' between a series of 'pulses' comprising a complete code

NUM_ATTEMPTS = 10     # number of times to repetitively send an individual code
TRANSMIT_PIN = 14     # signal pin from the transmission board (STX882) powered at 3V3
GPIO.setup(TRANSMIT_PIN, GPIO.OUT)

# initially make sure the socket is switched off
transmit_raw_code(skttest01_house_off)
socketstate = "off"
# set the maker kit RGB LED to red to indicate the remote socket is off
GPIO.output(RX_red_pin, True)
GPIO.output(RX_green_pin, False)
GPIO.output(RX_blue_pin, False)

# set the maker kit RED LED to ON to indicate the remote socket is off
GPIO.output(TX_red_pin, True)
GPIO.output(TX_amber_pin, False)
GPIO.output(TX_green_pin, False)

buzzer_pin = 12
GPIO.setup(buzzer_pin, GPIO.OUT)

print ("program running - hit CTRL C for a clean exit")

try:
    # We will just loop round switching the socket on and off whenever the tactile button is pressed
    while True:
        if socketstate == "off":
            print ("")
            print ("press the button to switch the socket on")
        elif socketstate == "on":
            print ("")
            print ("press the button to switch the socket off")
        else:        
            print ("some error has occured - socket state unrecognised")

        # 0.1 second beep x3 
        beep(3, 0.1)

        while not btn_pressed(button_pin):
            pass                         # if not pressed just loop endlessly

        # if here then tactile button 1 has been pressed
        print (" button pressed")
        # set the maker kit RGB LED to blue and the AMBER LED ON to indicate it is sending
        GPIO.output(RX_red_pin, False) 
        GPIO.output(RX_green_pin, False)
        GPIO.output(RX_blue_pin, True)
        GPIO.output(TX_red_pin, False)
        GPIO.output(TX_amber_pin, True)
        GPIO.output(TX_green_pin, False)

        if socketstate == "off":
            transmit_raw_code(skttest01_house_on)
            print (" socket switched on")
            socketstate = "on"
            # set the maker kit RGB LED to green to indicate the remote socket is on
            GPIO.output(RX_red_pin, False)
            GPIO.output(RX_green_pin, True)
            GPIO.output(RX_blue_pin, False)
            # set the maker kit GREEN LED to ON to indicate the remote socket is on
            GPIO.output(TX_red_pin, False)
            GPIO.output(TX_amber_pin, False)
            GPIO.output(TX_green_pin, True)
            print ("socket on signal sent")

        elif socketstate == "on":
            transmit_raw_code(skttest01_house_off)
            print (" socket switched off")
            socketstate = "off"
            # set the maker kit RGB LED to red to indicate the remote socket is off
            GPIO.output(RX_red_pin, True)
            GPIO.output(RX_green_pin, False)
            GPIO.output(RX_blue_pin, False)
            # set the maker kit RED LED to ON to indicate the remote socket is off
            GPIO.output(TX_red_pin, True)
            GPIO.output(TX_amber_pin, False)
            GPIO.output(TX_green_pin, False)
            print ("socket off signal sent")       

        else:        
            print ("some error has occured - socket state unrecognised")

# Clean up the GPIOs for next time
except KeyboardInterrupt:
    print ("keyboard interrupt: switching everything off")
    transmit_raw_code(skttest01_house_off)

    GPIO.output(RX_red_pin, False)
    GPIO.output(RX_green_pin, False)
    GPIO.output(RX_blue_pin, False)
    GPIO.output(TX_red_pin, False)
    GPIO.output(TX_amber_pin, False)
    GPIO.output(TX_green_pin, False)

    GPIO.cleanup()

