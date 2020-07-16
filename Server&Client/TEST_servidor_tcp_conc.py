#!/usr/bin/env python3

#TESTS SERVER

import socket, os, signal

PORT = 50003
CODIFICATION = "UTF-8"

s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

s.bind( ('', PORT) )
s.listen( 5 )

signal.signal(signal.SIGCHLD, signal.SIG_IGN)

while True:
	dialogo, dir_cli = s.accept()
	print( "Cliente conectado desde {}:{}.".format( dir_cli[0], dir_cli[1] ) )
	if os.fork():
		#dad
		dialogo.close()
	else:
		#son
		s.close()
		while True:
			buf = dialogo.recv( 1024 )
			print(buf.decode(CODIFICATION))
			print("Escribir respuesta:")
			respuesta = input()
			if not respuesta:
				break
			dialogo.sendall( respuesta.encode(CODIFICATION) )
		print( "Solicitud de cierre de conexión recibida." )
		dialogo.close()
		exit( 0 )
s.close()

