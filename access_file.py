# -*- coding: utf-8 -*-
import json
import borne
# module pour la lecture de l'adresse IP
import socket
import fcntl
import struct


class AccessFile(object):
    def __init__(self):
	self.access = False
	self.pathfile = "carte.json"
	self.data = " "
	self.IpBorne = self.GetIpAddress('eth0')
	print "Adresse ip borne : %s" % self.IpBorne
	self.ReadAccessFile()

    def GetIpAddress(self,ifname):
    	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    	return socket.inet_ntoa(fcntl.ioctl(
        	s.fileno(),
        	0x8915,  # SIOCGIFADDR
        	struct.pack('256s', ifname[:15])
    	)[20:24])

    # Fonction qui ouvre un fichier json et qui stocke les données
    def ReadAccessFile(self):
        try:
            with open(self.pathfile, 'r') as fic:
                self.data = fic.read()
	    fic.close()
        except :
            borne.Debug('Erreur de lecture du fichier')
            exit(1)

    # Fonction qui recherche la chaine passée en paramètre et retourne True
    # Si la chaine est trouvée
    def SearchCardId(self, CardTag):
	
	# On relit le fichier
	self.ReadAccessFile()
	
	# On initialise la variable
	self.access = False
	msg = " "

	# Lecture et chargement du fichier json
        series = json.loads(self.data)
        #print "code carte lue : %s" % CardTag

        for index, key in enumerate(series):
            card_code=series[index]["fields"]["code"]
            card_stat=series[index]["fields"]["statut"]
        
	    #borne.Debug(card_code)
	    #borne.Debug(card_stat)
	    #print "card_code lu : %s" % card_code
	    #print "card_stat lu : %s" % card_stat
	
	    if card_code==CardTag:
	        if card_stat == 1:
            	    #print "Carte(uid) :%s - valide : %s" % (card_code, card_stat)
	    	    #borne.Debug("AccessControl : uid carte (" + card_code + ") valide")
		    self.access = True
                else:
            	    #print "Carte(uid) :%s - non valide : %s" % (card_code, card_stat)
	    	    borne.Debug("AccesControl : uid carte (" + card_code + ") non valide")
		    self.access = False
	    else:
	        #print "Carte inconnue"
	        #borne.Debug("AccessControl : uid carte (" + card_code + ") inconnu")
		self.acces = False

        return self.access
