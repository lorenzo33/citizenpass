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
import lcd_display
import configparser
import time
import logging
import RPi.GPIO as GPIO

#Activation des logs de débuggage
DEBUG=True
#Activation de l'affichage standard
VERBOSE=False

# Broche pour l'affichage
LED_GREEN = 36
LED_RED = 38
LED_BLUE = 40

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

def ReadConfigFile():
    fichier = 'config.ini'

    #Création d'une instance de la classe
    config = configparser.ConfigParser()
    config.read(fichier)

    #Boucle qui parcourt les sections
    for section in config.sections():
        #Boucle qui parcourt les clés
	for key in config[section]:
	    if section == 'borne':
		if key == 'adresse_ip':
		    valeur = config[section][key]
		    return valeur
    
def InitGpio():
    #Initialisation du mode de fonctionnement du circuit GPIO
    GPIO.setmode(GPIO.BOARD)
    #Initialisation des variables
    GPIO.setup(LED_GREEN, GPIO.OUT)
    GPIO.PWM(LED_GREEN, 10)
    GPIO.setup(LED_GREEN, False)

    GPIO.setup(LED_RED, GPIO.OUT)
    GPIO.PWM(LED_RED, 10)
    GPIO.setup(LED_RED, False)

    GPIO.setup(LED_BLUE, GPIO.OUT)
    GPIO.PWM(LED_BLUE, 10)
    GPIO.setup(LED_BLUE, False)

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

	#Initialisation de l'afficheur
	afficheur = lcd_display.lcd()

	#Obtention de l'adresse IP
	time.sleep(2)
	addip = fichier.GetIpAddress('eth0')
	print "Adresse IP (eth0) : %s" % addip
        Debug("GetIpAddresse : %s" % addip)

	#On récupère l'adresse ip du fichier de config
	ip_borne = ReadConfigFile()
        print "Adresse IP (ini) : %s" % ip_borne
	Debug("ReadConfigFile : %s" % ip_borne)

	#Affichage de l'ip
	if str(addip) == ip_borne:
	    GPIO.PWM(LED_BLUE, 10)
	    GPIO.output(LED_BLUE, True)
	    	
	#Boucle de lecture
	while True:

    	    cardId = ReadNFC()
	    Debug("ReadNFC : lecture carte, uid (" + cardId + ")") 
            
	    test = fichier.SearchCardId(cardId)
            if test == True:
	        print "Accès Autorisé"
		Debug("Borne : carte autorisée, uid (" + cardId + ")")
		LedBlink('green')
		afficheur.lcd_string("PASS : AUTORISE", 2)
    	    else:
        	print "Non autorisé"
		Debug("Borne : carte non autorisée/inconnue, uid (" + cardId + ")")
		LedBlink('red')
		afficheur.lcd_string("PASS : INTERDIT", 2)
	    time.sleep(1)
	    afficheur.lcd_clear()

    except KeyboardInterrupt:
        Debug("KeyboardInterrupt : arrêt ctrl+c")
	#GPIO.cleanup()
        pass
    GPIO.cleanup()
    Debug("GPIO.cleanup : réinitialisation du GPIO") 

if __name__ == '__main__':
    Main()
