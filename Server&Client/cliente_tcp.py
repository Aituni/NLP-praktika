#!/usr/bin/env python3

import socket, sys, time
import intermediario as inter
import json

PORT = inter.Command.port
CODING = inter.Command.coding

def main():
	if len( sys.argv ) != 2:
		print( "Uso: {} <servidor>".format( sys.argv[0] ) )
		exit( 1 )

	dir_serv = (sys.argv[1], PORT)

	s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	print(dir_serv)
	s.connect( dir_serv )

	while True:
		if not client(s):
			break
	s.sendall("{}\r\n".format(inter.Command.Close).encode(CODING))	
	s.close()

def client(s): #return True to continue, False to exit

	print_menu("title")
	### PARAMETERS ###
	version = inter.recvline(s).decode(CODING)# VRS0.2\r\n
	version = float(version[3:])
	config = load_appConfig(s, version)

	json, tag_info, alg, tag, lan = ask_params(config)
	msg = "{}{}#{}#{}#{}#{}\r\n".format(inter.Command.Parameters, json, tag_info, alg, tag, lan) # PRMFalse#True#\r\n
	s.sendall( msg.encode( CODING ))
	#TODO: controlar error
	resp = inter.recvline(s).decode(CODING)# OK+ or ER-

	### FILE ###
	print_menu("options")#file type
	file_type = input() # 1 test or 2 upload

	if file_type == "2":
		print_menu("upload")
		path = input()
		inter.upload_file(s, path)

		inter.download_file(s)
	else:
		ask_testFile(s, config) #FLE1\r\n
		inter.download_file(s)
	print_menu('restart')
	return True

"""	help	title	options 	test 	upload 	parameters 	language 	algorithm 	tagger 	json 	tag_info"""
def print_menu(section):
	
	if section == "title":
		print("\n{}".format("-"*40))
		print("{:^40}".format("NLP-TAGGER"))
		print("{}".format("-"*40))
		print("\nWrite the option's id and press <ENTER> to confirm.")
		print("<q> to quit. \t <h> for help.\n")
	
	elif section == "help": #help
		print("\n####  HELP:  ####")
	elif section == "options":
		print("\n####  TAGGING FILE:  ####")
		print("choose which file do you want to analyze")
		print("\n  1. Test Files")
		print("  2. Upload File")

	elif section == "restart":
		time.sleep(1) #seconds
		print("\nRESTARTING")
		for i in range(3):
			time.sleep(1) #seconds
			print(".")
		time.sleep(1) #seconds

	elif section == "upload":
		print("\n####  UPLOAD FILE:  ####")
		print("Put the path of the file.")

	elif section == "test":
		print("\n####  TEST FILE:  ####")
		print("Select from the available test files.")

	elif  section == "parameters":
		print("\n####  CHOOSE PARAMETERS:  ####\n")

# true if break
def special_actions(text): 
	resul = False
	if text == 'h':
		print_menu(-1)
	if text == 'q':
		resul = True
	return resul

#TODO: control de errores
def ask_params(config):

	params = config['params']

	def ask_param(parameter):
		print("\n## {:^20} ##".format(parameter))
		k = 1
		opt_KeyDict={}
		for opt in params[parameter]:
			print( '{}. {}'.format(str(k), str(params[parameter][opt])) )
			opt_KeyDict[k] = opt
			k+=1

		selection = int(input('\nSelect one option:\t')) #TODO: control de errores
		if selection in opt_KeyDict:
			return opt_KeyDict[selection]
		#else return ERROR # TODO: error

	print_menu("parameters")
	print("NOTE: \n\tJson include following tags:"+str(config['json_taggers']))
	json = ask_param('json')
	tag_info = ask_param('tag_info')
	alg = ask_param('algorithm')
	tag = ask_param('tagger')
	lan = ask_param('language')

	return json, tag_info, alg, tag, lan

def load_appConfig(s, current_version):
	
	try:
		file = open('settings.json', 'r')
		config = json.load(file)
		if config['version'] < current_version:
			update_appConfig(s)
			return load_appConfig(s, -1)#updated version
		file.close()
		
	except:
		update_appConfig(s)
		return load_appConfig(s, -1)#updated version

	return config

def update_appConfig(s):
	msg = inter.Command.Update+'\r\n'
	s.sendall(msg.encode(CODING)) # UPD\r\n
	inter.download_file(s)

def ask_testFile(s, config):
		print_menu("test")
		files = config['test_files']
		for i in range(len(files)):
			print(str(i)+". "+ str(files[i]))

		test_file = input()
		msg = "{}{}\r\n".format(inter.Command.File, test_file) # FLE1\r\n #archivo de pruebas
		s.sendall( msg.encode( CODING ))

if "__main__" == __name__:
	main()
