#!/usr/bin/python

# RPi PCB version of servo_stepper_control_app_nosudo.py
# Servo & Stepper Motor PCB Flask controller: python code as part of a Flask based web server system
# 
# this version of the Flask app does NOT need to be run using sudo as it uses 
#  the 'development' Flask server - see the code at the very end of the listing
# command to run: 
#        python3 ./RPi_maker_PCB5/motor_control/web_motor_controller/web_motor_control_app_nosudo.py
# 
# provides browser access for the servo control of two semaphore 'flags' using a PCA9685 I2C controller
#  and a stepper motor that drives the needle of a gauge indicating the CPU temeperature
# the two servos are connected to channels 0 (left servo) and 15 (right servo) and are moved to a set of positions 
#  depending upon a text message that is input using a HTML template

#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# function to return the CPU temperature for the stepper gauge
#
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# Return CPU temperature as a character string                                     
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# function to set the GPIO pins in an individual Seq row - used for the stepper gauge
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
    # 'direction' is either -1 for backwards or +1 for forwards
    # 'sequences' is the number of four-step sequences to move
    # 'position' is the current stepper motor position measured in steps between 0 and 2000

    #print ("direction, sequences, position: " + str(direction) + " - " + str(sequences) + " - " + str(position) )

    # check we are not going off scale
    if direction == 1 and (position + 4*sequences) > 2000 :
        sequences = (2000 - position)/4    # decrease the number of sequences to just reach end of scale
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

    tstart = time.time()   # start the clock by recording the current time - not actually using this at the moment
    for seqloop in range (0, int(sequences)):
        #print ("sequence loop count: " +str(seqloop))

        # do one sequence of four steps
        # set the GPIO pins HIGH/LOW according to the pin sequence in Seq and 
        #  either go through the array forwards or backwards
        if direction == -1:
            for row in range(3, -1, -1):     # this does rows 3, 2, 1, 0
                #print ("pin row: " + str(row))
                setGPIOrow(row)
        elif direction == 1:
            for row in range(0, 4, 1):       # this does rows 0, 1, 2, 3
                #print ("pin row: " + str(row))
                setGPIOrow(row)

    #print ("number of sequences completed: " + str(seqloop+1))

    return (position, offscale)




#########################################################
## function to send a semaphore message with the servos
#########################################################

def send_semaphore(message_string):

    message_string = message_string.upper()   # convert message to uppercase
    print ("text message in UPPER case is: " + message_string)
    message_array = list(message_string)      # put the characters of the string into an array
    #print ("message as an array is: " + str(message_array))

    # loop through the individual letters in the 'message' string
    for i in range (0, len(message_string)):
        #print i
        #print message_array[i]
        print ("Working on the letter: " + str(i) + " - " + str(message_array[i]))
        # find the chr in the reference letters array to get the two servo angles for that letter
        for irow, row in enumerate(letters):  # loop through the rows and columns of the reference letters array
            #print ("looking at letters row: " + str(irow))
            #print ("looking at letters column 0: " + str(letters[irow][0]) )
            if letters[irow][0] == message_array[i]:   # we have found the row - the column should always be 0
                #print ("letters row is: " + str(irow))
                print ("left and right servo angles are: " + str(letters[irow][1]) + " and " + str(letters[irow][2]))
                # set the servo positions with the 'found' servo angles
                set_servo('left', letters[irow][1])
                set_servo('right', letters[irow][2])
                time.sleep (3)    # wait a short interval between each letter being 'flagged'
                break
            if irow > 19:    # if we reach the end of the rows in the reference array then the letter is not found
                print ("message letter " + str(i) + " not found")

    print ("message ends")
    # set servos to zero position
    set_servo('left', 0)
    set_servo('right', 0)

    return ()

#################################################################
## function to set the servo position for the semaphore demo
#################################################################
def set_servo(side, angle):
    # 'side' is either left or right to indicate which servo to set
    # 'angle' is the angle 'found' from the reference letters array for the letter to be sent
    # the angle is either 0, 45, 90, 135, or 180 which is then translated into a PWM pulse value
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

    # the line below uses the I2C servo control board (PCA9685) library to move the servo
    pwm.set_pwm(channel, 0, servo_pulse)
    return ()


#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# main code 
#
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

#import sys
import os                 # this imports the module to allow various system functions too be used
import time               # this imports the module to allow various time functions to be used
import RPi.GPIO as GPIO   # this imports the module to allow the GPIO pins to be easily utilised

