# -*- coding: utf8 -*-
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
import time

import RPi.GPIO as GPIO

# Initialisation des variables
DEBUG = True
VERBOSE = True

if(DEBUG):
    logging.basicConfig(format='%(asctime)s %(message)s', filename='borne.log', level=logging.DEBUG)

def debug(message):
    logging.debug(message)

def onScreen(message):
    if(VERBOSE):
        print(message)

def printDateToDisplay():
    while True:
        if displayTime!=True:
            thread.exit()
        display.lcdWriteFirstLine(time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
        time.sleep(1)
	display.lcdWriteFirstLine(" ")

def init_Gpio():
    GPIO.setmode(GPIO.BOARD)

def main():

    global displayTime
    displayTime = True
    
    GPIO.setwarnings(False)
    GPIO.cleanup()
    
    try: 
        init_Gpio()
        display.lcd_init()
        thr = thread.start_new_thread(printDateToDisplay, ())
	
	#Boucle qui lit et affiche les actions
	while True:
	    #display.lcdWriteSecondLine("En attente carte")
            cardId=nfc.ReadNfc()
	    #display.lcdWriteSecondLine(cardId)
  	    logging.info("carte lue %s\n", cardId)
     
    except KeyboardInterrupt:
        GPIO.cleanup()
	pass
    GPIO.cleanup()
    displayTime=False

if __name__ == "__main__":
    main()
