#!/usr/bin/env python3

import socket, os, signal
import intermediario as inter
import sys, importlib
import main # TODO: import main
import settings

PORT = inter.Command.port
CODING = inter.Command.coding

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
			reload(settings)
			while ...
		"""
		importlib.reload(settings)
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

	# enviar version
	resp = inter.Command.Version+str(settings.config.ALL['version'])+"\r\n"# VRS0.2\r\n
	s.sendall(resp.encode(CODING))

	msg = inter.recvline(s).decode(CODING)
	if msg[:3] == inter.Command.Close:
		return True
	elif msg[:3] == inter.Command.Update:
		settings.make_json()
		inter.upload_file(s, 'settings.json')

	elif msg[:3]=='PRM':
		msg = msg[3:]#quitar comando

		json, tag_info, alg, tag, lan = tuple(msg.split('#')) # parameters
		json = json == 'true'
		tag_info = tag_info == 'true'
		resp = inter.Command.OK+"\r\n"
		s.sendall(resp.encode(CODING)) # OK+

		msg = inter.recvline(s).decode(CODING)
		#if msg[:3]=='PRM':
		comand = msg[:3]
		if comand == inter.Command.File:
			#test files
			fileNum = int(msg[3:])#quitar comando
			filename = get_testFilename(fileNum)
		elif comand == inter.Command.Size:
			#uploaded file
			filename = inter.download_file(s)

		print('Ejecucion de aplicacion:')
		outFilename = "OUT_"+filename[:-4]# TODO: quitar formato
		main.main(filename, outFilename, alg, lan, tag, json, tag_info)
		if json:
			formato = ".json"
		else:
			formato = ".tsv"
		outfilepath = settings.config.ALL['paths']['out']+outFilename+formato
		inter.upload_file(s, outfilepath)# TODO: poner formato

	return False

def get_testFilename(fileNum):
	files = settings.config.ALL['test_files']
	return files[fileNum]

if "__main__" == __name__:
	servidor()