import Adafruit_PCA9685   # this imports a library that interfaces with the I2C servo control board (PCA9685)
                          #   and provides a set of PWM (pulse width modulation) functions the board can supply

# import the various Flask libraries that are needed
from flask import Flask, render_template
from flask import request

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO signals to use                                                                                                                         
# BCM numbering: GPIO19,GPIO20,GPIO21,GPIO16 connected to IN1, IN2, IN3 and IN4 on the ULN2003 control board
StepPins = [19,20,21,16]    # set all the GPIO pins into an array

# Set all the stepper control GPIO pins as output and as LOW
for pin in StepPins:
  #print ("Setup pins")
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)

# Define the phase sequence for the unipolar stepper motor i.e.
# for GPIO pins 6, 13, 16, & 20 connected to the drive coils using  
# the blue & yellow (coil 1) plus pink & orange (coil 2) wires
# the red wire is the common centre tap for both drive coils

# Full step sequence: sets two phases at a time producing a 0.1758 degree step angle 
#  and twice the torque as two coils are energised at the same time
#  the Seq array is for 4 steps at a time

Seq = [[1,0,0,1],
       [1,1,0,0],
       [0,1,1,0],
       [0,0,1,1]]

WaitTime = 3.0/float(1000)     # default wait time works OK
# other stepper gauge initial parameter values
currentposition = 0
errorscale = "ok"
lasttemp = 45.0

# Initialise the servo control board assuming it has its 
#  default address of hex 40 (0x40) and is the only device on the bus
#  this can be checked by running "sudo i2cdetect -y 1"
#  for all recent RPi models the port# is 1 in the above 'detect' command - but for pre-Oct'12 models it is 0
pwm = Adafruit_PCA9685.PCA9685()

# If for some reason the I2C device set up is not the default then use the following:
#    pwm = Adafruit_PCA9685.PCA9685(address=0x??, busnum=?)

pwm.set_pwm_freq(50)   # set the PWM frequency to 50Hz - as recommended for servos

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

# reference signal arrays i.e. letters and special signals

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

# the specials array is not currently used but is included for possible future use
specials = [['space',0,0],         # also included above
            ['error_up',135,135],
            ['error_down',45,45],
            ['cancel',135,45]]

semaphore_message = "default"

servo_stepper_app01 = Flask(__name__)  # creates a Flask object called servo_stepper_app01

##################################################################################################
# this route goes to the main select mode routine when the URL root is selected
# to select either the servo semaphore activity, the stepper motor 'gauge' activity, or to reboot
##################################################################################################
@servo_stepper_app01.route("/") # run the code below this function when the URL root is accessed
def start():
    select_mode = "selection routine",
    template_data = {
        'title' : "home page",
    }

    return render_template('select_motor_mode_nosudo.html', **template_data)


#########################################################################################################
# this route defines the actions selected when the servo & stepper motor system is in the selection mode
#########################################################################################################
@servo_stepper_app01.route("/<choice_mode>")  # run the code below this function when URL /<choice_mode> is accessed from select_motor_mode_nosudo.html where choice_mode is a variable
def motor_selection(choice_mode=None):
    none_selected = "no motor selected"

    # update time now       
    timenow = time.strftime('%H:%M %Z')
    print ("time updated in choice_mode route")    

    if choice_mode == 'servo_semaphore':   # run this section of code if 'servo_semaphore' is selected at the template

        # template data: individual parameters that are passed for use in the template to render the browser display
        template_data = {
            'title' : "servo semaphore system selected", # this sets the browser title template parameter
            'time_now' : timenow,                        # this sets the current time template parameter
            'sem_message' : semaphore_message,           # this sets the current semaphore message
        }

        # echo the current values of the servo system to the screen
        print ("semaphore message: " + semaphore_message)

        return render_template('semaphore_message.html', **template_data)   # run the 'semaphore_message.html' template


    elif choice_mode == 'stepper_gauge':   # run this section of code if 'stepper_gauge' is selected at the template

        # template data: individual parameters that are passed for use in the template to render the browser display
        template_data = {
            'title' : "stepper gauge system selected", # this sets the browser title template parameter
            'time_now' : timenow,                      # this sets the current time template parameter
        }

        # echo the values of the stepper gauge system to the screen
        # nothing for now

        return render_template('stepper_gauge_setup.html', **template_data) # run the 'stepper_gauge_setup.html' template


    elif choice_mode == 'reboot':
        os.system("sudo reboot")    # this does an immediate reboot of the system


    else:  # shouldn't ever arrive here but run this section of code if  neither 'servo_semaphore' nor 'stepper_gauge' nor 'reboot' are selected at the template
        template_data = {
            'title' : "no choice made",
        }
        return render_template('select_motor_mode_nosudo.html', **template_data)




