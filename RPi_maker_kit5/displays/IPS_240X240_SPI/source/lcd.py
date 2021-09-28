#This program is for learning only,Not to be used for any other purpose 
#without the permission of the author
#Testing Hardware:Raspberry PI all series
#QDtech-LCD liquid crystal driver for Raspberry PI
#xiaofeng@ShenZhen QDtech co.,LTD
#Company Website:www.qdtft.com
#Taobao Website:http://qdtech.taobao.com
#wiki Technology Website:http://www.lcdwiki.com
#We provide technical support,Any technical questions are welcome to 
#exchange and study at any time
#Fixed telephone (fax):+86 0755-23594567 
#cell-phone:15989313508(Mr Feng)
#E-mail:lcdwiki01@gmail.com    support@lcdwiki.com    goodtft@163.com
#Technical Support QQ:3002773612  3002778157
#Technical Exchange QQ group:324828016
#Date:2021/4/6
#Version:V1.0
#Copyright reserved, piracy must be investigated
#Copyright(C) ShenZhen QDtech co.,LTD 2018-2028
#All rights reserved
#****************************************************************************************************
#This program uses the bcm2835 gpio library,
#so the pin definition using BCM coding
#This is python program
#=====================================power supply wiring===========================================//
# OLED Module                Raspberry PI    
#    VCC        connect       DC 3.3V         //OLED power positive, Physical pin 1,17
#    GND        connect          GND          //OLED power ground,Physical pin 6,9,14,20,25,30,34,39
#======================================data line wiring=============================================//
#The default data bus type for this module is 4-wire SPI
# OLED Module                Raspberry PI 
#    SDA        connect       19(bcm:10)      //OLED spi write signal
#======================================control line wiring==========================================//
# OLED Module                Raspberry PI 
#    RES        connect        5(bcm:3)       //OLED reset control signal
#    DC         connect        3(bcm:2)       //OLED data or command selection control signal
#    SCL        connect       23(bcm:11)      //OLED spi colck signal
#    BLK        connect       12(bcm:18)      //LCD backlight control signal, if no control is needed, connect to 3.3V
#========================================touch screen wiring========================================//
#This module has no touch function,so it don't need touch screen wiring
#*****************************************************************************************************/	
#/****************************************************************************************************
#  * @attention
#  *
#  * THE PRESENT FIRMWARE WHICH IS FOR GUIDANCE ONLY AIMS AT PROVIDING CUSTOMERS
#  * WITH CODING INFORMATION REGARDING THEIR PRODUCTS IN ORDER FOR THEM TO SAVE
#  * TIME. AS A RESULT, QD electronic SHALL NOT BE HELD LIABLE FOR ANY
#  * DIRECT, INDIRECT OR CONSEQUENTIAL DAMAGES WITH RESPECT TO ANY CLAIMS ARISING
#  * FROM THE CONTENT OF SUCH FIRMWARE AND/OR THE USE MADE BY CUSTOMERS OF THE
#  * CODING INFORMATION CONTAINED HEREIN IN CONNECTION WITH THEIR PRODUCTS.
#*****************************************************************************************************/
import lcd_spi
import RPi.GPIO as GPIO
import time
import numpy as np

"""Define the size of the LCD"""
LCD_W = 240
LCD_H = 240

USE_HORIZONTAL=0 #Define the clockwise rotation direction of LCD screen:
                 #// 0-0 degree rotation, 1-90 degree rotation, 2-180 degree rotation, 3-270 degree rotation

# Initialize spi
myspi = lcd_spi.lcdspi()

