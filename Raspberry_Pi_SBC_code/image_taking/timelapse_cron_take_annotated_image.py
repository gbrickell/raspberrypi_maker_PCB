#!/usr/bin/python
# timelapse_cron_take_annotated_image.py - simple annotated image taking routine to be run as a cron job for time lapse image capture
#
# command: python3 ./RPi_maker_PCB5/image_taking/timelapse_cron_take_annotated_image.py
#

import time                # this imports the module to allow various simple time functions to be used
import RPi.GPIO as GPIO    # this imports the module to allow the GPIO pins to be easily utilised
import os                  # this imports the module to allow direct CLI commands to be run
from builtins import input # allows compatibility for input between Python 2 & 3
import subprocess
import re

# get the current username for use in file storage paths
user_name = os.getlogin()

# This basic routine does not use any GPIO functions - it just needs the USB camera connected to the Pi
# it should be run with a cron job e.g. as root under the sudo crontab ie create the following entry using "sudo crontab -e"
# script to run every 5 minutes to take an image with the Image Taking PCB's USB camera (adjust time as necessary)
#*/5 * * * * /home/benpi/my_virtual_env/bin/python3 /home/userId/RPi_maker_PCB5/image_taking/timelapse_cron_take_annotated_image.py >> /dev/null 2>> /dev/null
# or
# script to run every 5 minutes from 6am through to 9:55pm (adjust time as necessary)
#*/5 6-21 * * * /home/benpi/my_virtual_env/bin/python3 /home/userId/RPi_maker_PCB5/image_taking/timelapse_cron_take_annotated_image.py >> /dev/null 2>> /dev/null

# define the text part of what is added to each captured image: the default is "Time-lapse image" but
# you can change this to whatever you like and it appears before the timestamp info that is also added
# to the image - you should however limit the text to about 15 characters so that it will fit OK
annotation_text = "Time-lapse image"

# build the full folder path where images will be stored as a text string
imagefolder = "/home/" + user_name + "/RPi_maker_PCB5/image_taking/timelapse_image_folder/"

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

# get the current date and time in a specified format
# as this string will be used in the stored image file name
# only use characters that are allowed in Windows files or 
# the file will not download from the Pi to a Windows machine
now = time.strftime("%Y-%m-%d_%H.%M.%S")   # this creates a string  for use in the file name in this forma: YYYY-mm-dd_HH.MM.SS
datetimenowprint = time.strftime("%H:%M  %d %b %Y")  # and this creates a printable format for annotating the image

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

print (now + " - program running: normally run as a cron job")  # this screen display is left in so it is visible when running the program as a test

image_name = imagefolder + "single_image_" + now + ".jpg"    # create the full file name including the path
print (now + " - single image being taken")      # this screen display is left in so it is visible when running the program as a test

# create the full fswebcam command string: skip first 5 frames, 640x480 resolution, no messages, no banner, 80% compression, stored file name
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

# now add the image annotation text using the convert utility that is part of imagemagick
text_command = "convert " + image_name + " -pointsize 18 -fill white -annotate +20+455 '" + annotation_text + " " + datetimenowprint + "' " + image_name
# the command above sets the text colour as 'white' but you might want to change this to 'black' depending upon the image background
# other choices that might work are 'blue', 'green', red, etc
#print ("text command is: " + text_command)  # this output is usually commented out
os.system(text_command) 
print ("image annotated and resaved with the same name")

# these screen displays are left in so they are visible when running the program as a test
print (" image taken and stored as: " + image_name)
print (" ")

print (" program finished")

