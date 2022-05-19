# RPI Maker Kit examle code for the TM1637 7 segment LED display

# command:  python3 ./RPi_maker_kit5/displays/TM1637_7segment_LED/TM1637_test01.py


import tm1637  # imports the library that should be installed by: sudo pip3 install raspberrypi-tm1637
import time    # this imports the time module to allow various time functions to be used

tm = tm1637.TM1637(clk=18, dio=15, brightness=5)  # initialise the display using BCM numbering for the two GPIO pins to be used

# Now run through a series of test displays with a pause between each 

# all LEDS on "88:88"
tm.write([127, 255, 127, 127])
time.sleep(3)

# all LEDS off
tm.write([0, 0, 0, 0])
time.sleep(3)

# show "0123"
tm.write([63, 6, 91, 79])
time.sleep(3)

# show "COOL"
tm.write([0b00111001, 0b00111111, 0b00111111, 0b00111000])
time.sleep(3)

# show "HELP"
tm.show('help')
time.sleep(3)

# display "dEAd", "bEEF"
tm.hex(0xdead)
time.sleep(3)
tm.hex(0xbeef)
time.sleep(3)

# show "12:59"
tm.numbers(12, 59)
time.sleep(3)

# show "-123"
tm.number(-123)
time.sleep(3)

# show temperature '24*C'
tm.temperature(24)
time.sleep(10)

# all LEDS off
tm.write([0, 0, 0, 0])
