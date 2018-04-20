#!/usr/bin/python3

import socket
import sys


ip = input("Saississez l'adresse IP du Serveur:  ")
port = input("Saississez le port du port :   ")
try :
    port = int(port)
except:
    print("Saississez un entier..")
    sys.exit()
params = (ip, port)
BUFFER_SIZE = 8192 # default
# try:
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# except:
#     print("Pas de réponse du serveur.\n")
#     sys.exit()

#ENVOIE DU MESSAGE HELLO AU SERVEUR

s.sendto(b"HELLO\n", params)
data, _ = s.recvfrom(BUFFER_SIZE)
print('\tDonnée récupérée du serveur : %s' % data.strip())

s.close()
