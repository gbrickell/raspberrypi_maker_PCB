#!/usr/bin/python
# dht11_test_example.py uses the dht11.py library functions to capture temperature and humidity readings

# the sensor should either have a built-in pull-up resistor between the power + and signal out connectors,
#   or a seperate resistor should be added to the wiring connections

# command to run: python3 ./RPi_maker_PCB5/sensors/temp_sensors/dht11_test_example.py

import RPi.GPIO as GPIO  # import the GPIO pin management functions
import dht11             # import the custom DHT11 sensor functions - library code is assumed to be in the same folder
import time              # import the time functions
import datetime          # import the date functions

# initialize GPIO
GPIO.setwarnings(False)  # suppress any GPIO pin warning outputs
GPIO.setmode(GPIO.BCM)   # use the standard BCK pin numbering
GPIO.cleanup()           # clean up in case anything may have been previously set and not cleared

# read data using pin 14 and power with 3.3V
instance = dht11.DHT11(pin=14)   # establish the DHT11 instance on GPIO#14 i.e. the sensor output connection

print ("**********************************************")
print ("starting data collection from the DHT11 sensor")
print ("**********************************************")
print (" ")
print (" press CTRL-C to stop")
print (" ")

try:

    while True:
        result = instance.read()   # get the data from the sensor
        #print ("result: " + str(result.is_valid()))     # commented out but can be used to show the 'False' readings
        #print("Temperature: %d C" % result.temperature) # commented out but can be used to show the 'False' readings
        #print("Humidity: %d %%" % result.humidity)      # commented out but can be used to show the 'False' readings
        if result.is_valid():                            # check if the data collected is valid True or False
            print("Last valid input: " + str(datetime.datetime.now()))  # if valid display time and date
            print("*** Temperature: %dC ***" % result.temperature)      # display current temperature
            print("*** Humidity:    %d%% ***" % result.humidity)        # display current humidity

        elif result.error_code == 1:
            print("Missing data - error code: %d" % result.error_code)

        elif result.error_code == 2:
            print("CRC problem - error code: %d" % result.error_code)

        else:
            print("Error code: %d" % result.error_code)

        print(" ")
        time.sleep(10)   # wait 3 second before cycling back to take another set of readings: sensor is only ready every 2 seconds

except KeyboardInterrupt:       # if program is stopped do a GPIO pin clean up
    print (" ")
    print ("*******************************")
    print (" DHT11 data collection stopped ")
    print ("*******************************")
    print (" ")
    GPIO.cleanup()