#!/usr/bin/env python3

import socket, os, glob
import intermediario as inter
from shutil import copyfile

PORT = inter.Parameters.Port
CODING = inter.Parameters.Coding
ER_MSG = inter.Parameters.Error
APP_PATH = "../Tagger/"
ManModelDIR = ["./ManualModels"]

def servidor():
	s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

	s.bind( ('', PORT) )
	s.listen( 5 )

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
			try:
				config = inter.load_appConfig()
			except:
				copyfile(APP_PATH+"settings.json", "settings.json")
				config = inter.load_appConfig()

			makeDirs(config)
			while True:
				if not service(dialogo, config):
					clean_files(config)
					break
			print( "Solicitud de cierre de conexión recibida." )
			dialogo.close()
			exit( 0 )
	s.close()

# return True if exit. else, false
def service(s, config):
	
	# enviar version
	resp = inter.Command.Version+str(config['version'])+"\r\n"# VRS0.2\r\n
	s.sendall(resp.encode(CODING))

	msg = inter.recvline(s).decode(CODING)
	if msg[:3] == inter.Command.Close:
		return False
	elif msg[:3] == inter.Command.Update:
		inter.upload_file(s, APP_PATH+'settings.json')
		#os.remove('settings.json') #TODO

	elif msg[:3] == inter.Command.Parameters:
		msg = msg[3:]#quitar comando
		json, tag_info, alg, tag, lan = tuple(msg.split('#')) # parameters
		json = json == 'true'
		tag_info = tag_info == 'true'
		print("- json: ")
		print(json)
		print(str(json))
		print(type(json))

		print("- tag_info: ")
		print(tag_info)
		print(str(tag_info))
		print(type(tag_info))

		if tag == 'manual':
			modelName = inter.download_file(s, outDir=ManModelDIR[0])
			tag = ManModelDIR[0]+"/"+ modelName

		resp = inter.Command.OK+"\r\n"
		s.sendall(resp.encode(CODING)) # OK+ TODO: app response

		msg = inter.recvline(s).decode(CODING)
		comando = msg[:3]
		files_qty = 1
		
		if msg[:3] == inter.Command.Close:
			return False

		elif comando == inter.Command.File:
			#test files
			fileNum = int(msg[3:])#quitar comando
			filename = config['test_files'][fileNum]
			files_qty = 1

		elif comando == inter.Command.Quantity:
			# TODO: control de errores
			files_qty = int(msg[3:])
			filename = inter.download_file(s, outDir=config['paths']['server_in'])

		for i in range(files_qty):
			if i > 0:#test file dont need to download
				filename = inter.download_file(s, outDir=config['paths']['server_in']) 
			filepath = config['paths']['server_in']+filename
			print('Ejecucion de aplicacion:')
			#os.path.basename(path) # rm folders form path
			(outFilename, ext) = os.path.splitext(filename)
			outFilename = "OUT_"+ outFilename
			outFilepath = config['paths']['server_out']+outFilename

			pid = os.fork()
			if not pid:
				#son
				s.close()
				msg = 'python3 {}main.py {} {} {} {} {} {} {}'.format(
					APP_PATH, filepath, outFilepath, alg, lan, tag, json, tag_info )
				os.system(msg)
				exit(0)
			else:
				os.wait() # wait until son end processing file

				if json:
					formato = ".json"
				else:
					formato = ".tsv"
				outFilepath = outFilepath+formato

				resp = inter.Command.OK+"\r\n"
				s.sendall(resp.encode(CODING)) # OK+

				inter.upload_file(s, outFilepath)

	return True	

def makeDirs(config):
	if not os.path.exists(ManModelDIR[0]):
		os.makedirs(ManModelDIR[0])
		ManModelDIR[0] = ManModelDIR[0] + "/"

	if not os.path.exists(config['paths']['server_in'][:-1]): #[:-1] para quitar el "/" final
		os.makedirs(config['paths']['server_in'][:-1])

	if not os.path.exists(config['paths']['server_out'][:-1]):
		os.makedirs(config['paths']['server_out'][:-1])

def clean_files(config):
	input_files = glob.glob(config['paths']['server_in'] + "*")
	output_files = glob.glob(config['paths']['server_out'] + "*")
	ManModel_files = glob.glob(ManModelDIR[0]+"*")

	files = input_files + output_files + ManModel_files

	for file in files:
		os.remove(file)

if "__main__" == __name__:
	servidor()