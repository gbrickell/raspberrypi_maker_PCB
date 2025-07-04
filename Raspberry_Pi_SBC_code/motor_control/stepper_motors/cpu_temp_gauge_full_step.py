#!/usr/bin/python
#
# RPi kits PCB version of  cpu_temp_gauge_full_step.py
#  - using a 28BYJ-48 stepper motor control using a ULN2003 control board and a full step sequence
#     to rotate a gauge 'hand' to indicate CPU temperature
#  - change direction (StepDir)
#  - a wait time between steps so that the control board can keep up with the Pi's instructions (WaitTime)
# 

# command: python3 ./RPi_maker_PCB5/motor_control/stepper_motors/cpu_temp_gauge_full_step.py


#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# function to return the CPU temperature
#
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# Return CPU temperature as a character string                                     
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# function to set the GPIO pins in an individual Seq row
#
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
def setGPIOrow(row):
    for pin in range(0, 4):   # loop through the GPIO pins setting them to HIGH or LOW according to the Seq{} value
      xpin = StepPins[pin]
      if Seq[row][pin]!=0:      # if not 0 then assume 1 so set HIGH (True)
        #print (" Enable GPIO %i" %(xpin))
        GPIO.output(xpin, True)
      else:
        GPIO.output(xpin, False)        # if = 0 then set LOW (False)
    # Wait before returning - a wait time is needed as the control board may not be able to keep up
    time.sleep(WaitTime)

    return()

#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# function to move n sequences in either direction where 1 sequence is 4 steps
#
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
def stepmotor(direction, sequences, position):
    # direction is either -1 for backwards or +1 for forwards
    # position is measured in steps between 0 and 2000
    #print ("direction, sequences, position: " + str(direction) + " - " + str(sequences) + " - " + str(position) )

    # check we are not going off scale
    if direction == 1 and (position + 4*sequences) > 2000 :
        sequences = (2000 - position)/4    # decrease the number of sequnces to just reach end of scale
        offscale = "plus"                  # set the offscale parameter to indicate 'off to the plus'
        position = 2000                    # set the new current position after the movement below
        #print ("off scale plus")

    elif direction == -1 and (position - 4*sequences) < 0 :
        sequences = position/4            # decrease the number of sequences to just reach end of scale
        offscale = "minus"                # set the offscale parameter to indicate 'off to the minus'
        position = 0                      # set the new current position after the movement below
        #print ("off scale minus")

    else:
        offscale = "ok"                   # set the offscale parameter to indicate all ok
        position = position + 4*direction*sequences
        #print ("scale ok")

    tstart = time.time()   # start the clock by recording the current time
    for seqloop in range (0, int(sequences)):
        #print ("sequence loop count: " +str(seqloop))

        # do one sequence of four steps
        # set the GPIO pins HIGH/LOW according to the pin sequence in Seq and 
        #  either go through the array forwards or backwards
        if direction == -1:
            for row in range(3, -1, -1):
                #print ("pin row: " + str(row))
                setGPIOrow(row)
        elif direction == 1:
            for row in range(0, 4, 1):
                #print ("pin row: " + str(row))
                setGPIOrow(row)

    #print ("number of sequences completed: " + str(seqloop+1))

    return (position, offscale)


#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# main code
#
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# Import required libraries
import sys
import os
import time
import RPi.GPIO as GPIO

CPU_temp = getCPUtemperature()
print( "CPU temperature  : " + str(CPU_temp))

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO signals to use                                                                                                                         
# BCM numbering: GPIO8,GPIO11,GPIO9,GPIO10 connected to IN1, IN2, IN3 and IN4 on the ULN2003 control board
StepPins = [8,11,9,10]    # set all the GPIO pins into an array

# Set all pins as output
for pin in StepPins:
  #print ("Setup pins")
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)

# Define the phase sequence for the unipolar stepper motor i.e.
# for GPIO pins 6, 13, 19, & 26 connected to the drive coils using 
# the blue & yellow (coil 1) plus pink & orange (coil 2) wires
# the red wire is the common centre tap for both drive coils
# as shown in manufacturers datasheet

# Full step sequence: sets two phases at a time producing a 0.18 degree step angle 
#  and twice the torque as two coils are energised at the same time
#  the Seq array is for 4 steps at a time2

Seq = [[1,1,0,0],
       [0,1,1,0],
       [0,0,1,1],
       [1,0,0,1]]

WaitTime = 3.0/float(1000)     # default wait time that seems to work OK

currentposition = 0
errorscale = "ok"
lasttemp = 45.0

# Start main loop

try:    # this loop is not strictly necessary but it does allow the script to be easily stopped with CTRL-C
    while True:

        nexttemp = float(getCPUtemperature())
        print( "CPU temperature  : " + str(nexttemp))

        tempdelta = nexttemp - lasttemp
        lasttemp = nexttemp
        #print( "temp change: " + str(tempdelta))

        noseqs = int(abs(tempdelta)/0.02)
        if tempdelta < 0 :
            setdirection = -1
        else:
            setdirection = 1

        if noseqs > 0:
            currentposition, errorscale = stepmotor(setdirection, noseqs, currentposition)
        time.sleep(0.2) # wait a short interval just so that it is not too fast !

finally:  # this code is run when the try is interrupted with a CTRL-C
    # move the gauge back to position zero ready for next time
    currentposition, errorscale = stepmotor(-1, 500, currentposition)
    time.sleep(2)
    currentposition, errorscale = stepmotor(-1, 500, currentposition)  # do it twice just in case
    print(" ")
    print("Cleaning up the GPIO pins and returning the gauge to zero before stopping")
    print(" ")
    print(" ")
    print(" ")
    GPIO.cleanup()
    
# The cleanup command sets all the pins back to inputs which protects the
# Pi from accidental shorts-circuits if something metal touches the GPIO pin