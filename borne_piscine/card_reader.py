# -*- coding:utf8 -*- 

###################################################################
#
# Nom du fichier : card_reader.py
#
# Contenu : contient le programme qui lit les codes des cartes
#
# Developpeur : DELAPLACE Laurent 
#
# Date de création : 26/07/2017
#
###################################################################

import MFRC522 
import signal
import time 

class CardReader(object):
    def __init__(self):
	#Définition des variables globales
	self.reading = True
	self.wait_msg = "En attente présentation carte"
	self.MIFAREReader = MFRC522.MFRC522()

    def Exit(self):
	self.MIFAREReader.GPIO_CLEAN()

    # Fonction qui attend la présentation d'une carte, lit le code et le renvoie
    def Read(self):
	while self.reading:
  	    #Fonction qui test si une carte est présente
	    (status,TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
  
  	    if status == MIFAREReader.MI_OK:
  	        print "Carte presentée"
  	    
	    #Fonction qui récupère le tag de la carte présente
            (status,backData) = MIFAREReader.MFRC522_Anticoll()
  	    if status == MIFAREReader.MI_OK:
      	        print "Card read UID: "+str(backData[0])+","+str(backData[1])+","+str(backData[2])+","+str(backData[3])+","+str(backData[4])
	        return bckData
