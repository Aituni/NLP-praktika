#!/usr/bin/env python3

import socket, sys, intermediario, time

PORT = 50004
CODIFICATION = "UTF-8"

def main():
	if len( sys.argv ) != 2:
		print( "Uso: {} <servidor>".format( sys.argv[0] ) )
		exit( 1 )

	dir_serv = (sys.argv[1], PORT)

	s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	s.connect( dir_serv )

	while True:
		print("Escribir mensaje (Cliente):")
		msg = input() # 1 test_filest or 2 upload
		if not msg:
			break
		s.sendall( msg.encode( CODIFICATION ))
		resp = s.recv( 1024 )
		print("(server): "+resp.decode(CODIFICATION))

	s.close()

if "__main__" == __name__:
	main()