class ST7789V(object):
    """class for ST7789V 240*240 1.3inch IPS SPI LCD module."""
    def __init__(self,res,dc,blk):
        # set lcd display parameter
        self.width = 0 #LCD width
        self.height = 0 #LCD height
        self.lcdid = 0  #LCD ID
        self.lcddir = 0 #LCD display direction
        self.wramcmd = 0x2C #Start writing gram instruction
        self.setxcmd = 0x2A #Set X coordinate command
        self.setycmd = 0x2B #Set Y coordinate command
        self.setdircmd = 0x36 #Set lcd display direction command
        self.xoffset = 0 #Set X coordinate offset
        self.yoffset = 0  #Set Y coordinate offset
        # Initialize oled pin
        self.lcdled = blk
        self.lcdrs = dc
        self.lcdrst = res
    def lcdledset(self):
        GPIO.output(self.lcdled,GPIO.HIGH)
    def lcdledclr(self):
        GPIO.output(self.lcdled,GPIO.LOW)
    def lcdrsset(self):
        GPIO.output(self.lcdrs,GPIO.HIGH)
    def lcdrsclr(self):
        GPIO.output(self.lcdrs,GPIO.LOW)
    def lcdrstset(self):
        GPIO.output(self.lcdrst,GPIO.HIGH)
    def lcdrstclr(self):
        GPIO.output(self.lcdrst,GPIO.LOW)
    def lcdwrreg(self,value):
        self.lcdrsclr()
        myspi.spiwritebyte(value)
    def lcdwrdata(self,value):
        self.lcdrsset()
        myspi.spiwritebyte(value)
    def lcdwritereg(self,reg,value):
        self.lcdwrreg(reg)
        self.lcdwrdata(value)
    def lcdwriteram(self):
        self.lcdwrreg(self.wramcmd)
    def lcdwrite16bitdata(self,value):
        self.lcdrsset()
        myspi.spiwritebyte(value>>8)
        myspi.spiwritebyte(value)
    def lcdsetwindows(self,xstart,ystart,xend,yend):
        self.lcdwrreg(self.setxcmd)
        self.lcdwrdata((xstart+self.xoffset)>>8)
        self.lcdwrdata(xstart+self.xoffset)
        self.lcdwrdata((xend+self.xoffset)>>8)
        self.lcdwrdata(xend+self.xoffset)
        self.lcdwrreg(self.setycmd)
        self.lcdwrdata((ystart+self.yoffset)>>8)
        self.lcdwrdata(ystart+self.yoffset)
        self.lcdwrdata((yend+self.yoffset)>>8)
        self.lcdwrdata(yend+self.yoffset)
        self.lcdwriteram()
    def lcdsetcursor(self,xpos,ypos):
        self.lcdsetwindows(xpos,ypos,xpos,ypos)
    def lcddrawpoint(self,x,y,color):
        self.lcdsetcursor(x,y)
        self.lcdwrite16bitdata(color)
    def lcdclear(self,color):
        self.lcdsetwindows(0,0,self.width-1,self.height-1)
        self.lcdrsset()
        for i in range(0,self.height):
            for m in range(0,self.width):
                myspi.spiwritebyte(color>>8)
                myspi.spiwritebyte(color)
    def lcdgpioinit(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.lcdled,GPIO.OUT)
        GPIO.setup(self.lcdrs,GPIO.OUT)
        GPIO.setup(self.lcdrst,GPIO.OUT)
    def lcdreset(self):
        self.lcdrstclr()
        time.sleep(0.02)
        self.lcdrstset()
        time.sleep(0.02)
    def lcddirection(self,value):
        if value == 0:
            self.width = LCD_W
            self.height = LCD_H
            self.xoffset = 0
            self.yoffset = 0
            self.lcdwritereg(self.setdircmd,0)
        elif value == 1:
            self.width = LCD_H
            self.height = LCD_W
            self.xoffset = 0
            self.yoffset = 0   
            self.lcdwritereg(self.setdircmd,(1 << 6)|(1 << 5))
        elif value == 2:
            self.width = LCD_W
            self.height = LCD_H
            self.xoffset = 0
            self.yoffset = 80      
            self.lcdwritereg(self.setdircmd,(1 << 6)|(1 << 7))
        elif value == 3:
            self.width = LCD_H
            self.height = LCD_W
            self.xoffset = 80
            self.yoffset = 0        
            self.lcdwritereg(self.setdircmd,(1 << 5)|(1 << 7))
        else:
            raise ValueError('direction value must be 0~3')
    def lcdinit(self):
        self.lcdgpioinit() #LCD GPIO initialization
        self.lcdreset()    #LCD reset
        """init ST7789V"""        
        self.lcdwrreg(0x36); 
        self.lcdwrdata(0x00);
        self.lcdwrreg(0x3A); 
        self.lcdwrdata(0x05);
        self.lcdwrreg(0xB2);
        self.lcdwrdata(0x0C);
        self.lcdwrdata(0x0C);
        self.lcdwrdata(0x00);
        self.lcdwrdata(0x33);
        self.lcdwrdata(0x33);
        self.lcdwrreg(0xB7); 
        self.lcdwrdata(0x35);  
        self.lcdwrreg(0xBB);
        self.lcdwrdata(0x19);
        self.lcdwrreg(0xC0);
        self.lcdwrdata(0x2C);
        self.lcdwrreg(0xC2);
        self.lcdwrdata(0x01);
        self.lcdwrreg(0xC3);
        self.lcdwrdata(0x12);   
        self.lcdwrreg(0xC4);
        self.lcdwrdata(0x20);  
        self.lcdwrreg(0xC6); 
        self.lcdwrdata(0x0F);    
        self.lcdwrreg(0xD0); 
        self.lcdwrdata(0xA4);
        self.lcdwrdata(0xA1);
        self.lcdwrreg(0xE0);
        self.lcdwrdata(0xD0);
        self.lcdwrdata(0x04);
        self.lcdwrdata(0x0D);
        self.lcdwrdata(0x11);
        self.lcdwrdata(0x13);
        self.lcdwrdata(0x2B);
        self.lcdwrdata(0x3F);
        self.lcdwrdata(0x54);
        self.lcdwrdata(0x4C);
        self.lcdwrdata(0x18);
        self.lcdwrdata(0x0D);
        self.lcdwrdata(0x0B);
        self.lcdwrdata(0x1F);
        self.lcdwrdata(0x23);
        self.lcdwrreg(0xE1);
        self.lcdwrdata(0xD0);
        self.lcdwrdata(0x04);
        self.lcdwrdata(0x0C);
        self.lcdwrdata(0x11);
        self.lcdwrdata(0x13);
        self.lcdwrdata(0x2C);
        self.lcdwrdata(0x3F);
        self.lcdwrdata(0x44);
        self.lcdwrdata(0x51);
        self.lcdwrdata(0x2F);
        self.lcdwrdata(0x1F);
        self.lcdwrdata(0x1F);
        self.lcdwrdata(0x20);
        self.lcdwrdata(0x23);
        self.lcdwrreg(0x21); 
        self.lcdwrreg(0x11); 
        self.lcdwrreg(0x29); 
        self.lcddirection(USE_HORIZONTAL)
        self.lcdledset()
        #self.lcdclear(0xFFFF)
    def lcdimage(self,image):
        """set the value of Python Image Library to lcd GRAM"""
        imgwidth,imgheight = image.size
        if imgwidth != self.width or imgheight != self.height:
            raise ValueError('Image must be same dimensions as display({0}x{1}).' .format(self.width, self.height))
        img = np.asarray(image)
        pix = np.zeros((self.width,self.height,2), dtype = np.uint8)
        pix[...,[0]] = np.add(np.bitwise_and(img[...,[0]],0xF8),np.right_shift(img[...,[1]],5))
        pix[...,[1]] = np.add(np.bitwise_and(np.left_shift(img[...,[1]],3),0xE0),np.right_shift(img[...,[2]],3))
        pix = pix.flatten().tolist()
        self.lcdsetwindows(0,0,imgwidth-1,imgheight-1)
        self.lcdrsset()
        for i in range(0,len(pix),4096):
            myspi.spi.writebytes(pix[i:i+4096])	
