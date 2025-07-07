#!/bin/sh

# this control script supports the Raspberry Pi Maker Kit 5 project
# - when run as shown in the kit documentation it will download various PDFs, Scratch & python programs plus other material

# output a message about 'activating' a virtual environment for using Python
echo "**********************************************"
echo " please note that you should have activated"
echo " a virtual environment so that Python modules"
echo "  are installed by this script correctly"
echo "**********************************************"

# ask for Raspberry Pi user name
echo "Hello - please input the Raspberry Pi user name where everything will be stored:"
read uservarname

# check the script file size is correct as a simple check that the download was OK: size to be updated whenever the script changes
scriptsize=$(stat --format=%s "/home/$uservarname/RPi_maker_PCB5.sh")
echo " downloaded script file size: " $scriptsize
if [ $scriptsize -gt 29400 ] && [ $scriptsize -lt 29530 ]
then

  echo " script size looks OK - executing all the commands"

# create the main kit directory
echo " Creating the main kit folder"
mkdir /home/$uservarname/RPi_maker_PCB5

# download the documentation:
echo " Downloading the documentation"
# 1. download the readme.txt file and store it in the designated folder on the Raspberry Pi
wget -O /home/$uservarname/RPi_maker_PCB5/RPi_maker_PCB5_readme.txt https://onlinedevices.org.uk/dl1530

# 2. download the "Getting Started" PDF and store it in the designated folder on the Raspberry Pi
wget -O /home/$uservarname/RPi_maker_PCB5/RPi_maker_PCB5_getting_started.pdf https://onlinedevices.org.uk/dl1652

# 3. download the "RPi Maker Kit Usage Documentation" PDF and store it in the designated folder on the Raspberry Pi
wget -O /home/$uservarname/RPi_maker_PCB5/RPi_maker_PCB5_usage_documentation.pdf https://onlinedevices.org.uk/dl1531

##################################
# install all the libraries needed
##################################

# image taking
yes | pip3 install Flask
yes | pip3 install future
yes | sudo apt-get install fswebcam
yes | sudo apt install python3-opencv
yes | sudo apt-get install libav-tools
yes | sudo apt-get install feh
yes | sudo apt-get install imagemagick
yes | pip3 install pyautogui

# servo + stepper motors
yes | pip3 install Adafruit_PCA9685

# OLED 128x64 display
yes | pip3 install Adafruit-SSD1306

# C support
yes | sudo apt-get install cmake  # needed for the libPCA9685 install

# libPCA9685 install or delete/reinstall fast 'C' library for PCA9685
FOLDER=/home/$uservarname/libPCA9685
if [ -d "$FOLDER" ] ; then
    echo "removing earlier installed PCA9685 folder contents"
    yes | sudo rm -rf /home/$uservarname/libPCA9685
fi
yes | git clone https://github.com/edlins/libPCA9685

yes | cd /home/$uservarname/libPCA9685
yes | mkdir /home/$uservarname/libPCA9685/build
yes | cd /home/$uservarname/libPCA9685/build
yes | cmake /home/$uservarname/libPCA9685
yes | make
yes | sudo make install
yes | cd /home/$uservarname

# RF comms
yes | pip3 install rpi-rf

##############
# Electronics
##############

# create the Electronics directories
echo " Creating the Electronics folders"
mkdir /home/$uservarname/RPi_maker_PCB5/electronic_basics
# create the electronics Scratch code and web subfolders
echo " Creating the Scratch and web subfolders"
mkdir /home/$uservarname/RPi_maker_PCB5/electronic_basics/scratch1.4
mkdir /home/$uservarname/RPi_maker_PCB5/electronic_basics/scratch2
mkdir /home/$uservarname/RPi_maker_PCB5/electronic_basics/scratch3
mkdir /home/$uservarname/RPi_maker_PCB5/electronic_basics/ebasics_web_controller
mkdir /home/$uservarname/RPi_maker_PCB5/electronic_basics/ebasics_web_controller/static
mkdir /home/$uservarname/RPi_maker_PCB5/electronic_basics/ebasics_web_controller/static/css
mkdir /home/$uservarname/RPi_maker_PCB5/electronic_basics/ebasics_web_controller/static/images
mkdir /home/$uservarname/RPi_maker_PCB5/electronic_basics/ebasics_web_controller/templates

