#!/usr/bin/env python3

import socket, os, signal
import intermediario as inter
import sys, importlib

PORT = inter.Command.port
CODING = inter.Command.coding
APP_PATH = "../Tagger/"

def servidor():
	s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

	s.bind( ('', PORT) )
	s.listen( 5 )

	signal.signal(signal.SIGCHLD, signal.SIG_IGN)
	config_version = 0

	while True:
		dialogo, dir_cli = s.accept()
		print( "Cliente conectado desde {}:{}.".format( dir_cli[0], dir_cli[1] ) )
		
		pid = os.fork()
		if pid:
			#dad
			dialogo.close()
		else:
			#son
			s.close()
			#update config
			new_config_version = get_updatedConfig(config_version)
			if new_config_version > config_version:
				config_version = new_config_version
				config = load_appConfig()


			while True:
				if not service(dialogo, config):
					break
			print( "Solicitud de cierre de conexión recibida." )
			dialogo.close()
			exit( 0 )
	s.close()

# return True if exit. else, false
def service(s, config):
	
	# enviar version
	resp = inter.Command.Version+str(config.ALL['version'])+"\r\n"# VRS0.2\r\n
	s.sendall(resp.encode(CODING))

	msg = inter.recvline(s).decode(CODING)
	if msg[:3] == inter.Command.Close:
		return False
	elif msg[:3] == inter.Command.Update:
		settings.make_json()
		inter.upload_file(s, APP_PATH+'settings.json')
		#os.remove('settings.json') #TODO cuando se separen serv&Cli de Tagger

	elif msg[:3] == inter.Command.Parameters:
		msg = msg[3:]#quitar comando
		json, tag_info, alg, tag, lan = tuple(msg.split('#')) # parameters
		json = json == 'true'
		tag_info = tag_info == 'true'

		resp = inter.Command.OK+"\r\n"
		s.sendall(resp.encode(CODING)) # OK+

		msg = inter.recvline(s).decode(CODING)
		comando = msg[:3]
		files_qty = 1
		
		if msg[:3] == inter.Command.Close:
			return False

		elif comando == inter.Command.File:
			#test files
			fileNum = int(msg[3:])#quitar comando
			filename = get_testFilename(fileNum)

		elif comando == inter.Command.Size:
			#uploaded file
			filename = inter.download_file(s)

		elif comando == inter.Command.Quantity:
			# TODO: control de errores
			files_qty = int(msg[3:])
			filename = inter.download_file(s)

		for i in range(files_qty):
			if i > 0:
				filename = inter.download_file(s) 
			print('Ejecucion de aplicacion:')
			#os.path.basename(path) # rm folders form path
			(outFilename, ext) = os.path.splitext(filename)
			outFilename = "OUT_"+ outFilename
			pid = os.fork()
			if not pid:
				#son
				s.close()
				msg = 'python3 {}main.py {} {} {} {} {} {} {}'.format(
					APP_PATH, filename, outFilename, alg, lan, tag, json, tag_info )
				os.system(msg)
				exit(0)

			if json:
				formato = ".json"
			else:
				formato = ".tsv"
			outfilepath = config.ALL['paths']['out']+outFilename+formato

			resp = inter.Command.OK+"\r\n"
			s.sendall(resp.encode(CODING)) # OK+

			wait(pid) # wait until son end processing file
			inter.upload_file(s, outfilepath)

	return True

def get_updatedConfig(Current_version):
	pid = os.fork()
	if not pid:
		#son
		os.system("python3 {}settings.py v".format(APP_PATH))
		exit(0)
	#out, err = pid.communicate() #TODO
	wait(pid) # wait until settings version are completely exported

	#new_version = int(out)  #TODO
	new_version = 0.2

	if Current_version < new_version:
		pid2 = os.fork()
		if not pid2:
			#son
			os.system("python3 {}settings.py ".format(APP_PATH))
			exit(0)
	wait(pid2) # wait until settings are completely exported

	return new_version


def get_testFilename(fileNum):
	files = settings.config.ALL['test_files']
	return files[fileNum]

def load_appConfig():
	file = open(APP_PATH+'settings.json', 'r')
	config = json.load(file)
	file.close()
	return config

if "__main__" == __name__:
	servidor()