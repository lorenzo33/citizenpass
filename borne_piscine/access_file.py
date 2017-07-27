# -*- coding: utf-8 -*-
import json
import borne

class AccessFile(object):
    def __init__(self):
	self.access = False
	self.pathfile = "carte.json"
	self.data = " "
	self.ReadAccessFile()

    # Fonction qui ouvre un fichier json et qui stocke les données
    def ReadAccessFile(self):
        try:
            with open(self.pathfile, 'r') as fic:
                self.data = fic.read()
        except :
            borne.debug('Erreur de lecture du fichier')
            exit(1)

    # Fonction qui recherche la chaine passée en paramètre et retourne True
    # Si la chaine est trouvée
    def SearchCardId(self, CardTag):

	# On initialise la variable
	self.access = False
	msg = " "

	# Lecture et chargement du fichier json
        series = json.loads(self.data)
        #print "code carte lue : %s" % CardTag

        for index, key in enumerate(series):
            card_code=series[index]["fields"]["code"]
            card_stat=series[index]["fields"]["statut"]
        
	    borne.debug(card_code)
	    borne.debug(card_stat)
	    #print "card_code lu : %s" % card_code
	    #print "card_stat lu : %s" % card_stat
	
	    if card_code==CardTag:
	        if card_stat == 1:
            	    #print "Carte(uid) :%s - valide : %s" % (card_code, card_stat)
	    	    msg = "Carte(uid)" + card_code + " - valide"
		    borne.debug(msg)
		    self.access = True
                else:
            	    #print "Carte(uid) :%s - non valide : %s" % (card_code, card_stat)
	    	    msg = "Carte(uid)" + card_code + " - non valide"
		    borne.debug(msg)
		    self.access = False
	    else:
	        #print "Carte inconnue"
	        borne.debug("carte inconue")
		self.acces = False

        return self.access
