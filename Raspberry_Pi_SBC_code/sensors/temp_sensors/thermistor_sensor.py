# RPi kits PCB version of thermistor_sensor.py that shows an approximate temperature of the thermistor when a button is pressed
#  this is done by measuring the resistance of the thermistor using a so-called 'step response' method
#  and then the resistance is interpreted as a temperature according to the Steinhart-Hart equation

# command to run this script:  python3 ./RPi_maker_kit5/sensors/temp_sensors/thermistor_sensor.py

import RPi.GPIO as GPIO   # this imports the module to allow the GPIO pins to be easily utilised
import time, math         # this imports the time and math modules to allow various time & math functions to be used
GPIO.setwarnings(False)

GPIO_high = 1.25  
# this is the most inaccurate 'guessed value' - but it can be adjusted 
# to arrive at the measured thermistor resistance if known

C = 0.324   # this is the value of the capacitor in uF i.e. 330nF - adjust this value to accurate value if known
R1 = 969    # this is the value of the fixed resistors i.e. 1kohms - adjust this value to accurate value if known

# ref http://assets.newport.com/webDocuments-EN/images/TNSTEIN-1_Thermistor_Conversions_IX.PDF
B = 3950.0   # this is the B constant for use in the simple B or beta method
R0 = 10000.0 # reference resistance at 25C in ohms for use in the simple Beta method

# Steinhart-Hart a, b, c constants for a 10kohm thermistor
# ref http://www.skyeinstruments.com/wp-content/uploads/Steinhart-Hart-Eqn-for-10k-Thermistors.pdf
SH_A = 0.001125308852122
SH_B = 0.000234711863267
SH_C = 0.000000085663516

# This code sets the RPi to use the BCM (Broadcom) pin numbers which is usually the default but is positively set here
GPIO.setmode(GPIO.BCM)

# For more information about thermistors see the documentation supplied with the kit


# GPIO pin_charge charges the capacitor through a fixed 1kohm resistor and the thermistor in series
# GPIO pin_discharge discharges the capacitor through a fixed 1kohm resistor 
pin_charge = 13
pin_discharge = 19

button_pin = 26    # this is the GPIO pin that one side of the bottom tactile button is connected to

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
# this is a special setting that indicates when a pin changes from LOW to HIGH ie when the button is pressed

# this is a function to indicate when the button is pressed 
def btn_pressed():
    # if button is pressed GPIO.input will report FALSE
    if not GPIO.input(button_pin):
        return 1

# this function discharges (empties) the capacitor so it is ready to be recharged (filled up)
def discharge():
    GPIO.setup(pin_charge, GPIO.IN)
    GPIO.setup(pin_discharge, GPIO.OUT)
    GPIO.output(pin_discharge, False)
    time.sleep(0.01)  # this wait time is set to a value large enough for the capacitor to fully discharge

# this function returns the time taken for the GPIO pin_charge to go HIGH
# this means the voltage on the capacitor has reached the GPIO_high value
def charge_time():
    GPIO.setup(pin_discharge, GPIO.IN)    # configure the GPIO pin_discharge to be an input
    GPIO.setup(pin_charge, GPIO.OUT)      # configure the GPIO pin_charge to be an output
    GPIO.output(pin_charge, True)         # set the GPIO pin_charge HIGH so that it starts to charge the capacitor
    t1 = time.time()                      # start the clock by recording the current time
    while not GPIO.input(pin_discharge):  # loop while the GPIO pin_discharge is still not HIGH ie capacitor not charged
        pass
    t2 = time.time()                # stop the clock by recording the difference between the current and the start times
    #  if here then the GPIO pin_discharge is HIGH ie the capacitor has charged so we can return the time in microseconds
    deltaT = (t2-t1) * 1000000      # times were in seconds so multiply by 1000000 to get microseconds
    print("charge time (usecs): " + str(deltaT) )
    return deltaT      