# download the Electronics software

echo " Downloading the Electronics Flask web files"
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/ebasics_web_controller/static/css/normalize_advanced.css https://onlinedevices.org.uk/dl1216
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/ebasics_web_controller/static/css/skeleton_advanced.css https://onlinedevices.org.uk/dl1217
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/ebasics_web_controller/static/images/favicon.png https://onlinedevices.org.uk/dl1218
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/ebasics_web_controller/static/images/RPi_kits_PCB05_20210419_160549156_900w.jpg https://onlinedevices.org.uk/dl1226
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/ebasics_web_controller/static/images/RPi_kits_PCB05_front_image01.png https://onlinedevices.org.uk/dl1225
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/ebasics_web_controller/templates/electronics_header_insert.html https://onlinedevices.org.uk/dl1227
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/ebasics_web_controller/templates/electronics_layout.html https://onlinedevices.org.uk/dl1228
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/ebasics_web_controller/templates/electronics_select_mode1.html https://onlinedevices.org.uk/dl1229
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/ebasics_web_controller/templates/led1_setup_mode.html https://onlinedevices.org.uk/dl1221
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/ebasics_web_controller/templates/run_led1.html https://onlinedevices.org.uk/dl1222

echo " Downloading the Electronics Python code"
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/ebasics_web_controller/LED1_flash_web.py https://onlinedevices.org.uk/dl1224
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/LED_button_buzzer.py https://onlinedevices.org.uk/dl1238
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/LED_button_flash.py https://onlinedevices.org.uk/dl1239
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/LED_flash.py https://onlinedevices.org.uk/dl1240
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/LED_red_amber_green_flash.py https://onlinedevices.org.uk/dl1241
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/LED_red_green_flash.py https://onlinedevices.org.uk/dl1242
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/LED_RGB_flash.py https://onlinedevices.org.uk/dl1243
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/buzzer_player.py https://onlinedevices.org.uk/dl1574

echo " Downloading the Scratch 1.4 code"
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/scratch1.4/LED_button_buzzer.sb https://onlinedevices.org.uk/dl1254
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/scratch1.4/LED_button_flash.sb https://onlinedevices.org.uk/dl1255
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/scratch1.4/LED_flash.sb https://onlinedevices.org.uk/dl1256
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/scratch1.4/LED_red_green_flash.sb https://onlinedevices.org.uk/dl1257
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/scratch1.4/LED_RGB_flash.sb https://onlinedevices.org.uk/dl1258

echo " Downloading the Scratch 2 code"  
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/scratch2/LED_button_buzzer.sb2 https://onlinedevices.org.uk/dl1563
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/scratch2/LED_button_flash.sb2 https://onlinedevices.org.uk/dl1564
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/scratch2/LED_flash.sb2 https://onlinedevices.org.uk/dl1259
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/scratch2/LED_red_green_flash.sb2 https://onlinedevices.org.uk/dl1260
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/scratch2/LED_RGB_flash.sb2 https://onlinedevices.org.uk/dl1261

echo " Downloading the Scratch 3 code"
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/scratch3/LED_button_buzzer.sb2 https://onlinedevices.org.uk/dl1568
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/scratch3/LED_button_flash.sb2 https://onlinedevices.org.uk/dl1569
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/scratch3/LED_flash.sb2 https://onlinedevices.org.uk/dl1570
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/scratch3/LED_red_green_flash.sb2 https://onlinedevices.org.uk/dl1571
wget -O /home/$uservarname/RPi_maker_PCB5/electronic_basics/scratch3/LED_RGB_flash.sb2 https://onlinedevices.org.uk/dl1572


###############
# Image Taking 
###############

