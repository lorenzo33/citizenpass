# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Nom :        Lecteur RFID
# Objectif:    Code qui permet l'accès au lecteur RFID	
#
# Auteur:      Laurent DELAPLACE
#
# Creation:    18/07/2017
# Copyright:   (c) ACIFOP 2017
# Licence:
#-------------------------------------------------------------------------------
import MFRC522
import time

def ReadNfc():
    reading = True
    
    #Boucle qui lit les cartes présentées
    while reading:
	#On instancie la classe MFRC522
        MIFAREReader = MFRC522.MFRC522()

        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
	if status == MIFAREReader.MI_OK:
	    print "Carte Présentée"
	time.sleep(1)
	
	(status,backData) = MIFAREReader.MFRC522_Anticoll()
	if status == MIFAREReader.MI_OK:
	    MIFAREReader.AntennaOff()
	    reading = False
	    return str(backData[0])+str(backData[1])+str(backData[2])+str(backData[3])+str(backData[4])
