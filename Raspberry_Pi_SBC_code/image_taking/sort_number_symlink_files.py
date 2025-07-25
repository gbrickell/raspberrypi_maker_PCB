#!/usr/bin/python

# sort_number_symlink_files.py - routine to create sorted symbolic link files to the time lapse or stop motion files with a
#   simplified sequential number instead of the time & date info so that avconv can be used to create the video
#
# command: python3 ./RPi_maker_PCB5/image_taking/sort_number_symlink_files.py
#

# import required libraries
import time                # this imports the module to allow various simple time functions to be used
import os                  # this imports the module to allow direct CLI commands to be run
from builtins import input # allows compatibility for input between Python 2 & 3

# get the current username for use in file storage paths
user_name = os.getlogin()

# define the folder where the symlinks to the actual images will be created
symlink_subfolder = " "   # give the variable an initial value
print (" ")
print (" *************************************************************************************************")
print (" All symlinks to the images will be stored under /home/"+user_name+"/RPi_maker_PCB5/image_taking/ ")
print ("   ..... but you must now enter a subfolder name for the ** SYMLINKS **")
print ("   ..... just hit RETURN for the default of 'symlink_default_folder'")
while len(symlink_subfolder) <= 5 or " " in symlink_subfolder :
    symlink_subfolder = input(" Enter sub-folder name - must be more than 5 characters and no spaces (CTRL C to stop? )") or "symlink_default_folder"
print (" *************************************************************************************************")
print (" ")

# build the full path as a text string
symlink_directory = "/home/" + user_name + "/RPi_maker_PCB5/image_taking/" + symlink_subfolder + "/"

# create the symlink directory if it does not exist yet
# this creates the folder on the default SD card
if not os.path.exists(symlink_directory):
    os.makedirs(symlink_directory)
    print (symlink_directory + " folder created")
else:
    print (symlink_directory + " already exists, so no need to create it")
print (" ")

# create the command string to make sure the symlink folder and files are 'owned' by the user so that they are easier to manage
os_chown_command = "chown -R " + user_name +":" + user_name + " " + symlink_directory
os.system(os_chown_command)   # execute the file ownership change command

image_subfolder =  " "   # give the variable an initial null value
# set the target directory where the individual timestamped time lapsed images files have been stored
print (" ")
print (" ----------------------------------------------------------------------------------------------------------------")
print (" All the captured individual images will have been stored under /home/"+user_name+"/RPi_maker_PCB5/image_taking/ ")
print ("   ..... but you must now enter the subfolder name that has been used for the ** STORED IMAGES **")
print ("   ..... just hit RETURN for the default of 'timelapse_image_folder'")
while not os.path.exists("/home/" + user_name + "/RPi_maker_PCB5/image_taking/" + image_subfolder):
    image_subfolder = input(" Enter sub-folder name - which must exist (CTRL C to stop? )") or "timelapse_image_folder"
print (" ----------------------------------------------------------------------------------------------------------------")
print (" ")

# build the full path as a text string
target_directory = "/home/" + user_name + "/RPi_maker_PCB5/image_taking/" + image_subfolder + "/"

# set the system to be in the target directory
#os.chdir(target_directory)

# set start number for sequence
seqno = 0

# create a sorted list of the original timelapse files - which should automatically create the list in time sequence due to the file names used
allfiles = sorted(os.listdir(target_directory))
for filename in allfiles:
    # use os.symlink - a special command - to create the symbolic link files with the simplified/sequential file names
    os.symlink(target_directory + filename, symlink_directory + "{0:04d}".format(seqno) + "_image.jpg")

    #print (" symlink " + symlink_directory + "{0:04d}".format(seqno) + "_image.jpg created for " + filename)
    seqno = seqno + 1

print ("******************************************************************************")
print (str(seqno) + " symbolic link files created in " + symlink_directory)
print ("******************************************************************************")
print (" ")
print ("program finished")
print (" ")