# create the Image Taking directories
echo " Creating the Image Taking folders"
mkdir /home/$uservarname/RPi_maker_PCB5/image_taking
# create the electronics Scratch code and web subfolders
echo " Creating the web and image storage subfolders"
mkdir /home/$uservarname/RPi_maker_PCB5/image_taking/image_taking_controller
mkdir /home/$uservarname/RPi_maker_PCB5/image_taking/image_taking_controller/static
mkdir /home/$uservarname/RPi_maker_PCB5/image_taking/image_taking_controller/static/css
mkdir /home/$uservarname/RPi_maker_PCB5/image_taking/image_taking_controller/static/images
mkdir /home/$uservarname/RPi_maker_PCB5/image_taking/image_taking_controller/templates
mkdir /home/$uservarname/RPi_maker_PCB5/image_taking/button_video_folder
mkdir /home/$uservarname/RPi_maker_PCB5/image_taking/button_video_led_folder
mkdir /home/$uservarname/RPi_maker_PCB5/image_taking/button_video_timer_folder
mkdir /home/$uservarname/RPi_maker_PCB5/image_taking/PIR_image_folder
mkdir /home/$uservarname/RPi_maker_PCB5/image_taking/single_image_folder
mkdir /home/$uservarname/RPi_maker_PCB5/image_taking/single_image_led_folder
mkdir /home/$uservarname/RPi_maker_PCB5/image_taking/single_image_timer_folder
mkdir /home/$uservarname/RPi_maker_PCB5/image_taking/stopmotion_video_folder
mkdir /home/$uservarname/RPi_maker_PCB5/image_taking/timelapse_image_folder
mkdir /home/$uservarname/RPi_maker_PCB5/image_taking/timelapse_video_folder
mkdir /home/$uservarname/RPi_maker_PCB5/image_taking/video_clip_folder


# download the Image Taking software
echo " Downloading the Image Taking Flask web files"
wget -O /home/$uservarname/RPi_maker_PCB5/image_taking/image_taking_controller/static/css/normalize_advanced.css https://onlinedevices.org.uk/dl1216
wget -O /home/$uservarname/RPi_maker_PCB5/image_taking/image_taking_controller/static/css/skeleton_advanced.css https://onlinedevices.org.uk/dl1217
wget -O /home/$uservarname/RPi_maker_PCB5/image_taking/image_taking_controller/static/images/favicon.png https://onlinedevices.org.uk/dl1218
wget -O /home/$uservarname/RPi_maker_PCB5/image_taking/image_taking_controller/static/images/RPi_kits_PCB05_20210419_160549156_900w.jpg https://onlinedevices.org.uk/dl1226
wget -O /home/$uservarname/RPi_maker_PCB5/image_taking/image_taking_controller/static/images/RPi_kits_PCB05_front_image01.png https://onlinedevices.org.uk/dl1225
wget -O /home/$uservarname/RPi_maker_PCB5/image_taking/image_taking_controller/templates/cam_options_setup.html https://onlinedevices.org.uk/dl1591
wget -O /home/$uservarname/RPi_maker_PCB5/image_taking/image_taking_controller/templates/cam_setup_mode.html https://onlinedevices.org.uk/dl1592
wget -O /home/$uservarname/RPi_maker_PCB5/image_taking/image_taking_controller/templates/header_insert.html https://onlinedevices.org.uk/dl1593
wget -O /home/$uservarname/RPi_maker_PCB5/image_taking/image_taking_controller/templates/layout.html https://onlinedevices.org.uk/dl1594
wget -O /home/$uservarname/RPi_maker_PCB5/image_taking/image_taking_controller/templates/select_mode.html https://onlinedevices.org.uk/dl1595
wget -O /home/$uservarname/RPi_maker_PCB5/image_taking/image_taking_controller/templates/stream_video_mode.html https://onlinedevices.org.uk/dl1596

echo " Downloading the Image Taking Python code"
wget -O /home/$uservarname/RPi_maker_PCB5/image_taking/image_taking_controller/image_camera_usb_opencv_annotate.py https://onlinedevices.org.uk/dl1597
wget -O /home/$uservarname/RPi_maker_PCB5/image_taking/image_taking_controller/image_streaming_app_root_annotate.py https://onlinedevices.org.uk/dl1598
wget -O /home/$uservarname/RPi_maker_PCB5/image_taking/image_taking_controller/image_streaming_app_user_annotate.py https://onlinedevices.org.uk/dl1599
wget -O /home/$uservarname/RPi_maker_PCB5/image_taking/button_led_take_image.py https://onlinedevices.org.uk/dl1600
wget -O /home/$uservarname/RPi_maker_PCB5/image_taking/button_led_take_video.py https://onlinedevices.org.uk/dl1601
wget -O /home/$uservarname/RPi_maker_PCB5/image_taking/button_take_image.py https://onlinedevices.org.uk/dl1602
wget -O /home/$uservarname/RPi_maker_PCB5/image_taking/button_take_video.py https://onlinedevices.org.uk/dl1603
wget -O /home/$uservarname/RPi_maker_PCB5/image_taking/button_timer_take_image.py https://onlinedevices.org.uk/dl1604
wget -O /home/$uservarname/RPi_maker_PCB5/image_taking/button_timer_take_video.py https://onlinedevices.org.uk/dl1605
wget -O /home/$uservarname/RPi_maker_PCB5/image_taking/PIR_take_image.py https://onlinedevices.org.uk/dl1606
wget -O /home/$uservarname/RPi_maker_PCB5/image_taking/sort_number_symlink_files.py https://onlinedevices.org.uk/dl1607
wget -O /home/$uservarname/RPi_maker_PCB5/image_taking/timelapse_cron_take_annotated_image.py https://onlinedevices.org.uk/dl1608
wget -O /home/$uservarname/RPi_maker_PCB5/image_taking/timelapse_cron_take_image.py https://onlinedevices.org.uk/dl1609