##################################################################################################################
# this route defines the actions selected when the servo semaphore activity is 'on' and in 'message input' mode
##################################################################################################################
@servo_stepper_app01.route("/servo_semaphore/<semaphore_command>")  # run the code below this function when URL /servo_semaphore/<semaphore_command> is accessed where <semaphore_command> is a variable
def semaphore_active(semaphore_command=None):
    no_command = "no command given"

    # update time now
    timenow = time.strftime('%H:%M %Z')
    print ("time updated in servo_semaphore route")

    if semaphore_command == 'send_updated_message':
        # execute this set of code to send a revised semaphore message

        print ("send updated message path selected")
        print ("request method: " + str(request.method))
        print ("new message text: " + str(request.args.get('message')))
        semaphore_message = str(request.args.get('message'))

        # now 'signal' the revised semaphore message
        print ("start of new semaphore message")

        send_semaphore(semaphore_message)

        print ("end of new semaphore message")
        # end of semaphore sending - return to the message input screen

        # template data: individual parameters that are passed for use in the template to render the browser display
        template_data = {
            'title' : "send new message selected", # this sets the browser title template parameter
            'time_now' : timenow,                  # this sets the current time template parameter
            'sem_message' : semaphore_message,     # this sets the revised semaphore message

        }

        return render_template('semaphore_message.html', **template_data)    # run the 'semaphore_message.html' template

    elif semaphore_command == 'send_same_message':
        # execute this set of code to do a repeat send of the unchanged semaphore message

        print ("send existing message path selected")
        print ("request method: " + str(request.method))
        print ("message text: " + str(request.args.get('message')))
        semaphore_message = str(request.args.get('message'))

        print ("existing message text: " + semaphore_message)

        # now 'signal' the same repeated semaphore message
        print ("start of repeat send of semaphore message")

        send_semaphore(semaphore_message)

        print ("end of repeat send of semaphore message")
        # end of semaphore sending - return to the message input screen

        # template data: individual parameters that are passed for use in the template to render the browser display
        template_data = {
            'title' : "send new message selected", # this sets the browser title template parameter
            'time_now' : timenow,                  # this sets the current time template parameter
            'sem_message' : semaphore_message,     # this sets the revised semaphore message

        }

        return render_template('semaphore_message.html', **template_data)    # run the 'semaphore_message.html' template


    elif semaphore_command == 'select':

        print ("select motor option path selected")
        template_data = {
            'title' : "none selected",
        }
        print (" going back to select .....")

        return render_template('select_motor_mode_nosudo.html', **template_data)

    else:    # should not ever get here but added just in case

        print ("unknown selection path?")
        template_data = {
            'title' : "none selected",
        }
        print (" going back to select .....")

        return render_template('select_motor_mode_nosudo.html', **template_data)



