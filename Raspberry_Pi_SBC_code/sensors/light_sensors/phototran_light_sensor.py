# RPi kits PCB version of phototran_light_sensor.py that times how long it takes to recharge a capacitor when a button is pressed
#   where this provides a 'proxy' measurement of the phototransistor 'resistance' and hence the light level

# command to run this script:  python3 ./RPi_maker_kit5/sensors/light_sensors/phototran_light_sensor.py

import RPi.GPIO as GPIO   # this imports the module to allow the GPIO pins to be easily utilised
import time               # this imports the module to allow various time functions to be used
GPIO.setwarnings(False)

# This code sets the RPi to use the BCM (Broadcom) pin numbers which is usually the default but is positively set here
GPIO.setmode(GPIO.BCM)


pin_charge = 5     # GPIO pin_charge connected to the phototransistor collector when set HIGH charges the capacitor through a fixed 1k resistor

pin_discharge = 6  # GPIO pin_discharge  discharges the capacitor through a fixed 1k resistor

button_pin = 26    # this is the GPIO pin that one side of the (bottom: button2) tactile switch is connected to

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
# this is a special setting that indicates when a pin changes from LOW to HIGH ie when the button is pressed

# this function discharges (empties) the 330nF capacitor so it is ready to be recharged (filled up)
def discharge():
    GPIO.setup(pin_charge, GPIO.IN)
    GPIO.setup(pin_discharge, GPIO.OUT)
    GPIO.output(pin_discharge, False)
    time.sleep(0.2)  # this wait time is set to a value large enough for the capacitor to fully discharge
    #print ("capacitor discharged")    # show this debug by deleting the # in front of the print

# this function charges (fills up) the the 330nF capacitor and returns the time taken for the GPIO pin_charge 
# to go HIGH this means the voltage on the capacitor has reached approx. 1.65V
def charge_time():
    GPIO.setup(pin_discharge, GPIO.IN)    # configure the GPIO pin_discharge to be an input
    GPIO.setup(pin_charge, GPIO.OUT)      # configure the GPIO pin_charge to be an output
    GPIO.output(pin_charge, True)         # set the GPIO pin_charge HIGH so that it starts to charge the capacitor
    t1 = time.time()                      # start the clock by recording the current time
    while not GPIO.input(pin_discharge):  # loop while the GPIO pin_discharge is still not HIGH ie capacitor not charged
        pass
    t2 = time.time()             # stop the clock by recording the difference between the current and the start times
    #  if here then the GPIO pin_discharge is HIGH ie the capacitor has charged so we can return the time in milliseconds
    millitime = (t2 - t1) * 1000
    #print ("capacitor recharged - time (ms): " + str(millitime)) # show this debug by deleting the # in front of the print
    return millitime      # times were in seconds so multiply by 1000 to get milliseconds


# this is a function to repetitively discharge and recharge the 330nF capacitor that is in series
# with the phototransistor and obtain an average time in milliseconds for the recharging
#  - the longer this time, the higher the phototransistor 'resistance' and the lower the light level
#
def phototransistor_time(repeats):         # start the definition of the function
    total = 0;
    for i in range(1, repeats+1):
        #print ("loop counter: " + str(i))  # show this debug by deleting the # in front of the print
        discharge()
        total = total + charge_time()
        #print ("current total time (ms): " + str(total)) # show this debug by deleting the # in front of the print
    av_time = total / float(repeats)
    #print ("average recharge time (ms): " + str(av_time)) # show this debug by deleting the # in front of the print
    return av_time

# this is a function to indicate when the button is pressed 
def btn_pressed():
    # if button is pressed GPIO.input will report FALSE
    if not GPIO.input(button_pin):
        return 1

###########
# main code
###########

print (" ")
print ("program running: press button 2 (bottom) to take a light reading or CTRL-C to stop ")

try:    # this loop is not strictly necessary but it does allow the script to be easily stopped with CTRL-C
    while True:  # this is the loop that checks if the button is pressed and measures the phototransistor recharge time if it is
        discharge()                      # capacitor discharged just in case        

        while not btn_pressed():         # check if button pressed
            pass                         # if not pressed just loop endlessly

        # if we are here then the button has been pressed
        print(" ")
        print ("button 2 pressed: light collection process started")
        print(" ")
        photo_time = phototransistor_time(5)          # calculate the average recharge time from 5 readings
        print ("average phototransistor recharge time (ms): " + str(photo_time))
        print(" ")
        # now loop back to wait for the button to be pressed again
        print ("press button 2 (bottom) again to take another light level reading or CTRL-C to stop ")

finally:  # this code is run when the try is interrupted with a CTRL-C
    print(" ")
    print("Cleaning up the GPIO pins before stopping")
    print(" ")
    print(" ")
    print(" ")
    GPIO.cleanup()
    
# The cleanup command sets all the pins back to inputs which protects the
# Pi from accidental shorts-circuits if something metal touches the GPIO pins.
    