##############
# Displays
##############
# create the Display project directories
echo " Creating the Display project folders"
mkdir /home/$uservarname/RPi_maker_PCB5/displays
mkdir /home/$uservarname/RPi_maker_PCB5/displays/IPS_240X240_SPI
mkdir /home/$uservarname/RPi_maker_PCB5/displays/IPS_240X240_SPI/font
mkdir /home/$uservarname/RPi_maker_PCB5/displays/IPS_240X240_SPI/pic
mkdir /home/$uservarname/RPi_maker_PCB5/displays/IPS_240X240_SPI/source
mkdir /home/$uservarname/RPi_maker_PCB5/displays/IPS_80x160_SPI
mkdir /home/$uservarname/RPi_maker_PCB5/displays/LCD_1602_i2c_display
mkdir /home/$uservarname/RPi_maker_PCB5/displays/MAX7219_7segment_LED
mkdir /home/$uservarname/RPi_maker_PCB5/displays/OLED_128x64_I2C
mkdir /home/$uservarname/RPi_maker_PCB5/displays/TM1637_7segment_LED

# download the Display project software
echo " Downloading the Display project Python code"
wget -O /home/$uservarname/RPi_maker_PCB5/displays/IPS_240X240_SPI/font/simsun.ttc https://onlinedevices.org.uk/dl1532
wget -O /home/$uservarname/RPi_maker_PCB5/displays/IPS_240X240_SPI/pic/pic-1.jpg https://onlinedevices.org.uk/dl1533
wget -O /home/$uservarname/RPi_maker_PCB5/displays/IPS_240X240_SPI/pic/pic-2.jpg https://onlinedevices.org.uk/dl1534
wget -O /home/$uservarname/RPi_maker_PCB5/displays/IPS_240X240_SPI/pic/pic-3.jpg https://onlinedevices.org.uk/dl1535
wget -O /home/$uservarname/RPi_maker_PCB5/displays/IPS_240X240_SPI/source/1.3_IPS_LCD.py https://onlinedevices.org.uk/dl1536
wget -O /home/$uservarname/RPi_maker_PCB5/displays/IPS_240X240_SPI/source/lcd.py https://onlinedevices.org.uk/dl1537
wget -O /home/$uservarname/RPi_maker_PCB5/displays/IPS_240X240_SPI/source/lcd_spi.py https://onlinedevices.org.uk/dl1538

wget -O /home/$uservarname/RPi_maker_PCB5/displays/IPS_80x160_SPI/cat.jpg https://onlinedevices.org.uk/dl1539
wget -O /home/$uservarname/RPi_maker_PCB5/displays/IPS_80x160_SPI/deployrainbows.gif https://onlinedevices.org.uk/dl1540
wget -O /home/$uservarname/RPi_maker_PCB5/displays/IPS_80x160_SPI/framerate.py https://onlinedevices.org.uk/dl1541
wget -O /home/$uservarname/RPi_maker_PCB5/displays/IPS_80x160_SPI/gif.py https://onlinedevices.org.uk/dl1542
wget -O /home/$uservarname/RPi_maker_PCB5/displays/IPS_80x160_SPI/image.py https://onlinedevices.org.uk/dl1543
wget -O /home/$uservarname/RPi_maker_PCB5/displays/IPS_80x160_SPI/scrolling-text.py https://onlinedevices.org.uk/dl1544
wget -O /home/$uservarname/RPi_maker_PCB5/displays/IPS_80x160_SPI/shapes.py https://onlinedevices.org.uk/dl1545

