##!/usr/bin/python
# RPi PCBs PCB version of test software from QDtech co.,LTD downloadable from http://www.lcdwiki.com
# various additions/changes made to their test software

# command python3 ./RPi_maker_PCB5/displays/IPS_240X240_SPI/source/1.3_IPS_LCD.py

#=====================================power supply wiring===========================================//
# OLED Module                Raspberry PI    
#    VCC        connect       DC 3.3V         // Maker PCB PCB 7P black connector 3V3
#    GND        connect          GND          // Maker PCB PCB 7P black connector GND
#======================================data line wiring=============================================//
#The default data bus type for this module is 4-wire SPI
# OLED Module                Raspberry PI 
#    SDA        connect       19(bcm:10)      // Maker PCB PCB 7P black connector MOSI
#======================================control line wiring==========================================//
# OLED Module                Raspberry PI 
#    RES        connect        5(bcm:3)       // Maker PCB PCB GPIO spare #14 
#    DC         connect        3(bcm:2)       // Maker PCB PCB GPIO spare #15 
#    SCL        connect       23(bcm:11)      // Maker PCB PCB 7P black connector SCLK
#    BLK        connect       12(bcm:18)      // Maker PCB PCB GPIO spare #18 
#========================================touch screen wiring========================================//
#  none
#*****************************************************************************************************/	
#/****************************************************************************************************

# -*- coding: UTF-8 -*-
import lcd
import time
import os

from lcd import USE_HORIZONTAL

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

DC =  15
RES = 14
BLK = 18

ColorTab=['RED','GREEN','BLUE','YELLOW','BROWN']
Direction=['Rotation:0','Rotation:90','Rotation:180','Rotation:270']

# get the current username for use in file storage paths
user_name = os.getlogin()

#curpath = os.getcwd()
#font1 = curpath+"/../font/simsun.ttc"
font1 = "/home/" + user_name + "/RPi_maker_PCB5/displays/IPS_240X240_SPI/font/simsun.ttc"

#pic1 = curpath+"/../pic/pic-1.jpg"
#pic2 = curpath+"/../pic/pic-2.jpg"
#pic3 = curpath+"/../pic/pic-3.jpg"
pic1 = "/home/" + user_name + "/RPi_maker_PCB5/displays/IPS_240X240_SPI/pic/pic-1.jpg"
pic2 = "/home/" + user_name + "/RPi_maker_PCB5/displays/IPS_240X240_SPI/pic/pic-2.jpg"
pic3 = "/home/" + user_name + "/RPi_maker_PCB5/displays/IPS_240X240_SPI/pic/pic-3.jpg"

mylcd = lcd.ST7789V(RES,DC,BLK)
mylcd.lcdinit()

