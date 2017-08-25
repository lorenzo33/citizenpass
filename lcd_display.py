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
LCD_EN  = 35
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
    def __init__(self):
	
	#Initialisation des variables
	self.rs = LCD_RS
	self.en = LCD_EN
	self.d4 = LCD_D4
	self.d5 = LCD_D5
	self.d6 = LCD_D6
	self.d7 = LCD_D7
	self.backlight = LED_ON

	GPIO.setmode(GPIO.BOARD)     # Use pin numbers 
	#Initialise les branches GPIO en sortie
	for pin in (self.rs,self.en,self.d4,self.d5,self.d6,self.d7,self.backlight):
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


    #Fonction qui affiche un message sur la première ligne
    def lcd_FirstLine(self,text,style):
    	self.lcd_byte(LCD_LINE_1, LCD_CMD)
	self.lcd_string(text, style)

    #Fonction qui affiche un message sur la 2ème ligne
    def lcd_SecondLine(self,text, style):
	self.lcd_byte(LCD_LINE_2, LCD_CMD)
	self.lcd_string(text, style)

    #Fonction qui traite les données envoyées
    def lcd_byte(self,bits, mode):
        # Send byte to data pins
	# bits = data
	# mode = True  for character
	# False for command

	GPIO.output(self.rs, mode) # RS

	# High bits
	GPIO.output(self.d4, False)
	GPIO.output(self.d5, False)
	GPIO.output(self.d6, False)
	GPIO.output(self.d7, False)
	
	if bits&0x10==0x10:
	    GPIO.output(self.d4, True)
	if bits&0x20==0x20:
	    GPIO.output(self.d5, True)
	if bits&0x40==0x40:
	    GPIO.output(self.d6, True)
	if bits&0x80==0x80:
	    GPIO.output(self.d7, True)

	# Toggle 'Enable' pin
	time.sleep(E_DELAY)    
	GPIO.output(self.en, True)  
	time.sleep(E_PULSE)
	GPIO.output(self.en, False)  
	time.sleep(E_DELAY)      

	# Low bits
	GPIO.output(self.d4, False)
	GPIO.output(self.d5, False)
	GPIO.output(self.d6, False)
	GPIO.output(self.d7, False)
	
	if bits&0x01==0x01:
	    GPIO.output(self.d4, True)
	if bits&0x02==0x02:
	    GPIO.output(self.d5, True)
	if bits&0x04==0x04:
	    GPIO.output(self.d6, True)
	if bits&0x08==0x08:
	    GPIO.output(self.d7, True)

	# Toggle 'Enable' pin
	time.sleep(E_DELAY)    
	GPIO.output(self.en, True)  
	time.sleep(E_PULSE)
	GPIO.output(self.en, False)  
	time.sleep(E_DELAY)