wget -O /home/$uservarname/RPi_maker_PCB5/displays/LCD_1602_i2c_display/hello_world.py https://onlinedevices.org.uk/dl1546
wget -O /home/$uservarname/RPi_maker_PCB5/displays/LCD_1602_i2c_display/I2C_LCD_driver.py https://onlinedevices.org.uk/dl1547
wget -O /home/$uservarname/RPi_maker_PCB5/displays/LCD_1602_i2c_display/LCD_all_functions_demo.py https://onlinedevices.org.uk/dl1548

wget -O /home/$uservarname/RPi_maker_PCB5/displays/MAX7219_7segment_LED/sevensegment_demo.py https://onlinedevices.org.uk/dl1549

wget -O /home/$uservarname/RPi_maker_PCB5/displays/OLED_128x64_I2C/animate.py https://onlinedevices.org.uk/dl1550
wget -O /home/$uservarname/RPi_maker_PCB5/displays/OLED_128x64_I2C/happycat_oled_32.ppm https://onlinedevices.org.uk/dl1551
wget -O /home/$uservarname/RPi_maker_PCB5/displays/OLED_128x64_I2C/happycat_oled_64.ppm https://onlinedevices.org.uk/dl1552
wget -O /home/$uservarname/RPi_maker_PCB5/displays/OLED_128x64_I2C/image.py https://onlinedevices.org.uk/dl1553
wget -O /home/$uservarname/RPi_maker_PCB5/displays/OLED_128x64_I2C/shapes.py https://onlinedevices.org.uk/dl1554
wget -O /home/$uservarname/RPi_maker_PCB5/displays/OLED_128x64_I2C/simple_text.py https://onlinedevices.org.uk/dl1555
wget -O /home/$uservarname/RPi_maker_PCB5/displays/OLED_128x64_I2C/SSD1306.py https://onlinedevices.org.uk/dl1556

wget -O /home/$uservarname/RPi_maker_PCB5/displays/TM1637_7segment_LED/TM1637_test01.py https://onlinedevices.org.uk/dl1557

###########################################################
# customisation to update Platform.py in Adafruit_GPIO
###########################################################
echo " "
echo "*********************************** "
echo " "

# check what version of python3 is being used
version=$(python3 -V 2>&1 | grep -Po '(?<=Python )(.+)')
shortver=$(printf '%-.3s' "$version")

# build the paths to both the .local and the /usr/local folders
part1a=/usr/local/lib/python
part1b=/home/$uservarname/.local/lib/python
part3a=/dist-packages/Adafruit_GPIO/
part3b=/site-packages/Adafruit_GPIO/
usrGPIOFOLDER="$part1a$shortver$part3a"
locGPIOFOLDER="$part1b$shortver$part3b"
echo " usrGPIOFOLDER: " $usrGPIOFOLDER
echo " locGPIOFOLDER: " $locGPIOFOLDER

filename=Platform_copy.py
GPIOFILEA="$usrGPIOFOLDER/$filename"
echo " GPIOFILE usr: " $GPIOFILEA
GPIOFILEB="$locGPIOFOLDER/$filename"
echo " GPIOFILE loc: " $GPIOFILEB

# update the /usr/local file if installed here
if [ -r "$GPIOFILEA" ]
then 
    fileA=1
else
    fileA=0
fi
if [ -d "$usrGPIOFOLDER" ] &&  [ $fileA -eq 0 ]
then
    cd $usrGPIOFOLDER
    sudo cp Platform.py Platform_copy.py
    sudo wget -O Platform.py https://onlinedevices.org.uk/dl2145
    #cd /home/$uservarname
    echo " custom Adafruit Platform.py uploaded to /usr python$shortver"
else
    echo " no Platform file action for /usr python$shortver"
fi

# update the .local file if installed here
if [ -r "$GPIOFILEB" ]
then 
    fileB=1
else
    fileB=0
fi
if [ -d "$locGPIOFOLDER" ] &&  [ $fileB -eq 0 ]
then
    cd $locGPIOFOLDER
    sudo cp Platform.py Platform_copy.py
    sudo wget -O Platform.py https://onlinedevices.org.uk/dl2145
    #cd /home/$uservarname
    echo " custom Adafruit Platform.py uploaded to .local python$shortver"
