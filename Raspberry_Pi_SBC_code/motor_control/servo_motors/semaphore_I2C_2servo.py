#!/usr/bin/python

# RPi kits PCB version of  semaphore_I2C_2servo.py - simple test program for the servo control of two semaphore 'flags' 
#  using a PCA9685 I2C controller to move servos on channels 0 (left servo) and 15 (right servo) 
#  to a set of positions depending upon a text message that is set in line 130
#
# a more extensive set of code is also available that lets a message be input with a browser interface
#
# command: python3 /home/pi/RPi_maker_PCB5/motor_control/servo_motors/semaphore_I2C_2servo.py
#
#
#

########################################
## function to set the servo position
########################################
def set_servo(side, angle):
    if side == "left":
        channel = 0
        if angle == 0:
            servo_pulse = left0
        elif angle == 45:
            servo_pulse = left45
        elif angle == 90:
            servo_pulse = left90
        elif angle == 135:
            servo_pulse = left135
        elif angle == 180:
            servo_pulse = left180
        else:
            print ("incorrect servo angle set for left side")
            return ()

    elif side == "right":
        channel = 15
        if angle == 0:
            servo_pulse = right0
        elif angle == 45:
            servo_pulse = right45
        elif angle == 90:
            servo_pulse = right90
        elif angle == 135:
            servo_pulse = right135
        elif angle == 180:
            servo_pulse = right180
        else:
            print ("incorrect servo angle set for right side")
            return ()

    else:
        print ("incorrect side value in the set_servo function")
        return ()

    pwm.set_pwm(channel, 0, servo_pulse)
    return ()

####################
# main code
####################

import time               # this imports the module to allow various time functions to be used
import RPi.GPIO as GPIO   # this imports the module to allow the GPIO pins to be easily utilised

import Adafruit_PCA9685   # this imports a library that interfaces with the I2C servo control board (PCA9685)
                          #   and provides a set of PWM (pulse width modulation) functions the board can supply

# This code sets the RPi to use the BCM (Broadcom) pin numbers which is usually the default but is positively set here
GPIO.setmode(GPIO.BCM)

# Initialise the servo control board assuming it has its 
#  default address hex 40 (0x40) and is the only device on the bus
#  this can be checked by running "sudo i2cdetect -y 1"
#  for all recent RPi models the port# is 1 in the above 'detect' command - but for pre-Oct'12 models it is 0
pwm = Adafruit_PCA9685.PCA9685()

# If for some reason the I2C device set up is not the default then use the following:
#    pwm = Adafruit_PCA9685.PCA9685(address=0x??, busnum=?)

pwm.set_pwm_freq(50)   # set the PWM frequency to 50Hz - as per the SG90 data sheet.

# set the 5 servo pulse lengths for the 0, 45, 90, 135 and 180 degree positions for both left and right servos
# each number may have to be fine tuned for the specific servo - see the support documentation for more details

left0 = 580 
left45 = 465
left90 = 350
left135 = 240
left180 = 130

right0 = 160 
right45 = 262
right90 = 365
right135 = 490
right180 = 615

# signal arrays i.e. letters and special signals

# NB some letters (H, I, O, W, X & Z) cannot be sent as they need rotations that are not (yet?) possible
letters = [['A',45,0],
           ['B',90,0],
           ['C',135,0],
           ['D',180,0],
           ['E',0,135],
           ['F',0,90],
           ['G',0,45],
           ['J',180,90],
           ['K',45,180],
           ['L',45,135],
           ['M',45,90],
           ['N',45,45],
           ['P',90,180],
           ['Q',90,135],
           ['R',90,90],
           ['S',90,45],
           ['T',135,180],
           ['U',135,135],
           ['V',180,45],
           ['Y',135,90],
           [' ',0,0]]

# test print S
#print (letters[15][0])

specials = [['space',0,0],
            ['error_up',135,135],
            ['error_down',45,45],
            ['cancel',135,45]]

# just for initial test use some simple text
message_string = "makerspace rules"
message_string = message_string.upper()
print ("text message in UPPER case is: " + message_string)
message_array = list(message_string)
#print ("message as an array is: " + str(message_array))

# loop through the individual letters in the 'message' string
for i in range (0, len(message_string)):
    #print i
    #print message_array[i]
    print ("Working on the letter: " + str(i) + " - " + str(message_array[i]))
    # find the chr in the letters array to get the two servo angles for that letter
    for irow, row in enumerate(letters): 
        #print ("looking at letters row: " + str(irow))
        #print ("looking at letters column 0: " + str(letters[irow][0]) )
        if letters[irow][0] == message_array[i]:   # we have found the row - the column should always be 0
            #print ("letters row is: " + str(irow))
            print ("left and right servo angles are: " + str(letters[irow][1]) + " and " + str(letters[irow][2]))
            # set the servo positions with the 'found' servo angles
            set_servo('left', letters[irow][1])
            set_servo('right', letters[irow][2])
            time.sleep (3)
            break
        if irow > 19:
            print ("message letter " + str(i) + " not found")


print ("message ends")
# set servos to zero position
set_servo('left', 0)
set_servo('right', 0)


