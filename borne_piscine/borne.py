# -*- coding: utf-8 -*-
#!/usr/bin/python

#-------------------------------------------------------------------------------
# Nom :        Borne
# Objet:       Programme de lecture des cartes RFID et d'affichage des accès 
#
# Auteur:      Laurent DELAPLACE
#
# Creation:    18/07/2017
# Copyright:   (c) ACIFOP 2017
# Licence:
#-------------------------------------------------------------------------------

# Définition des données à importer
import display
import nfc
import logging

import thread
import threading
import time

import RPi.GPIO as GPIO

class Borne(threadin.Thread):

    # Initialisation des variables
    DEBUG = True
    VERBOSE = True

    if(self.DEBUG):
        logging.basicConfig(format='%(asctime)s %(message)s', filename='borne.log', level=logging.DEBUG)

    def __init__(self):

    	global displayTime, Message
    	self.displayTime = True
	self.lcd = display.LcdDisplay() 	    




def debug(message):
        logging.debug(message)

    def onScreen(message):
        if(VERBOSE):
            print(message)

    def printDateToDisplay():
        while True:
            if displayTime!=True:
                thread.exit()
        	lcd.lcdWriteFirstLine(time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
		lcd.lcdWriteSecondLine(Message)
        	time.sleep(1)
		lcd.Clear()

    def init_Gpio():
        GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False)
    	GPIO.cleanup()

    def main():


    	try: 
            init_Gpio()
            #display.lcd_init()
            lcd =  display.LcdDisplay()
	    thr = thread.start_new_thread(printDateToDisplay, ())
	    Message = "Attente carte"	

	    #Boucle qui lit et affiche les actions
	    while True:
	        cardId=nfc.ReadNfc()
	        Message = "Carte Lue"
  	        logging.info("carte lue %s\n", cardId)
     
        except KeyboardInterrupt:
            GPIO.cleanup()
	    pass
        GPIO.cleanup()
    	displayTime=False

if __name__ == "__main__":
    main()
