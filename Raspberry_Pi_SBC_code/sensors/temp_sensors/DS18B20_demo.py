#!/usr/bin/python
# DS18B20_demo.py shows how the DS18B20 temp sensor 
#  uses the 1-wire interface to measure temperature
# Author : Enmore Green Limited
# Date   : 210422
# command to run:  python3 ./RPi_maker_kit5/sensors/temp_sensors/DS18B20_demo.py
#  command above to be updated for the user's path to the code

#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# funtion to read the raw temperature reading from the 
#   1-wire interface file automatically created for the detected device
#   where the device address is passed as a parameter
#
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
def temp_raw(address):
    f = open(address, 'r')
    lines = f.readlines()
    f.close()
    return lines

#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# processed temperature reading
#
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
def read_temp(sensor_address):
    # get a first set of raw temperature readings from the 1-wire interface data file
    lines = temp_raw(sensor_address)   
    # now keep checking the 1-wire interface data file until new/complete data has been received
    while lines[0].strip()[-3:] != 'YES':    #loop until we find 'YES' on the 1st line
        time.sleep(0.2)
        lines = temp_raw()

    # if here then good data has been received from the 1-wire bus
    #    so decode and display the temperature reading in degC and degF
    temp_output = lines[1].find('t=')

    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

    # return to the main code to repeat the cycle

#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# main code
#
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

import time   # import this library to use the sleep function
import os     # import this library to be able to easily do a file check

# 1-wire interface assumed to be 'on' and the default GPIO#4 pin being used for the 1-wire data input

# set the temp sensor unique serial code to that of the specific DS18B20 being used
#sensor_code = '28-0517c1e67dff'
#sensor_code = '28-0517c1a6ebff'
#sensor_code = '28-0417c1c353ff'
#sensor_code = '28-0417c1b0c5ff'
#sensor_code = '28-020691771b99'
#sensor_code = '28-02089177aeca'
sensor_code = '28-020391774d7e'

# set the full path/file address for where the 1-wire interface puts the sensor's data
temp_sensor = '/sys/bus/w1/devices/' + sensor_code + '/w1_slave'

if os.path.isfile(temp_sensor):
    print ("***************************************************************")
    print ("** Using a DS18B20 sensor to measure and display temperature **")
    print ("   the program runs continuously until stopped with CTRL-C     ")
    print ("***************************************************************")
    # now continuously loop collecting and displaying the latest data from the sensor
    try:    # this loop is not strictly necessary but it does allow the script to be safely stopped with CTRL-C
        while True:
                tempc, tempf = read_temp(temp_sensor)
                print("{:.3f}".format(tempc) + " degC - " + "{:.3f}".format(tempf) + " degF")
                time.sleep(1)
    finally:  # this code is run when the try is interrupted with a CTRL-C
        print ("  ")
        print ("******************")
        print ("** code stopped **")
        print ("******************")
        print ("  ")
        print ("  ")
else:
    print ("***************************************************************")
    print ("the defined DS18B20 probe is not available")
    print ("please check the connection and restart the program")
    print ("***************************************************************")
    print ("  ")
    print ("  ")