while 1:
    lcdimage = Image.new("RGB", (mylcd.width, mylcd.height),"WHITE")
    display = ImageDraw.Draw(lcdimage)
    lcdfont = ImageFont.truetype(font1,16)
    display.rectangle((0,0,mylcd.width,20),fill="BLUE")
    display.rectangle((0,mylcd.height-20,mylcd.width,mylcd.height),fill="BLUE")
    display.text((23,2),"1.3inch IPS test program", font=lcdfont,fill="WHITE")
    display.text((59,mylcd.height-18),"www.lcdwiki.com", font=lcdfont,fill="WHITE")
    display.text((51,73),"QDTECH Electronic", font=lcdfont,fill="RED")
    display.text((55,90),"LCD test program", font=lcdfont,fill="RED")
    display.text((59,107),"1.3inch ST7789V", font=lcdfont,fill="GREEN")
    display.text((91,124),"240x240", font=lcdfont,fill="GREEN")
    display.text((79,141),"2021-04-06", font=lcdfont,fill="BLUE")
    mylcd.lcdimage(lcdimage)
    time.sleep(1.5)

    display.rectangle((0,0,mylcd.width,mylcd.height),fill="WHITE")
    display.text((20,30),"WHITE", font=lcdfont,fill="BLACK")
    mylcd.lcdimage(lcdimage)
    time.sleep(1)
    display.rectangle((0,0,mylcd.width,mylcd.height),fill=0)
    display.text((20,30),"BLACK", font=lcdfont,fill="WHITE")
    mylcd.lcdimage(lcdimage)
    time.sleep(1)
    display.rectangle((0,0,mylcd.width,mylcd.height),fill="RED")
    display.text((20,30),"RED", font=lcdfont,fill="BLUE")
    mylcd.lcdimage(lcdimage)
    time.sleep(1)
    display.rectangle((0,0,mylcd.width,mylcd.height),fill="GREEN")
    display.text((20,30),"GREEN", font=lcdfont,fill="BLUE")
    mylcd.lcdimage(lcdimage)
    time.sleep(1)
    display.rectangle((0,0,mylcd.width,mylcd.height),fill="BLUE")
    display.text((20,30),"BLUE", font=lcdfont,fill="RED")
    mylcd.lcdimage(lcdimage)
    time.sleep(1)

    display.rectangle((0,0,mylcd.width,mylcd.height),fill="WHITE")
    display.rectangle((0,0,mylcd.width,20),fill="BLUE")
    display.rectangle((0,mylcd.height-20,mylcd.width,mylcd.height),fill="BLUE")
    display.text((43,2),"Rectangle Fill test", font=lcdfont,fill="WHITE")
    display.text((59,mylcd.height-18),"www.lcdwiki.com", font=lcdfont,fill="WHITE")
    for i in range(5):
        display.rectangle((mylcd.width/2-40+(i*16),mylcd.height/2-40+(i*13),mylcd.width/2-40+(i*16)+30,mylcd.height/2-40+(i*13)+30),outline=ColorTab[i])
    mylcd.lcdimage(lcdimage)
    time.sleep(1)
    for i in range(5):
        display.rectangle((mylcd.width/2-40+(i*16),mylcd.height/2-40+(i*13),mylcd.width/2-40+(i*16)+30,mylcd.height/2-40+(i*13)+30),fill=ColorTab[i])
    mylcd.lcdimage(lcdimage)
    time.sleep(1)


    display.rectangle((0,0,mylcd.width,mylcd.height),fill="WHITE")
    display.rectangle((0,0,mylcd.width,20),fill="BLUE")
    display.rectangle((0,mylcd.height-20,mylcd.width,mylcd.height),fill="BLUE")
    display.text((55,2),"Circle Fill test", font=lcdfont,fill="WHITE")
    display.text((59,mylcd.height-18),"www.lcdwiki.com", font=lcdfont,fill="WHITE")
    for i in range(5):
        display.ellipse((mylcd.width/2-55+(i*15),mylcd.height/2-40+(i*13),mylcd.width/2-25+(i*15),mylcd.height/2-10+(i*13)),outline=ColorTab[i])
    mylcd.lcdimage(lcdimage)
    time.sleep(1)
    for i in range(5):
        display.ellipse((mylcd.width/2-55+(i*15),mylcd.height/2-40+(i*13),mylcd.width/2-25+(i*15),mylcd.height/2-10+(i*13)),fill=ColorTab[i])
    mylcd.lcdimage(lcdimage)
    time.sleep(1)

    display.rectangle((0,0,mylcd.width,mylcd.height),fill="WHITE")
    display.rectangle((0,0,mylcd.width,20),fill="BLUE")
    display.rectangle((0,mylcd.height-20,mylcd.width,mylcd.height),fill="BLUE")
    display.text((47,2),"Triangle Fill test", font=lcdfont,fill="WHITE")
    display.text((59,mylcd.height-18),"www.lcdwiki.com", font=lcdfont,fill="WHITE")
    for i in range(5):
        display.polygon([(mylcd.width/2-40+(i*15),mylcd.height/2-12+(i*11)),(mylcd.width/2-25-1+(i*15),mylcd.height/2-12-26-1+(i*11)),(mylcd.width/2-10-1+(i*15),mylcd.height/2-12+(i*11))],outline=ColorTab[i])
    mylcd.lcdimage(lcdimage)
    time.sleep(1)
    for i in range(5):
        display.polygon([(mylcd.width/2-40+(i*15),mylcd.height/2-12+(i*11)),(mylcd.width/2-25-1+(i*15),mylcd.height/2-12-26-1+(i*11)),(mylcd.width/2-10-1+(i*15),mylcd.height/2-12+(i*11))],fill=ColorTab[i])
    mylcd.lcdimage(lcdimage)
    time.sleep(1)

    display.rectangle((0,0,mylcd.width,mylcd.height),fill="WHITE")
    display.rectangle((0,0,mylcd.width,20),fill="BLUE")
    display.rectangle((0,mylcd.height-20,mylcd.width,mylcd.height),fill="BLUE")
    display.text((51,2),"FONT Display test", font=lcdfont,fill="WHITE")
    display.text((59,mylcd.height-18),"www.lcdwiki.com", font=lcdfont,fill="WHITE")
    lcdfont = ImageFont.truetype(font1,12)
    display.text((10,23),"6X12:ABCDEabcde0123456789!&*$%#", font=lcdfont,fill="RED")
    lcdfont = ImageFont.truetype(font1,16)
    display.text((10,35),"8X16:ABCDabcd0123456789!&*$", font=lcdfont,fill="RED")
    lcdfont = ImageFont.truetype(font1,24)
    display.text((10,51),"12X24:ABCabc0123!&*", font=lcdfont,fill="RED")
    lcdfont = ImageFont.truetype(font1,32)
    display.text((10,75),"16X32:ABab01!&", font=lcdfont,fill="RED") 
    lcdfont = ImageFont.truetype(font1,48)
    display.text((10,107),"24X48:Aa8", font=lcdfont,fill="RED")
    lcdfont = ImageFont.truetype(font1,60)
    display.text((10,155),"30X60:A", font=lcdfont,fill="RED")
    mylcd.lcdimage(lcdimage)
    time.sleep(1)

    pic = Image.open(pic1)
    mylcd.lcdimage(pic)
    time.sleep(1)
    pic = Image.open(pic2)
    mylcd.lcdimage(pic)
    time.sleep(1)
    pic = Image.open(pic3)
    mylcd.lcdimage(pic)
    time.sleep(1)

    lcdfont = ImageFont.truetype(font1,16)
    for i in range(4):
        mylcd.lcddirection(i)
        pic = Image.open(pic2)
        display = ImageDraw.Draw(pic)
        display.rectangle((0,0,mylcd.width,20),fill="BLUE")
        display.rectangle((0,mylcd.height-20,mylcd.width,mylcd.height),fill="BLUE")
        display.text((35,2),"Rotation Display test", font=lcdfont,fill="WHITE") 
        display.text((59,mylcd.height-18),"www.lcdwiki.com", font=lcdfont,fill="WHITE")
        display.text((10,21),Direction[i], font=lcdfont,fill="RED")
        mylcd.lcdimage(pic)
        time.sleep(1)

    mylcd.lcddirection(USE_HORIZONTAL)

    lcdimage = Image.new("RGB", (mylcd.width, mylcd.height),"BLACK")
    mylcd.lcdimage(lcdimage)
    time.sleep(3)
