#!/usr/bin/python

# RPi PCBs PCB version of L298N_2motors_test01.py
# using a L298N to control the motors with PWM

# command to run:  python3 ./RPi_maker_PCB5/motor_control/drive_motors/L298N_motor_controller/L298N_motors_LCD_PWM.py


#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# Raspberry Pi L298N more developed PWM motor functions but based upon the article at 
#  http://www.instructables.com/id/Control-DC-and-stepper-motors-with-L298N-Dual-Moto/
#  which describes the L298N motor controller use with an Arduino Uno
# 
#  N.B. depending upon how the motors are connected the motor direction
#    signals to the in1, in2, in3 nd in4 pins may need to be reversed
#
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

def forward_pwm(dutycycleA, dutycycleB):   # A is right and B is left
    # separate duty cycles are set so that each motor can be fine tuned if they vary in performance
    # in1, in2, in3 and in4 to be adjusted so that both motors go fwd

    print ("forward " + str(dutycycleA) + " - " +str(dutycycleB))

    # set enA (right motor) with the PWM dutycycle
    pwm_enA.start(dutycycleA)
    # set in1 off and in2 on i.e. LOW - HIGH for forward motion
    GPIO.output(in1, 0)
    GPIO.output(in2, 1)

    # set enB (left motor) with the PWM dutycycle
    pwm_enB.start(dutycycleB)
    # set in3 off and in4 on -i.e. LOW - HIGH for forward motion
    GPIO.output(in3, 0)
    GPIO.output(in4, 1)
 
def backward_pwm(dutycycleA, dutycycleB):  # A is right and B is left
    # in1, in2, in3 and in4 to be adjusted so that both motors go back

    print ("backward " + str(dutycycleA) + " - " +str(dutycycleB))

    # set enA (right motor) with the PWM dutycycle
    pwm_enA.start(dutycycleA)
    # set in1 on and in2 off i.e. HIGH - LOW for backward motion
    GPIO.output(in1, 1)
    GPIO.output(in2, 0)

    # set enB (left motor) with the PWM dutycycle
    pwm_enB.start(dutycycleB)
    # set in3 on and in4 off i.e. HIGH - LOW for backward motion
    GPIO.output(in3, 1)
    GPIO.output(in4, 0)
 
def stop_pwm(mode):
    if mode == "brake":
        print ("brake stop")
        # motor braking
        # set enA with 100% PWM dutycycle
        pwm_enA.start(100)
        # set in1 off and in2 off i.e. LOW- LOW for no motion
        GPIO.output(in1, 0)
        GPIO.output(in2, 0)
        # set enB with 100% PWM dutycycle
        pwm_enB.start(100)
        # set in3 off and in4 off i.e. LOW- LOW for no motion
        GPIO.output(in3, 0)
        GPIO.output(in4, 0)

    elif mode == "coast":
        print ("coast stop")
        # coasting
        # set enA with 0% PWM dutycycle
        pwm_enA.start(0)
        # set in1 off and in2 off i.e. LOW- LOW for no motion
        GPIO.output(in1, 0)
        GPIO.output(in2, 0)
        # set enB with 0% PWM dutycycle
        pwm_enB.start(0)
        # set in3 off and in4 off i.e. LOW- LOW for no motion
        GPIO.output(in3, 0)
        GPIO.output(in4, 0)
 
def turnRight_pwm(turn_time, dutycycleB):   # left motor fwd & right motor off
    print ("turn Right " + str(turn_time) + " - " +str(dutycycleB))

    # set enA (right motor) with 0% PWM dutycycle
    pwm_enB.start(0)
    # set in1 off and in2 off i.e. LOW - LOW for no motion 
    GPIO.output(in1, 0)
    GPIO.output(in2, 0)

    # set enB (left motor) with the passed PWM dutycycle
    pwm_enB.start(dutycycleB)
    # set in3 off and in4 on -i.e. LOW - HIGH for forward motion
    GPIO.output(in3, 0)
    GPIO.output(in4, 1)

    time.sleep(turn_time) # only run the motors for the set amount of turn_time seconds
    stop_pwm("brake")     # stop the motors after the turn
 
def turnLeft_pwm(turn_time, dutycycleA):   # right motor (A) fwd & left motor (B) off
    print ("turn Left " + str(turn_time) + " - " +str(dutycycleA))

    # set enB (left motor) with 0% PWM dutycycle
    pwm_enB.start(0)
    # set in3 off and in4 off i.e. LOW - LOW for no motion
    GPIO.output(in3, 0)
    GPIO.output(in4, 0)

    # set enA (right motor) with the passed PWM dutycycle
    pwm_enA.start(dutycycleA)
    # set in1 off and in2 on i.e. LOW - HIGH for forward motion
    GPIO.output(in1, 0)
    GPIO.output(in2, 1)
 
    time.sleep(turn_time) # only run the motors for the set amount of turn_time seconds
    stop_pwm("brake")     # stop the motors after the turn
 
def spinRight_pwm(spin_time, dutycycleA, dutycycleB):   # left motor (B) fwd & right motor (A) back
    print ("spin Right " + str(spin_time) + " - " +str(dutycycleA) + " - " +str(dutycycleB))

    # set enA (right motor) with the passed PWM dutycycle
    pwm_enA.start(dutycycleA)
    # set in1 on and in2 off i.e. HIGH - LOW for backward motion
    GPIO.output(in1, 1)
    GPIO.output(in2, 0)

    # set enB (left motor) with the passed PWM dutycycle
    pwm_enB.start(dutycycleB)
    # set in3 off and in4 on -i.e. LOW - HIGH for forward motion
    GPIO.output(in3, 0)
    GPIO.output(in4, 1)

    time.sleep(spin_time) # only run the motors for the set amount of spin_time seconds
    stop_pwm("brake")     # stop the motors after the spin
   
