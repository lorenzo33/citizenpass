# -*- coding:utf8 -*- 
import MFRC522 
import signal
from lxml import etree

#Définition des variables globales
continue_reading = True
wait_msg = "En attente présentation carte"
MIFAREReader = MFRC522.MFRC522()
cardA = [224,45,27,27,205]
cardB = [102,169,174,187,218]
cardC = [176,175,148,162,41]
file_access = "liste.xml"

############################################
# Fonction qui arrête la boucle de lecture #
# et qui réinitialise la carte MFRC522     #
############################################
def end_read(signal, frame):
    global continue_reading
    continue_reading = False
    print "Ctrl+C pour quitter la lecture."
    MIFAREReader.GPIO_CLEAN()

###############################################
# Fonction pour la lecture du fichier d'accès #
###############################################
def read_file(file_path):
    print "Chargement du fichier d'accès"
    tree = etree.parse(file_path)
    for card in tree.xpath("/cards/card"):
        print(card.get("uid"))

signal.signal(signal.SIGINT, end_read)

read_file(file_access)
print "%s" % wait_msg

while continue_reading:
  (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
  if status == MIFAREReader.MI_OK:
      print "Carte presentée"
  (status,backData) = MIFAREReader.MFRC522_Anticoll()
  if status == MIFAREReader.MI_OK:
      print "Card read UID: "+str(backData[0])+","+str(backData[1])+","+str(backData[2])+","+str(backData[3])+","+str(backData[4])
      if  backData == cardA:
          print "Carte Blanche" 
      elif backData == cardB:
          print "Badge bleu"
      elif backData == cardC:
          print "Piscine Pessac"
      else:
          print "Carte inconnue"
      print "%s" % wait_msg

