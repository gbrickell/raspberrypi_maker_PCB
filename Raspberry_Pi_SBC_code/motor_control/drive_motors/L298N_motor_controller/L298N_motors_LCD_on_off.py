# L298N controlled motors - Simple on/off Motor Test Code ie not using PWM00000

# command to run:  python3 ./RPi_maker_kit5/motor_control/drive_motors/L298N_motor_controller/L298N_motors_LCD_on_off.py

#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# Raspberry Pi generic set of simple (non PWM) L298N motor functions 
# 
# pin settings to be adjusted depending upon how the motors are wired
#
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

def forward():
    print ("forward")
    # in1, in2, in3 and in4 to be adjusted so that both motors go fwd

    # set enA on, set in1 off and in2 on (right motor)
    GPIO.output(enA, 1)
    GPIO.output(in1, 0)
    GPIO.output(in2, 1)

    # set enB on, set in3 off and in4 on (left motor)
    GPIO.output(enB, 1)
    GPIO.output(in3, 0)
    GPIO.output(in4, 1)
 
def backward():
    print ("backward")
    # in1, in2, in3 and in4 to be adjusted so that both motors go back

    # set enA on, set in1 on and in2 off (right motor)
    GPIO.output(enA, 1)
    GPIO.output(in1, 1)
    GPIO.output(in2, 0)

    # set enB on, set in3 on and in4 off (left motor)
    GPIO.output(enB, 1)
    GPIO.output(in3, 1)
    GPIO.output(in4, 0)
 
def stop(mode):
    if mode == "brake":
        print ("brake stop")
        # motor braking
        # set enA on, set in1 off and in2 off
        GPIO.output(enA, 1)
        GPIO.output(in1, 0)
        GPIO.output(in2, 0)
        # set enB on, set in3 off and in4 off
        GPIO.output(enB, 1)
        GPIO.output(in3, 0)
        GPIO.output(in4, 0)

    elif mode == "coast":
        print ("coast stop")
        # coasting
        # set enA off, set in1 off and in2 off
        GPIO.output(enA, 0)
        GPIO.output(in1, 0)
        GPIO.output(in2, 0)
        # set enB off, set in3 off and in4 off
        GPIO.output(enB, 0)
        GPIO.output(in3, 0)
        GPIO.output(in4, 0)
 
def turnRight():   # left motor fwd & right motor off
    print ("turn Right")

    # set enA off, set in1 off and in2 off (right motor)
    GPIO.output(enA, 0)
    GPIO.output(in1, 0)
    GPIO.output(in2, 0)

    # set enB on, set in3 off and in4 on (left motor)
    GPIO.output(enB, 1)
    GPIO.output(in3, 0)
    GPIO.output(in4, 1)
 
def turnLeft():   # right motor fwd & left motor off
    print ("turn Left")

    # set enA on, set in1 off and in2 on (right motor)
    GPIO.output(enA, 1)
    GPIO.output(in1, 0)
    GPIO.output(in2, 1)

    # set enB off, set in3 off and in4 off (left motor)
    GPIO.output(enB, 0)
    GPIO.output(in3, 0)
    GPIO.output(in4, 0)
 
def spinRight():   # left motor fwd & right motor back
    print ("spin Right")

    # set enA on, set in1 on and in2 off (right motor)
    GPIO.output(enA, 1)
    GPIO.output(in1, 1)
    GPIO.output(in2, 0)

    # set enB on, set in3 off and in4 on (left motor)
    GPIO.output(enB, 1)
    GPIO.output(in3, 0)
    GPIO.output(in4, 1)
   
def spinLeft():   # left motor back & right motor fwd
    print ("spin Left")
 
   # set enA on, set in1 off and in2 on (right motor)
    GPIO.output(enA, 1)
    GPIO.output(in1, 0)
    GPIO.output(in2, 1)
 
   # set enB on, set in3 on and in4 off (left motor)
    GPIO.output(enB, 1)
    GPIO.output(in3, 1)
    GPIO.output(in4, 0)

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

# Turn all motors off
stop("coast")
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("both motors off", 2, 0)   # display at row 2 column 0

forward()
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("both motors fwd", 2, 0)   # display at row 2 column 0
time.sleep(3)
stop("brake")
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("both motors off", 2, 0)   # display at row 2 column 0
time.sleep(2)


backward()
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("both motors back", 2, 0)   # display at row 2 column 0
time.sleep(3)
stop("brake")
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("both motors off", 2, 0)   # display at row 2 column 0
time.sleep(2)

turnLeft()
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("turning left", 2, 0)   # display at row 2 column 0
time.sleep(3)
stop("brake")
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("both motors off", 2, 0)   # display at row 2 column 0
time.sleep(2)

turnRight()
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("turning right", 2, 0)   # display at row 2 column 0
time.sleep(3)
stop("brake")
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("both motors off", 2, 0)   # display at row 2 column 0
time.sleep(2)

spinLeft()
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("spinning left", 2, 0)   # display at row 2 column 0
time.sleep(3)
stop("brake")
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("both motors off", 2, 0)   # display at row 2 column 0
time.sleep(2)

spinRight()
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("spinning right", 2, 0)   # display at row 2 column 0
time.sleep(3)
stop("brake")
mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Driving motors:", 1, 0)   # display at row 1 column 0
mylcd.lcd_display_string("both motors off", 2, 0)   # display at row 2 column 0
time.sleep(2)

mylcd.lcd_clear()  # clear LCD screen
mylcd.lcd_display_string("Program ended", 1, 1)     # display at row 1 column 1
GPIO.cleanup()

time.sleep(2)
mylcd.lcd_clear()  # clear LCD screen
mylcd.backlight(0) # turn off LCD backlight