def spinLeft_pwm(spin_time, dutycycleA, dutycycleB):   # left motor back & right motor fwd
    print ("spin Left " + str(spin_time) + " - " +str(dutycycleA) + " - " +str(dutycycleB))

    # set enA (right motor) with the passed PWM dutycycle
    pwm_enA.start(dutycycleA)
    # set in1 off and in2 on i.e. LOW - HIGH for forward motion
    GPIO.output(in1, 0)
    GPIO.output(in2, 1)

    # set enB (left motor) with the passed PWM dutycycle
    pwm_enB.start(dutycycleB)
    # set in3 on and in4 off i.e. HIGH - LOW for backward motion
    GPIO.output(in3, 1)
    GPIO.output(in4, 0)

    time.sleep(spin_time) # only run the motors for the set amount of spin_time seconds
    stop_pwm("brake")     # stop the motors after the spin


#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# main code
#
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

# import the LCD driver code, initalise the LCD and clear the screen
import I2C_LCD_driver
mylcd = I2C_LCD_driver.lcd()
mylcd.lcd_clear()  # clear LCD screen

import RPi.GPIO as GPIO # Import the GPIO Library
import time # Import the Time library

# Set the GPIO modes
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# L298N setup code
# Define Outputs from RPi to L298N - variable names are as per the L298N pin labels
# the IN1-IN4 pins 'borrow' the PCB stepper motor / SPI connections on the 7P female connector
# enA and enB use two of the spare GPIO pins
enA = 15   # this will be a software set PWM pin
in1 = 8
in2 = 11
enB = 18   # this will be a software set PWM pin
in3 = 9
in4 = 10

# Set the GPIO Pin mode
GPIO.setup(enA, GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(enB, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)

# set the various PWM parameters
# How many times to turn the GPIO pin on and off each second 
Frequency = 20      # usually 20
# How long the GPIO pin stays on each cycle, as a percent  
# Setting the duty cycle to 0 means the motors will not turn
DutyCycleA = 50     # usually 30 for a quite slow turn rate
DutyCycleB = 50     # usually 30 for a quite slow turn rate
Stop = 0

# turn and spin times i.e. the times the motors are 'on' to effect a turn or spin
TurnTime = 2      # usually 0.5 for an actual turn
SpinTime = 2      # usually 0.5 for an actual spin

pwm_enA = GPIO.PWM(enA, Frequency)  # set the enA pin as a software set PWM pin
pwm_enB = GPIO.PWM(enB, Frequency)  # set the enB pin as a software set PWM pin
# Start the software PWM pins with a duty cycle of 0 (i.e. motors not moving)
pwm_enA.start(0)
pwm_enB.start(0)


# Turn all motors off
stop_pwm("coast")
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("both motors off", 2, 0)   # display at row 2 column 0

forward_pwm(DutyCycleA, DutyCycleB)
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("both motors fwd", 2, 0)   # display at row 2 column 0
time.sleep(3)
stop_pwm("brake")
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("both motors off", 2, 0)   # display at row 2 column 0
time.sleep(2)

forward_pwm(75, 0)
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("motor A fwd 70%", 2, 0)   # display at row 2 column 0
time.sleep(3)
stop_pwm("brake")
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("both motors off", 2, 0)   # display at row 2 column 0
time.sleep(2)

forward_pwm(0, 75)
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("motor B fwd 70%", 2, 0)   # display at row 2 column 0
time.sleep(3)
stop_pwm("brake")
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("both motors off", 2, 0)   # display at row 2 column 0
time.sleep(2)

backward_pwm(DutyCycleA, DutyCycleB)
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("both motors back", 2, 0)   # display at row 2 column 0
time.sleep(3)
stop_pwm("brake")
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("both motors off", 2, 0)   # display at row 2 column 0
time.sleep(2)

backward_pwm(75, 0)
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("motor A back 70%", 2, 0)   # display at row 2 column 0
time.sleep(3)
stop_pwm("brake")
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("both motors off", 2, 0)   # display at row 2 column 0
time.sleep(2)

backward_pwm(0, 75)
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("motor B back 70%", 2, 0)   # display at row 2 column 0
time.sleep(3)
stop_pwm("brake")
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("both motors off", 2, 0)   # display at row 2 column 0
time.sleep(2)

mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("turning left", 2, 0)   # display at row 2 column 0
turnLeft_pwm(TurnTime, DutyCycleA)
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("both motors off", 2, 0)   # display at row 2 column 0
time.sleep(2)


mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("turning right", 2, 0)   # display at row 2 column 0
turnRight_pwm(TurnTime, DutyCycleB)
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("both motors off", 2, 0)   # display at row 2 column 0
time.sleep(2)


mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("spinning left", 2, 0)   # display at row 2 column 0
spinLeft_pwm(SpinTime, DutyCycleA, DutyCycleB)
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("both motors off", 2, 0)   # display at row 2 column 0
time.sleep(2)


mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("spinning right", 2, 0)   # display at row 2 column 0
spinRight_pwm(SpinTime, DutyCycleA, DutyCycleB)
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("both motors off", 2, 0)   # display at row 2 column 0
time.sleep(2)

mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Program ended", 1, 1)     # display at row 1 column 1

time.sleep(2)
mylcd.lcd_clear()  # clear LCD screen
mylcd.backlight(0) # turn off LCD backlight


