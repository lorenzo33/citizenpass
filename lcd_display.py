# -*- coding:utf-8 -*-
#!/usr/bin/python
#
# HD44780 LCD 
# Raspberry Pi
#
# Author : Laurent DELAPLACE
# 
# Date   : 17/08/2017
#

#importation des modules
import RPi.GPIO as GPIO
import time

# Definition des constantes pour la connexion GPIO => LCD 
LCD_RS = 37
LCD_E  = 35
LCD_D4 = 33 
LCD_D5 = 31
LCD_D6 = 29
LCD_D7 = 32
LED_ON = 15

#Constantes pour l'affichage
LCD_WIDTH = 16    
LCD_CHR = True   #Mode Affichage
LCD_CMD = False  #Mode Commande

LCD_LINE_1 = 0x80 # Adresse RAM pour 1ere ligne du LCD
LCD_LINE_2 = 0xC0 # Adresse RAM pour 2eme ligne du LCD 

#Constantes pour le temps
E_PULSE = 0.00005
E_DELAY = 0.00005

###################################################################
# Déclaration de la classe lcd pour la gestion de l'afficheur
###################################################################
class lcd(object):
    def __init__(self,rs,en,d4,d5,d6,d7,backlight):
	
	#Initialisation des variables
	self._rs = rs
	self._en = en
	self._d4 = d4
	self._d5 = d5
	self._d6 = d6
	self._d7 = d7
	self._backlight = backlight

	GPIO.setmode(GPIO.BOARD)     # Use pin numbers 
	
	#Initialise les branches GPIO en sortie
	for pin in (rs,en,d4,d5,d6,d7,backlight):
	    GPIO.setup(pin, GPIO.OUT)
	self.lcd_clear()

    #Fonction d'initialisation de l'affichage
    def lcd_clear(self):
  	self.lcd_byte(0x33,LCD_CMD)
  	self.lcd_byte(0x32,LCD_CMD)
  	self.lcd_byte(0x28,LCD_CMD)
  	self.lcd_byte(0x0C,LCD_CMD)
  	self.lcd_byte(0x06,LCD_CMD)
  	self.lcd_byte(0x01,LCD_CMD)


    #Fonction d'affichage d'un message sur l'afficheur
    def lcd_string(self,message,style):
	# style=1 Left justified
    	if style==1:
	    message = message.ljust(LCD_WIDTH," ")  

	# style=2 Centred
	elif style==2:
	    message = message.center(LCD_WIDTH," ")

	# style=3 Right justified
	elif style==3:
	    message = message.rjust(LCD_WIDTH," ")

	for i in range(LCD_WIDTH):
    	    self.lcd_byte(ord(message[i]),LCD_CHR)

    #Fonction qui traite les données envoyées
    def lcd_byte(self,bits, mode):
        # Send byte to data pins
	# bits = data
	# mode = True  for character
	# False for command

	GPIO.output(self._rs, mode) # RS

	# High bits
	GPIO.output(self._d4, False)
	GPIO.output(self._d5, False)
	GPIO.output(self._d6, False)
	GPIO.output(self._d7, False)
	
	if bits&0x10==0x10:
	    GPIO.output(self._d4, True)
	if bits&0x20==0x20:
	    GPIO.output(self._d5, True)
	if bits&0x40==0x40:
	    GPIO.output(self._d6, True)
	if bits&0x80==0x80:
	    GPIO.output(self._d7, True)

	# Toggle 'Enable' pin
	time.sleep(E_DELAY)    
	GPIO.output(self._en, True)  
	time.sleep(E_PULSE)
	GPIO.output(self._en, False)  
	time.sleep(E_DELAY)      

	# Low bits
	GPIO.output(self._d4, False)
	GPIO.output(self._d5, False)
	GPIO.output(self._d6, False)
	GPIO.output(self._d7, False)
	
	if bits&0x01==0x01:
	    GPIO.output(self._d4, True)
	if bits&0x02==0x02:
	    GPIO.output(self._d5, True)
	if bits&0x04==0x04:
	    GPIO.output(self._d6, True)
	if bits&0x08==0x08:
	    GPIO.output(self._d7, True)

	# Toggle 'Enable' pin
	time.sleep(E_DELAY)    
	GPIO.output(self._en, True)  
	time.sleep(E_PULSE)
	GPIO.output(self._en, False)  
	time.sleep(E_DELAY)