else
    echo " no Platform file action for .local python$shortver"
fi

echo " "
echo "*********************************** "
echo " "


##################
# Motor Control  #
##################

# create the Motor Control directories
echo " Creating the Motor Control folders"
mkdir /home/$uservarname/RPi_maker_PCB5/motor_control
mkdir /home/$uservarname/RPi_maker_PCB5/motor_control/drive_motors
mkdir /home/$uservarname/RPi_maker_PCB5/motor_control/drive_motors/HG7881_motor_controller
mkdir /home/$uservarname/RPi_maker_PCB5/motor_control/drive_motors/L298N_motor_controller
mkdir /home/$uservarname/RPi_maker_PCB5/motor_control/servo_motors
mkdir /home/$uservarname/RPi_maker_PCB5/motor_control/stepper_motors
mkdir /home/$uservarname/RPi_maker_PCB5/motor_control/web_motor_controller
mkdir /home/$uservarname/RPi_maker_PCB5/motor_control/web_motor_controller/static
mkdir /home/$uservarname/RPi_maker_PCB5/motor_control/web_motor_controller/static/css
mkdir /home/$uservarname/RPi_maker_PCB5/motor_control/web_motor_controller/static/images
mkdir /home/$uservarname/RPi_maker_PCB5/motor_control/web_motor_controller/templates

# download the Motor Control software
echo " Downloading the Motor Control Flask web files"
wget -O /home/$uservarname/RPi_maker_PCB5/motor_control/web_motor_controller/static/css/normalize_advanced.css https://onlinedevices.org.uk/dl1216
wget -O /home/$uservarname/RPi_maker_PCB5/motor_control/web_motor_controller/static/css/skeleton_advanced.css https://onlinedevices.org.uk/dl1217
wget -O /home/$uservarname/RPi_maker_PCB5/motor_control/web_motor_controller/static/images/favicon.png https://onlinedevices.org.uk/dl1218
wget -O /home/$uservarname/RPi_maker_PCB5/motor_control/web_motor_controller/templates/select_motor_mode.html https://onlinedevices.org.uk/dl1614
wget -O /home/$uservarname/RPi_maker_PCB5/motor_control/web_motor_controller/templates/select_motor_mode_nosudo.html https://onlinedevices.org.uk/dl1615
wget -O /home/$uservarname/RPi_maker_PCB5/motor_control/web_motor_controller/templates/semaphore_message.html https://onlinedevices.org.uk/dl1616
wget -O /home/$uservarname/RPi_maker_PCB5/motor_control/web_motor_controller/templates/stepper_gauge_setup.html https://onlinedevices.org.uk/dl1617

echo " Downloading the Motor Control Python code"
wget -O /home/$uservarname/RPi_maker_PCB5/motor_control/web_motor_controller/web_motor_control_app.py https://onlinedevices.org.uk/dl1613
wget -O /home/$uservarname/RPi_maker_PCB5/motor_control/web_motor_controller/web_motor_control_app_nosudo.py https://onlinedevices.org.uk/dl1612
wget -O /home/$uservarname/RPi_maker_PCB5/motor_control/drive_motors/HG7881_motor_controller/HG7881-motors_LCD_on_off.py https://onlinedevices.org.uk/dl1618
wget -O /home/$uservarname/RPi_maker_PCB5/motor_control/drive_motors/HG7881_motor_controller/HG7881-motors_LCD_PWM.py https://onlinedevices.org.uk/dl1619
wget -O /home/$uservarname/RPi_maker_PCB5/motor_control/drive_motors/HG7881_motor_controller/I2C_LCD_driver.py https://onlinedevices.org.uk/dl1620
wget -O /home/$uservarname/RPi_maker_PCB5/motor_control/drive_motors/L298N_motor_controller/I2C_LCD_driver.py https://onlinedevices.org.uk/dl1620
wget -O /home/$uservarname/RPi_maker_PCB5/motor_control/drive_motors/L298N_motor_controller/L298N_motors_LCD_on_off.py https://onlinedevices.org.uk/dl1621
wget -O /home/$uservarname/RPi_maker_PCB5/motor_control/drive_motors/L298N_motor_controller/L298N_motors_LCD_PWM.py https://onlinedevices.org.uk/dl1622
wget -O /home/$uservarname/RPi_maker_PCB5/motor_control/servo_motors/I2C_2servo_btn.py https://onlinedevices.org.uk/dl1623
wget -O /home/$uservarname/RPi_maker_PCB5/motor_control/servo_motors/I2C_servo_btn.py https://onlinedevices.org.uk/dl1624
wget -O /home/$uservarname/RPi_maker_PCB5/motor_control/servo_motors/semaphore_I2C_2servo.py https://onlinedevices.org.uk/dl1625
wget -O /home/$uservarname/RPi_maker_PCB5/motor_control/servo_motors/simple_servo_btn.py https://onlinedevices.org.uk/dl1626
wget -O /home/$uservarname/RPi_maker_PCB5/motor_control/stepper_motors/cpu_temp_gauge_full_step.py https://onlinedevices.org.uk/dl1627
wget -O /home/$uservarname/RPi_maker_PCB5/motor_control/stepper_motors/full_step_stepper.py https://onlinedevices.org.uk/dl1628
wget -O /home/$uservarname/RPi_maker_PCB5/motor_control/stepper_motors/half_step_stepper.py https://onlinedevices.org.uk/dl1629
wget -O /home/$uservarname/RPi_maker_PCB5/motor_control/stepper_motors/wave_drive_stepper.py https://onlinedevices.org.uk/dl1630

