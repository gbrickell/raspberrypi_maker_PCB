#!/usr/bin/python
# RPi kits PCB version of PIR_take_image.py - image taking routine triggered by movement detected by a PIR
#
# command: python3 ./RPi_maker_kit5/image_taking/PIR_take_image.py
#

import time                # this imports the module to allow various simple time functions to be used
import RPi.GPIO as GPIO    # this imports the module to allow the GPIO pins to be easily utilised
import os                  # this imports the module to allow direct CLI commands to be run
from builtins import input # allows compatibility for input between Python 2 & 3
import subprocess
import re

# get the current username for use in file storage paths
user_name = os.getlogin()

# This code sets the RPi to use the BCM (Broadcom) pin numbers which is usually the default but is positively set here
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)   # avoids various warning messages about GPIO pins being already in use

pir_pin = 23     # this is the GPIO input pin that the PIR OUT pin is connected to

GPIO.setup(pir_pin, GPIO.IN)   # this sets the input GPIO pin from the PIR to be an input 'type' i.e. it will register  
                               #  either HIGH or LOW depending upon whether it sees a c. 3.3V at the pin 

# define the folder where images will be stored
time_subfolder = " "   # give the variable an initial value
print (" ")
print (" **************************************************************************************************")
print (" All PIR detected images will be stored under /home/" + user_name + "/RPi_maker_kit5/image_taking/ ")
print ("   ..... but you must now enter a subfolder name")
print ("   ..... just hit RETURN for the default of 'PIR_image_folder'")
while len(time_subfolder) <= 5 or " " in time_subfolder :
    time_subfolder = input(" Enter sub-folder name - must be more than 5 characters and no spaces (CTRL C to stop? )") or "PIR_image_folder"
print (" **************************************************************************************************")
print (" ")

# build the full path as a text string
imagefolder = "/home/" + user_name + "/RPi_maker_kit5/image_taking/" + time_subfolder + "/"

# create the directory if it does not exist
if not os.path.exists(imagefolder):
    os.makedirs(imagefolder)      # execute the folder creation command

    # in some circumstances new file/directory ownership may become an issue
    # so the lines below create a command string to make sure the new directory and its files are 'owned' by 'user_name'
    os_chown_command = "chown -R " + user_name +":" + user_name + " " + imagefolder
    os.system(os_chown_command)   # execute the file ownership change command

    print (imagefolder + " folder created")
else:
    print (imagefolder + " already exists, so no need to create it")
print (" ")

# initialise some control variables
Current_State  = 0      # simple variable to indicate the detection state
trigger_interval = 5    # minimum interval in seconds between images to avoid multiple images from the same movement detection - adjust as needed

# get the current date and time in a specified format
# as this string will be used in the stored image file name
# only use characters that are allowed in Windows files or 
# the file will not download from the Pi to a Windows machine
now = time.strftime("%Y-%m-%d_%H.%M.%S")   # this creates a string in a designated format e.g. YYYY-mm-dd_HH.MM.SS

# check where the USB camera is connected
lsdevres = subprocess.getoutput('ls /dev/')
if len(re.findall("video0", lsdevres)) > 0 :
    print ("/dev/video0 is present")
    usb_device = "-d /dev/video0"
elif len(re.findall("video1", lsdevres)) > 0 :
    print ("/dev/video1 is present")
    usb_device = "-d /dev/video1"
elif len(re.findall("video2", lsdevres)) > 0 :
    print ("/dev/video1 is present")
    usb_device = "-d /dev/video2"
else:
    print ("no USB camera is present - exiting the program")
    usb_device = "exit"
    sys.exit()

print (now + " - program running : using a PIR movement detection to take an image - type CTRL-C to stop")
try:    # this loop is not strictly necessary but it does allow the script to be easily stopped with CTRL-C

    #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    # wait for PIR module electronic to settle 
    #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    print ("Waiting for PIR electronics to settle ...")
 
    # Initial mini loop to wait until until PIR output is 0 ie the electronics have settled
    while GPIO.input(pir_pin) == 1:
        Current_State  = 0    
    print ("  Ready - starting detection loop at: " + time.strftime('%a %d %b %Y %H:%M:%S %Z'))
    print ("**********************************************************************")

    while True:  # this is the loop that checks if the PIR is triggered and takes an image if it is

        #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        # check for movement detection
        #+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        # Read PIR state from the input GPIO pin
        Current_State = GPIO.input(pir_pin)
        #print (" Current State = " + str(Current_State))  # debug output usually commented out

        if Current_State == 1:
            #PIR is triggered so take a single image.
            print ("  PIR movement detected at: " + time.strftime('%a %d %b %Y %H:%M:%S %Z'))
            now = time.strftime("%Y-%m-%d_%H.%M.%S") # get the time and date in a format to be used in the file name
            image_name = imagefolder + "single_image_" + now + ".jpg"    # create the full file name including the path
            # create the full fswebcam command string: 
            # skip first 5 frames, 640x480 resolution, no messages, no banner, 80% compression, stored file name
            # the example below does not have any flip or rotate options which may be needed
            # add --rotate <angle> where <angle> can be 90, 180 or 270 if rotation needed
            # add --flip <direction> where <direction> can be h or v if you do want to flip the image for some reason
            # usb_device is determined earlier to set the -d parameter for where the USB camera is connected
            os_image_command = "fswebcam " + usb_device + " -S 5 -r 640x480 -q --no-banner --jpeg 80 " + image_name   
            os.system(os_image_command)          # take the image using the fswebcam command string

            # in some circumstances new file/directory ownership may become an issue
            # so the lines below create a command string to make sure the new file is 'owned' by 'user_name'
            os_chown_command = "chown " + user_name +":" + user_name + " " + image_name
            os.system(os_chown_command)   # execute the file ownership change command

            time.sleep(1)      # wait a short interval before cycling back to allow the image capture to complete
            print (" image taken and stored as: " + image_name)
            print (" waited " + str(trigger_interval) + " seconds before recycling to avoid multiple images from the same movement detection")
            print ("**********************************************************************")
            time.sleep(trigger_interval)
            Current_State  = 0

        time.sleep(0.5)  # this is just a short pause so that the processor is not monopolised by this loop


finally:  # this code is run when the try is interrupted with a CTRL-C
    print(" ")
    print("Cleaning up the GPIO pins before stopping")
    print(" ")
    print(" ")
    print(" ")
    GPIO.cleanup()
    
# The cleanup command sets all the pins back to inputs which protects the
# Pi from accidental shorts-circuits if something metal touches the GPIO pins.

