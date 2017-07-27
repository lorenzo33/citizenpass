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

#Activation des logs de débuggage
DEBUG=True
#Activation de l'affichage standard
VERBOSE=False

if(DEBUG):
    logging.basicConfig(format='%(asctime)s %(message)s',filename='borne.log', level=logging.DEBUG)

def debug(message):
    logging.debug(message)

def onScreen(message):
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

def Main():
    
    try:
	#Création d'une instance pour gérer la lecture du fichier d'accès
    	fichier = access_file.AccessFile()
    	
	#Boucle de lecture
	while True:
    	    cardId = ReadNFC()
	    debug("Carte lue : " + cardId) 
            
	    test = fichier.SearchCardId(cardId)
            if test == True:
        	print "Accès Autorisé"
		debug("Carte autorisée : " + cardId)
    	    else:
        	print "Non autorisé"
		debug("Carte refusée :" + cardId)
	    time.sleep(2)

    except KeyboardInterrupt:
        #GPIO.cleanup()
        pass
    GPIO.cleanup()

if __name__ == '__main__':
    Main()