################
### Sensors  ###
################

# create the Sensor directories
echo " Creating the Sensor folders"
mkdir /home/$uservarname/RPi_maker_PCB5/sensors
mkdir /home/$uservarname/RPi_maker_PCB5/sensors/light_sensors
mkdir /home/$uservarname/RPi_maker_PCB5/sensors/magnetic_sensors
mkdir /home/$uservarname/RPi_maker_PCB5/sensors/MPR121_touch_sensor
mkdir /home/$uservarname/RPi_maker_PCB5/sensors/object_detection
mkdir /home/$uservarname/RPi_maker_PCB5/sensors/object_detection/microwave_detection
mkdir /home/$uservarname/RPi_maker_PCB5/sensors/object_detection/PIR_detection
mkdir /home/$uservarname/RPi_maker_PCB5/sensors/object_detection/ultrasonic_detection
mkdir /home/$uservarname/RPi_maker_PCB5/sensors/pressure_sensors
mkdir /home/$uservarname/RPi_maker_PCB5/sensors/RFID_sensing
mkdir /home/$uservarname/RPi_maker_PCB5/sensors/temp_sensors
mkdir /home/$uservarname/RPi_maker_PCB5/sensors/TTP229_touch_keypad

echo " Downloading the Sensor Python code"
#wget -O /home/$uservarname/RPi_maker_PCB5/sensors/MPR121_touch_sensor/cap-touch.py https://onlinedevices.org.uk/dl1631
#wget -O /home/$uservarname/RPi_maker_PCB5/sensors/MPR121_touch_sensor/keyboard.py https://onlinedevices.org.uk/dl1632
wget -O /home/$uservarname/RPi_maker_PCB5/sensors/MPR121_touch_sensor/MPR121.py https://onlinedevices.org.uk/dl1633
#wget -O /home/$uservarname/RPi_maker_PCB5/sensors/MPR121_touch_sensor/playtest.py https://onlinedevices.org.uk/dl1634
wget -O /home/$uservarname/RPi_maker_PCB5/sensors/MPR121_touch_sensor/simpletest.py https://onlinedevices.org.uk/dl1635
#wget -O /home/$uservarname/RPi_maker_PCB5/sensors/TTP229_touch_keypad/TTP229_test01.py https://onlinedevices.org.uk/dl1636
#wget -O /home/$uservarname/RPi_maker_PCB5/sensors/TTP229_touch_keypad/TTP229_test02.py https://onlinedevices.org.uk/dl1637

wget -O /home/$uservarname/RPi_maker_PCB5/sensors/object_detection/microwave_detection/microwave_detect01.py https://onlinedevices.org.uk/dl1636
wget -O /home/$uservarname/RPi_maker_PCB5/sensors/object_detection/PIR_detection/PIR_detect01.py https://onlinedevices.org.uk/dl1637
wget -O /home/$uservarname/RPi_maker_PCB5/sensors/object_detection/ultrasonic_detection/ultrasonic_detect01.py https://onlinedevices.org.uk/dl1638

