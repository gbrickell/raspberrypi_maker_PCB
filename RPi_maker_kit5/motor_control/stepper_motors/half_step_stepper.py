#!/usr/bin/python

# RPi kits PCB version of half_step_stepper_detailed.py 
#  - using a 28BYJ-48 stepper motor control connected to a ULN2003 control board and the RPi_kits_PCB
#  - and a half step drive step sequence that energises either one or two coils at one time which has 
#     the effect of creating a different single step that is half the amount ie a 'half step'
#  - it simply rotates the stepper motor one full revolution with parameters that can be set to:
#    - change direction (StepDir)
#    - a wait time between steps so that the control board can keep up with the Pi's instructions (WaitTime)
# WaitTime in ms can also be changed by a command input parameter

# command: python3 /home/pi/RPi_maker_kit5/motor_control/stepper_motors/half_step_stepper.py

# Import required libraries
import sys
import time
import RPi.GPIO as GPIO

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
# for GPIO pins 8, 11, 9, & 10 connected to the drive coils using 
# the blue & yellow (coil 1) plus pink & orange (coil 2) wires
# the red wire is the common centre tap for both drive coils
# as shown in manufacturers datasheet

# Full step sequence: sets two phases at a time producing a 0.1758 degree step angle and 2048 steps per revolution
#  and twice the torque as two coils are energised at the same time

# the Seq array is used to define the sequence of pin HIGH/LOW settings
#  as each 'energisation' of either one or two coils produces a single step the 8 rows of the Seq array below generates 8 separate steps from the 8 sequences
Seq = [[1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1],
       [1,0,0,1]]
       
StepSeqCount = int(len(Seq)/2)  # StepSeqCount is the number of steps produced when the Seq array is process once: 4 for the half step drive sequence
print ("number of steps per Seq cycle: " + str(StepSeqCount) )
# should only ever need 8 sequences for all the drive options

StepDir = 1  # Set to 1 for clockwise
             # Set to -1 for anti-clockwise

# Read wait time from command line
if len(sys.argv)>1:
    WaitTime = float(sys.argv[1])/float(1000)
else:
    WaitTime = 2.5/float(1000)     # default wait time of 2.5ms that seems to work OK
print ("wait time (ms): " + str(WaitTime) )


# Initialise variables
StepCounter = 0    # array ref for Seq i.e. a counter for which sequence is being 'set'
if StepDir == -1:
    StepCounter = 7    # if direction is anti-clock then start from the end of the Seq array and move backwards thru it

# Start main loop
stepseqcyclecount = 0  # this is the number of full 8 sequence cycles completed
tstart = time.time()   # start the clock by recording the current time

try:    # this loop is not strictly necessary but it does allow the script to be easily stopped with CTRL-C
    while True:
      # this  loop does repeated 'cycles' through the Seq array by setting/resetting the StepCounter and accumulating the stepseqcyclecount

      #print (" step counter: " + str(StepCounter))
      #print (Seq[StepCounter])

      # for each Seq 'row' determined by the StepCounter loop through the array row i.e. each pin setting
      for pin in range(0, 4):   # loop through the GPIO pins setting them to HIGH or LOW according to the Seq[[]] value
        xpin = StepPins[pin]
        if Seq[StepCounter][pin]!=0:      # if not 0 then assume 1 so set HIGH (True)
          #print (" Enable GPIO %i" %(xpin))
          GPIO.output(xpin, True)
        else:
          GPIO.output(xpin, False)        # if = 0 then set LOW (False)

      StepCounter += StepDir    #update the Seq StepCounter in either the forward or backward direction
      if StepCounter == -1:     # this means the last item was 0 and we are going backwards
        StepCounter = 7         # so this is necessary if we are going backwards

      # If we reach the end of the sequence start again
      if (StepDir == 1 and StepCounter > 7) or (StepDir == -1 and StepCounter < 0):
        StepCounter = 0    
        stepseqcyclecount = stepseqcyclecount + 1   # increase the count of the number of 8 sequences ie cycles thru the Seq array
        #print (" 8 seq cycle count = " + str(stepseqcyclecount))
        if stepseqcyclecount >= 2048/StepSeqCount:  # the stepper uses 2048 individual full steps for a full rev so check if a full rev has been done
            tfinish = time.time()  # stop the clock by recording the difference between the current and the start times
            if StepDir == 1:
                print (" half step drive step sequence - forward rotation: this should be 1 full shaft revolution")
            else:
                print (" half step drive step sequence - backward rotation: this should be 1 full shaft revolution")
            print (" time taken for 1 revolution: " + str(tfinish-tstart) + " seconds")
            break

      # Wait before moving on - a wait time is needed as the control board may not be able to keep up
      time.sleep(WaitTime)


finally:  # this code is run when the try is interrupted with a CTRL-C
    print(" ")
    print("Cleaning up the GPIO pins before stopping")
    print(" ")
    print(" ")
    print(" ")
    GPIO.cleanup()
    
# The cleanup command sets all the pins back to inputs which protects the
# Pi from accidental shorts-circuits if something metal touches the GPIO pin