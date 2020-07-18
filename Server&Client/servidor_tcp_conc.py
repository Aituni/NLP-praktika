#!/usr/bin/env python3

import socket, os, signal
import intermediario as inter
import sys, importlib
import main# TODO: import main

PORT = inter.Command.port
CODIF = "UTF-8"

def servidor():
	s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

	s.bind( ('', PORT) )
	s.listen( 5 )

	signal.signal(signal.SIGCHLD, signal.SIG_IGN)

	while True:
		dialogo, dir_cli = s.accept()
		print( "Cliente conectado desde {}:{}.".format( dir_cli[0], dir_cli[1] ) )
		"""
		if os.fork():
			dialogo.close()
		else:
			s.close()
			while ...
		"""
		while True:
			if service(dialogo):
				print("recibida peticion 'CLOSE'")
				break
		print( "Solicitud de cierre de conexión recibida." )
		dialogo.close()
		exit( 0 )
	s.close()

# return True if exit. else, false
def service(s):
	msg = inter.recvline(s).decode(CODIF)
	if msg[:3] == inter.Command.Close:
		return True

	#if msg[:3]=='PRM':
	msg = msg[3:]#quitar comando
	lan, alg, tag, json, tag_info = get_params(msg)
	s.sendall("OK+\r\n".encode(CODIF))

	msg = inter.recvline(s).decode(CODIF)
	#if msg[:3]=='PRM':
	msg = msg[3:]#quitar comando
	if msg == "1":
		#test files
		option = inter.recvline(s).decode(CODIF)
		option = option[3:]
		filename = test_files(option)
	elif msg =="2":
		#uploaded file
		filename = download_file(s)

	print('Ejecucion de aplicacion:')
	outFilename = "OUT_"+filename[:-4]# TODO: quitar formato
	main.main(filename, outFilename, alg, lan, tag, json, tag_info)
	upload_file(s, outFilename+".txt")# TODO: poner formato

	return False

def upload_file(s, filename):
	file = open("../tests/Output/"+filename, "rb")
	contenido = file.read()
	size = len(contenido)

	msg = "{}{}#{}\r\n".format(inter.Command.Size, size, filename) # SZE1234#filename\r\n
	s.sendall(msg.encode(CODIF))
	#TODO: controlar error
	resp = inter.recvline(s).decode(CODIF)# OK+

	s.sendall(contenido)#archivo
	file.close()

def get_params(msg):
	options = msg.split("#")
	opt = options[0]#language
	if opt == "1":
		lan = "eu"
	elif opt == "2":
		lan = "es"
	elif opt == "3":
		lan = "en"
	elif opt == "4":
		lan = "ca"
	elif opt == "5":
		lan = "gl"

	opt = options[1]#algorithm
	if opt == "1":
		alg = "F"
	elif opt == "2":
		alg = "T"
	elif opt == "3":
		alg = "FT"

	opt = options[2]#Tagger
	if opt == "1":
		tag = "ner"
	elif opt == "2":
		tag = "pos"
	elif opt == "3":
		tag = "chunk"

	opt = options[3]#json
	if opt == "1":
		json = True
	elif opt == "2":
		json = False

	opt = options[4]#tag_info
	if opt == "1":
		tag_info = True
	elif opt == "2":
		tag_info = False

	return lan, alg, tag, json, tag_info

def download_file(s):
	file_info = inter.recvline(s).decode(CODIF) # SZE1234#filename
	file_info = file_info.split("#")

	filename = file_info[-1]
	size = file_info[-2]
	size = int(size[3:])

	data = inter.recvall(s, size)
	file = open(filename, "wb")
	file.write(data)
	file.close()

	return filename

def test_files(opt):
	filename = ""

	if opt == "1":
		filename = "english_text.txt"
	elif opt == "2":
		filename = "es"
	elif opt == "3":
		filename = "eusk_text.txt"
	elif opt == "4":
		filename = "ca"
	elif opt == "5":
		filename = "gl"

	return filename

if "__main__" == __name__:
	servidor()