wget -O /home/$uservarname/RPi_maker_PCB5/sensors/pressure_sensors/bmp180.py https://onlinedevices.org.uk/dl1920

wget -O /home/$uservarname/RPi_maker_PCB5/sensors/magnetic_sensors/US5881_hall.py https://onlinedevices.org.uk/dl2015

# not loading the RFID code yet

wget -O /home/$uservarname/RPi_maker_PCB5/sensors/temp_sensors/dht11.py https://onlinedevices.org.uk/dl1641
wget -O /home/$uservarname/RPi_maker_PCB5/sensors/temp_sensors/dht11_test_example.py https://onlinedevices.org.uk/dl1642
wget -O /home/$uservarname/RPi_maker_PCB5/sensors/temp_sensors/dht11_test_LCD_example.py https://onlinedevices.org.uk/dl1643
wget -O /home/$uservarname/RPi_maker_PCB5/sensors/temp_sensors/DS18B20_demo.py https://onlinedevices.org.uk/dl1644
wget -O /home/$uservarname/RPi_maker_PCB5/sensors/temp_sensors/DS18B20_LCD_demo.py https://onlinedevices.org.uk/dl1645
wget -O /home/$uservarname/RPi_maker_PCB5/sensors/temp_sensors/I2C_LCD_driver.py https://onlinedevices.org.uk/dl1646
wget -O /home/$uservarname/RPi_maker_PCB5/sensors/temp_sensors/thermistor_sensor.py https://onlinedevices.org.uk/dl1647

wget -O /home/$uservarname/RPi_maker_PCB5/sensors/light_sensors/phototran_light_sensor.py https://onlinedevices.org.uk/dl1244


#################
### RF comms  ###
#################
# create the RF comms directories
echo " Creating the RF comms folders"
mkdir /home/$uservarname/RPi_maker_PCB5/RF_communication
mkdir /home/$uservarname/RPi_maker_PCB5/RF_communication/C218D001C+FS1000A_comms
mkdir /home/$uservarname/RPi_maker_PCB5/RF_communication/RXB8_comms
mkdir /home/$uservarname/RPi_maker_PCB5/RF_communication/SRX882+STX882_comms

echo " Downloading the RF comms Python code"
wget -O /home/$uservarname/RPi_maker_PCB5/RF_communication/C218D001C+FS1000A_comms/Key_Fob_RX_plot_C218D001C.py https://onlinedevices.org.uk/dl1943
wget -O /home/$uservarname/RPi_maker_PCB5/RF_communication/C218D001C+FS1000A_comms/rpi-rf_receive.py https://onlinedevices.org.uk/dl1944
wget -O /home/$uservarname/RPi_maker_PCB5/RF_communication/C218D001C+FS1000A_comms/switch_socket02.py https://onlinedevices.org.uk/dl1945
wget -O /home/$uservarname/RPi_maker_PCB5/RF_communication/RXB8_comms/Key_Fob_RX_plot_RXB8.py https://onlinedevices.org.uk/dl1941
wget -O /home/$uservarname/RPi_maker_PCB5/RF_communication/RXB8_comms/rpi-rf_receive.py https://onlinedevices.org.uk/dl1942
wget -O /home/$uservarname/RPi_maker_PCB5/RF_communication/SRX882+STX882_comms/Key_Fob_RX_plot.py https://onlinedevices.org.uk/dl1938
wget -O /home/$uservarname/RPi_maker_PCB5/RF_communication/SRX882+STX882_comms/rpi-rf_receive.py https://onlinedevices.org.uk/dl1939
wget -O /home/$uservarname/RPi_maker_PCB5/RF_communication/SRX882+STX882_comms/switch_socket02.py https://onlinedevices.org.uk/dl1940


########################################
echo " All downloads are now complete."
echo " "
echo " You might want to scroll back through the Terminal output to see if there are any errors and "
echo " also please read the downloaded RPi_maker_PCB5_readme01.txt file to see the latest information "
echo " regarding this kit and advice on how you can dispose of it, if or when you are finished with it."
echo " "
echo " "

# now remove the script so that it can be run again if necessary
rm /home/$uservarname/RPi_maker_PCB5.sh


else

  echo " script size doesn't seem right - suggest you try downloading it again"

fi



