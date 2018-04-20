#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Exemple de serveur UDP utilisant socketserver
"""


__author__ = "Sébastien CHAZALLET"
__copyright__ = "Copyright 2012"
__credits__ = ["Sébastien CHAZALLET", "InsPyration.org", "Éditions ENI"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Sébastien CHAZALLET"
__email__ = "sebastien.chazallet@laposte.net"
__status__ = "Production"


import socketserver

params = ('127.0.0.1', 8808)

donnees = []


class ExampleUDPHandler(socketserver.DatagramRequestHandler):
	def handle(self):
		data = self.rfile.readline().strip()
		print('>>> Reçu: %s', data)
		if not data:
			conn.close()

		elif data != b"HELLO":
			print("Mauvais mot HELLO")
			self.server_close()
            conn.close()

		else:
			print("Pas de valeurs")
			self.wfile.write("Pas de valeurs.")
	self.wfile.write(data.strip() + b".\n")


if __name__ == '__main__':
    print("IP SERVEUR : %s, PORT DU SERVEUR : %s" % (params[0],params[1]))
    server = socketserver.UDPServer(params, ExampleUDPHandler)
    server.serve_forever()