##################################################################################################################
# this route defines the actions selected when the stepper gauge activity is 'on' 
##################################################################################################################
@servo_stepper_app01.route("/stepper_gauge/<stepper_command>")  # run the code below this function when URL /stepper_gauge/<stepper_command> is accessed where <stepper_command> is a variable
def stepper_active(stepper_command=None):
    no_command = "no command given"

    # update time now
    timenow = time.strftime('%H:%M %Z')
    print ("time updated in stepper_gauge route")

    if stepper_command == 'start_gauge':
        # execute this set of code to start the stepper CPU temperature gauge

        # assume gauge is set to 'zero' position ie at 45 degC and set initial parameters
        currentposition = 0
        errorscale = "ok"
        lasttemp = 45.0

        print ("starting CPU temperature gauge - Raspberry Pi must be rebooted to stop this if a CTRL cannot be done")

        try:    # this loop is not strictly necessary but it might allow the script to be stopped with CTRL-C
            while True:

                nexttemp = float(getCPUtemperature())         # get the CPU temperature as a float variable
                print( "CPU temperature  : " + str(nexttemp))

                tempdelta = nexttemp - lasttemp               # calculate the temeperature change since the last cycle
                lasttemp = nexttemp
                #print( "temp change: " + str(tempdelta))

                noseqs = int(abs(tempdelta)/0.02)             # convert the temeperature change into 4-step sequences
                # set the direction depnding upon whether the temeperature change is up or down
                if tempdelta < 0 :
                    setdirection = -1
                else:
                    setdirection = 1

                if noseqs > 0:     # only do a gauge movement if there has been a tempeerture change
                    currentposition, errorscale = stepmotor(setdirection, noseqs, currentposition)
                time.sleep(0.2)    # wait a short interval just so that it is not too fast !

        finally:  # this code is run when the try is interrupted with a CTRL-C which is not always possible
            # move the gauge back to position zero ready for next time
            currentposition, errorscale = stepmotor(-1, 500, currentposition)
            currentposition, errorscale = stepmotor(-1, 500, currentposition)  # do it twice just in case
            print(" ")
            #print("Cleaning up the GPIO pins and returning the gauge to zero before stopping")
            #print(" ")
            #print(" ")
            #print(" ")
            #GPIO.cleanup()

        # template data: individual parameters that are passed for use in the template to render the browser display
        template_data = {
            'title' : "stepper gauge system selected", # this sets the browser title template parameter
            'time_now' : timenow,                      # this sets the current time template parameter
            'move_amount' : "",                        # return the movement amount as blank

        }

        return render_template('stepper_gauge_setup.html', **template_data)    # run the 'stepper_gauge_setup.html' template

    elif stepper_command == 'interval_move':

        print ("interval move path selected")
        print ("request method: " + str(request.method))
        moveamount = str(request.args.get('moveamt'))  # this gets the requested amount from the template input
        print ("number of sequences to move: " + moveamount)
        if len(moveamount) == 0:
            noseqs = 0
        else:
            noseqs = int(moveamount)     
        print ("noseqs: " + str(noseqs))
        if noseqs < 0 :    # if the movement requested as an integer is negative set the direction
            direction = -1
            noseqs = abs(noseqs)  # now set the movement as an absolute integer
        else:
            direction = 1  # and noseqs does not need to change

        print ("direction and number of sequences: " + str(direction) + " - " + str(noseqs))

        errorscale = "ok"

        # move the gauge 'needle' the input number of sequences
        currentposition, errorscale = stepmotor(direction, noseqs, 1000) # set current position mid scale so it can move either way
        print ("error scale: " + str(errorscale))

        # template data: individual parameters that are passed for use in the template to render the browser display
        template_data = {
            'title' : "stepper gauge system selected", # this sets the browser title template parameter
            'time_now' : timenow,                      # this sets the current time template parameter
            'move_amount' : "",                        # return the movement amount as blank

        }

        return render_template('stepper_gauge_setup.html', **template_data)    # run the 'stepper_gauge_setup.html' template

    elif stepper_command == 'calibrate_gauge':
        # execute this set of code to do end of scale calibration checks

        errorscale = "ok"

        # start of gauge end of scale tests
        # assume we are starting at position 0
     
        # send gauge 'needle' to end of gauge - 55 degC ie 500 sequences(2000 steps) forwards from position 0
        currentposition, errorscale = stepmotor(1, 500, 0)
        time.sleep(5)  # wait a few second so that the position can be visually checked
        # send gauge 'needle' to beginning of gauge - 45 degC ie 500 sequences(2000 steps) backwards from position 2000
        currentposition, errorscale = stepmotor(-1, 500, 2000)
        time.sleep(5)  # wait a few second so that the position can be visually checked

        # end of gauge end of  scale tests

        # template data: individual parameters that are passed for use in the template to render the browser display
        template_data = {
            'title' : "stepper gauge system selected", # this sets the browser title template parameter
            'time_now' : timenow,                      # this sets the current time template parameter
            'move_amount' : "",                        # return the movement amount as blank

        }

        return render_template('stepper_gauge_setup.html', **template_data)    # run the 'stepper_gauge_setup.html' template


    elif stepper_command == 'select':

        print ("select motor option path selected")
        template_data = {
            'title' : "none selected",
        }
        print (" going back to select .....")

        return render_template('select_motor_mode_nosudo.html', **template_data)


    else:    # should not ever get here but added just in case

        print ("unknown selection path?")
        template_data = {
            'title' : "none selected",
        }
        print (" going back to select .....")

        return render_template('select_motor_mode_nosudo.html', **template_data)


#####################################################
# the code below is the last code in the system
#####################################################

if __name__ == "__main__":
    # using the 'development' flask server WITHOUT sudo so need to use a port other than 80
    servo_stepper_app01.run(host='0.0.0.0', port=8080, debug=False, threaded=True)   # 0.0.0.0 means any device on the network can access the web app
    #servo_stepper_app01.run(host='0.0.0.0', port=8080, debug=True)   # option to run without 'threaded' set to True and debug 'on'