# this function records the time taken to charge the capacitor to the level when the GPIO#23 pin goes HIGH
# this value is set as GPIO_high but ideally needs to be measured separately for the particular RPi
def time_read():
    discharge()                   # first discharge the capacitor just in case
    t_recharge = charge_time()    # now find the recharging time
    discharge()                   # discharge the capacitor ready to be used again
    print ("recharge time usec for this loop: " + str(t_recharge))
    return t_recharge             # return the recharge time in microseconds

# this function converts the time taken to charge the capacitor into a value of resistance
# to make the answer as good as possible and reduce errors, a number of readings are taken and the average used.
def calc_resistance():
    n = 20             # this is the number of readings we will take
    totaltime = 0      # set the total of the time readings to zero at the start of the cycle
    for i in range(1, n+1):                   # loop through the following line of code n times: NB stops at n+1
        totaltime = totaltime + time_read()   # this is the running total of readings taken so far
        print ("loop " + str(i) + " of " + str(n))
        print ("current total time usec: " + str(totaltime))

    t_average = totaltime / float(n)          # on completion of the loop above calculate the average time reading
    print ("t_average usec: " + str(t_average))
    # tau is the RC time constant ie tau = R*C and is defined as the time
    # to reach 63.2% of the capacitor charging voltage - which is 3.3V from the GPIO pin
    # and from a normal charging curve at 0.7*tau the capacitor voltage will be 50% of the charging voltage
    # at this part of the charging curve we can approximate it to a straight line
    # so a simple approximation is that the ratio of the time to reach GPIO_high is the same as reaching 50% i.e
    tau = (t_average * 0.5 * 3.3)/(GPIO_high * 0.7)
    print ("tau usec: " + str(tau))
    R_combined = tau/C   # if we know tau then we can calculate the combined resistance from tau=R*C tau:usec C:uF
    print ("R_combined: " + str(R_combined))

    R_thermistor = R_combined - R1  # therefore the thermistor resistance is calculated by subtracting the fixed resistor

    print ("R thermistor (ohms): " + "%.1f" % R_thermistor)       # show resistance with 1 decimal place
    return R_thermistor


def read_temp_c():
    R = calc_resistance()

    t0 = 273.15     # 0 deg C in K
    t25 = t0 + 25.0 # 25 deg C in K


    # simple beta method
    beta_inv_T = 1/t25 + 1/B * math.log(R/R0)
    beta_T = (1/beta_inv_T - t0)

    # full Steinhart-Hart equation
    inv_T = SH_A + SH_B * math.log(R) + SH_C * math.pow(math.log(R),3)
    T = (1/inv_T - t0)
    return (T, beta_T)

###########
# main code
###########

print (" ")
print ("program running: press button 2 (bottom) to take a temperature reading or CTRL-C to stop ")

try:    # this loop is not strictly necessary but it does allow the script to be easily stopped with CTRL-C
    while True:  # this is the loop that checks if the button is pressed and takes a reading if it is

        while not btn_pressed():
            pass                         # if not pressed just loop endlessly

        print(" ")
        print ("button 2 pressed: temperature measurement process started")
        print(" ")
        temp_c, temp_c_beta = read_temp_c()  # button is pressed so take an average temperature reading in degrees C

        print("Assumed GPIO HIGH: " + str(GPIO_high))
        print("Temperature reading full Steinhart-Hart: " + "%.1f" % temp_c)       # show temp with 1 decimal place
        print("Temperature reading simple beta method:  " + "%.1f" % temp_c_beta)  # show temp with 1 decimal place
        print("  ")
        # now start the while loop again
        print ("press button 2 (bottom) again to take another temperature measurement or CTRL-C to stop ")

finally:  # this code is run when the try is interrupted with a CTRL-C
    print(" ")
    print("Cleaning up the GPIO pins before stopping")
    print(" ")
    print(" ")
    print(" ")
    GPIO.cleanup()
    
# The cleanup command sets all the pins back to inputs which protects the
# Pi from accidental shorts-circuits if something metal touches the GPIO pins.
