*********************************************************************************
RPi_maker_pcb_readme.txt - version control details for the Raspberry Pi Maker PCB
*********************************************************************************

required components version 2.0 September 2024
----------------------------------------------
  required components for use with the v5.0 PCB are listed in the RPi_PCB5_usage_documentation_v2-1.pdf
  and RPi_maker_pcb_getting_started_v2-0.pdf documents
 
  
  please note:
  ------------
  all electronic and electrical components need to be carefully recycled 
  but we would much prefer for you to pass this equipemnt on to another 
  user if you have no further use for it. 

*******************************************************************	
software & documentation version 2.0  September 2024
-------------------------------------------------------------------
  description: updated version with content to support usage with Raspberry Pi SBCs using the Bookworm OS 


  ** documentation ** 
    RPi_maker_pcb_readme.txt - this document which is updated whenever a new version is released
    RPi_maker_pcb_getting_started_v2-0.pdf - Raspberry Pi Maker PCB getting started leaflet v2.0 September 2024
    RPi_PCB5_usage_documentation_v2-1.pdf - Raspberry Pi Maker PCB detailed usage documentation v2.1 September 2024


  ** Scratch, Python and other software files **
  
  * Raspberry Pi single board computer (SBC) code:
  
  electronic basics
  -----------------
  Scratch 1.4 - LED_button_buzzer.sb
              - LED_button_flash.sb
			  - LED_flash.sb
			  - LED_red_green_flash.sb
			  - LED_RGB_flash.sb
  Scratch 2   - LED_button_buzzer.sb2
              - LED_button_flash.sb2
			  - LED_flash.sb2
			  - LED_red_green_flash.sb2 
			  - LED_RGB_flash.sb2
  Scratch 3   - LED_button_buzzer.sb3
              - LED_button_flash.sb3
			  - LED_flash.sb3
			  - LED_red_green_flash.sb3 
			  - LED_RGB_flash.sb3
  Python - LED_flash.py
	     - LED_red_green_flash.py
		 - LED_red_amber_green_flash.py
	     - LED_button_flash.py
	     - LED_button_buzzer.py
		 - buzzer_player.py
  web code      - LED1_flash_web.py
  web css       - normalize_advanced.css	
                - skeleton_advanced.css
  web images    - favicon.png
                - RPi_kits_PCB05_20210419_160549156_900w.jpg
			    - RPi_kits_PCB05_front_image01.png
  web templates - electronics_header_insert.html
                - electronics_layout.html
				- electronics_select_mode1.html
				- led1_setup_mode.html
				- run_led1.html

  image taking
  ------------
  Python - button_led_take_image.py
         - button_led_take_video.py
		 - button_take_image.py
	     - button_take_video.py
		 - button_timer_take_image.py
		 - button_timer_take_video.py
		 - PIR_take_image.py
		 - sort_number_symlink_files.py
		 - timelapse_cron_take_annotated_image.py
		 - timelapse_cron_take_image.py
  web code      - image_camera_usb_opencv_annotate.py
                - image_streaming_app_root_annotate.py
				- image_streaming_app_user_annotate.py
  web css       - normalize_advanced.css	
                - skeleton_advanced.css
  web images    - favicon.png
                - Starter_kit_PCB01_20210518_132528401_900w.jpg
			    - Starter_kit_PCB01_front_image.png
  web templates - cam_options_setup.html
                - cam_setup_mode.html
				- header_insert.html
				- layout.html
				- select_mode.html
				- stream_video_mode.html
  
  displays
  --------
  Python - code for IPS_240X240_SPI display
         - code for IPS_80x160_SPI display
		 - code for LCD_1602_i2c display
		 - code for MAX7219_7segment_LED display
		 - code for OLED_128x64_I2C display
		 - code for TM1637_7segment_LED display
    
  motor control
  -------------
  Python - code for drive motor control
         - code for servo motor control
		 - code for stepper motor control
  web code - web front end code for motor control
  
  RF_communication
  ----------------
  Python - code for C218D001C + FS1000A communications
         - code for RXB8 communications
		 - code for SRX882 + STX882 communications
  
  sensors
  -------
  Python - code for light sensor data capture
         - code for magnetic sensor data capture
		 - code for MPR121 touch sensor data capture
		 - code for object_detection sensor data capture
		 - code for pressure sensor data capture
		 - code for temperature sensor data capture
		 - code for TTP229 touch keypad data capture

  
copyright 2021-2024 Geoff Brickell
