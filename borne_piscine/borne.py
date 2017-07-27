# -*- coding:utf-8 -*-

###################################################################
#
# Nom du fichier : borne.py
#
# Contenu : contient le programme principal pour gérer les bornes
# d'accès au service
#
# Developpeur : DELAPLACE Laurent 
#
# Date de création : 26/07/2017
#
###################################################################

# Importation des modules
#from access_file import AccessFile
from MFRC522 import *
import access_file
import time
import logging
import RPi.GPIO as GPIO

#Activation des logs de débuggage
DEBUG=True
#Activation de l'affichage standard
VERBOSE=False

# Broche pour l'affichage
LED_GREEN = 38
LED_RED = 40

if(DEBUG):
    logging.basicConfig(format='%(asctime)s %(message)s',filename='borne.log', level=logging.DEBUG)

def Debug(message):
    logging.debug(message)

def OnScreen(message):
    if(VERBOSE):
        print(message)

def ReadNFC():
    reading = True
    while reading:
	#Création d'une instance pour la lecture
        MIFAREReader = MFRC522()

        #Détection de la présence d'une carte
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        #if status == MIFAREReader.MI_OK:
        #    print("Card detected")
        (status,backData) = MIFAREReader.MFRC522_Anticoll()

        if status == MIFAREReader.MI_OK:
            #print ("Card Number: "+str(backData[0])+","+str(backData[1])+","+str(backData[2])+","+str(backData[3])+","+str(backData[4]))
            MIFAREReader.AntennaOff()
            reading=False
            return str(backData[0])+str(backData[1])+str(backData[2])+str(backData[3])+str(backData[4])

def InitGpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_GREEN, GPIO.OUT)
    GPIO.setup(LED_RED, GPIO.OUT)

def LedBlink(led_color):
    if led_color == 'red':
        GPIO.output(LED_RED, True)
	time.sleep(2)
	GPIO.output(LED_RED, False)
    if led_color == 'green':
	GPIO.output(LED_GREEN, True)
	time.sleep(2)
	GPIO.output(LED_GREEN, False)

def Main():
    
    try:
	#Création d'une instance pour gérer la lecture du fichier d'accès
    	fichier = access_file.AccessFile()
	
	#Initialisation des entrées/sorties du raspberry
	InitGpio()
	    	
	#Boucle de lecture
	while True:
    	    cardId = ReadNFC()
	    Debug("ReadNFC : lecture carte, uid (" + cardId + ")") 
            
	    test = fichier.SearchCardId(cardId)
            if test == True:
        	print "Accès Autorisé"
		Debug("Borne : carte autorisée, uid (" + cardId + ")")
		LedBlink('green')
    	    else:
        	print "Non autorisé"
		Debug("Borne : carte non autorisée/inconnue, uid (" + cardId + ")")
		LedBlink('red')
	    time.sleep(1)

    except KeyboardInterrupt:
        #GPIO.cleanup()
        pass
    GPIO.cleanup()

if __name__ == '__main__':
    Main()
