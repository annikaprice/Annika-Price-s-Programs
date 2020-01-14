# This version of the CarCamera.py program is on Annika Price's school account which contains modifications
# to Mark Washington's original CarCamera.py program.

# It needs to be documented with specific comments.

'''
Written by Mark Washington and Annika Price
''' 


import sys

import RPi.GPIO as GPIO

import pygame

import pygame.camera

from lib import Adafruit_BME280, MCP3008



VOLT_PORT = 1

AMP_PORT = 3



pygame.init()

pygame.display.init()

pygame.camera.init()



resolution = (640, 480)  # Resolution for PiTFT screen

screen = pygame.display.set_mode(resolution, 0)

cam_list = pygame.camera.list_cameras()

overlay_font = pygame.font.SysFont(None, 30)



thermometer = Adafruit_BME280.BME280(t_mode=Adafruit_BME280.BME280_OSAMPLE_8,
                                     
				     p_mode=Adafruit_BME280.BME280_OSAMPLE_8,
                                     
				     h_mode=Adafruit_BME280.BME280_OSAMPLE_8)



amp_volt_sensor = MCP3008.MCP3008(clk=5, cs=19, miso=13, mosi=6)


cam = pygame.camera.Camera(cam_list[0], resolution)

cam.start()



while True:
    
	try:
        
		temperature = round(thermometer.read_temperature_f(), 1)
        
		amps = round(amp_volt_sensor.read_adc(AMP_PORT), 1)
        
		volts = round(amp_volt_sensor.read_adc(VOLT_PORT), 1)
    
	except:
        
		temperature = "Error"
        
		amps = "Error"
        
		volts = "Error"
    
    

image = cam.get_image()


# Print the read temperature, amperage, and voltage to the Raspberry Pi screen.
    
temperature_text = overlay_font.render("Temp  " + str(temperature), True, (255, 255, 255))
    
amperage_text = overlay_font.render("Amps: " + str(amps), True, (255, 255, 255))
    
voltage_text = overlay_font.render("Volt: " + str(volts), True, (255, 255, 255))

    

screen.blit(image, (0, 0))  # Blit image from camera to screen
    
screen.blit(temperature_text, (3, 420))  # Blit temperature to screen
    
screen.blit(amperage_text, (3, 440))
    
screen.blit(voltage_text, (3, 460))

    

pygame.display.update()



############################# button 17 on the side of the raspberry pi is the exit button###############################
GPIO.setmode(GPIO.BCM)





button_gpio = 17

GPIO.setup(button_gpio, GPIO.IN, pull_up_down = GPIO.PUD_UP)

exitButtonText = overlay_font.render("Press Button 17 to Exit Out Of Program CarCamera.py")

while True:
	
	if (GPIO.input(button_gpio) == 0):
		
		print "17 pressed"
		
		GPIO.cleanup()
				
		cam.stop()
		
		pygame.quit()
		
		sys.exit(0)




pygame.display.update()


########################################################################################################################    

for event in pygame.event.get():
        
	if event.type == pygame.QUIT:
	    
	cam.stop()
            
	pygame.quit()
            
	sys.exit()

    
	pygame.display.update()
