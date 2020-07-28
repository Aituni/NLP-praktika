#!/usr/bin/env python3

import socket, sys, time
import intermediario as inter
import json, glob, os

PORT = inter.Command.port
CODING = inter.Command.coding
err_msg_inVal = " inserted value is not valid "

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
			print(" Turning off. Bye. ")
			break
		else:
			print_menu('restart')
	s.sendall("{}\r\n".format(inter.Command.Close).encode(CODING))	
	s.close()


def client(s): #return True to continue, False to exit

	print_menu("title")
	#----------------------#
	#   VERSION / UPDATE   #
	#----------------------#
	#TODO: app exit when download for the first time settings.json
	msg = inter.recvline(s).decode(CODING)# VRS0.2\r\n
	comando = msg[:3]
	if comando != inter.Command.Version:
		print("Error: Unexpected {} command, {} expected".format(comando, inter.Command.Version))
		return False
	else:
		version = float(msg[3:])
		config = load_appConfig(s, version)

	#----------------#
	#   PARAMETERS   #
	#----------------#
	p = ask_params(config)
	if not p:
		return False # Exit
	msg = "{}{}#{}#{}#{}#{}\r\n".format(
		inter.Command.Parameters, p['json'], p['tag_info'], 
		p['algorithm'], p['tagger'], p['language']) # PRMFalse#True#\r\n
	s.sendall( msg.encode( CODING ))
	#TODO: controlar error
	resp = inter.recvline(s).decode(CODING)# OK+ or ER-
	if not inter.isOK(resp):
		return False

	#----------#
	#   FILE   #
	#----------#
	print_menu("options")#file type
	while True:
		file_type = input("\nSelect one option:\t") # 1 test, 2 upload, 3 all dir files
		try:
			action = special_actions(file_type)
			if action:
				if action == -1:
					return False # Exit
			else:
				if int(file_type) > 3 or int(file_type) < 0:
					raise InError(err_msg_inVal)
				else:
					break # valid value
		except:
			continue # ask again
	

	# - - - - - #
	# Test file #
	# - - - - - #
	if int(file_type) == 1: 
		file_num_str = ask_testFile(s, config) #FLE1\r\n
		if not file_num_str:
			return False # Exit
		msg = "{}{}\r\n".format(inter.Command.File, file_num_str) # FLE1\r\n
		s.sendall( msg.encode( CODING ))

		if not inter.isOK(inter.recvline(s).decode(CODING)):
			return False #Exit
		inter.download_file(s)

	# - - - - - - #
	# Upload file #
	# - - - - - - #
	elif int(file_type) == 2: # Upload file
		print_menu("upload_file")
		while True:
			path = input()
			if path.find("'")!=-1:
				path=path[:-1].replace("'", "")
			action = special_actions(path)
			if action:
				if action == -1:
					return False # Exit
			elif os.path.isfile(path):
				break
			else:
				print("{} File not found.".format(path))
		inter.upload_file(s, path)
		if not inter.isOK(inter.recvline(s).decode(CODING)):
			return False #exit
		inter.download_file(s)

	# - - - - - - - - - - -#
	# Upload all dir files #
	# - - - - - - - - - - -#
	elif int(file_type) == 3: # dir files
		print_menu("upload_dir")
		files = []
		while True:
			path = input()
			if path.find("'")!=-1:
				path=path[:-1].replace("'", "")
			action = special_actions(path)
			if action:
				if action == -1:
					return False # Exit
			elif os.path.isdir(path):
				files = glob.glob(path+"/*")
				if len(files) == 0:
					print(" {} dir is empty".format(path))
				else:
					break
			else:
				print(" {} dir not found.".format(path))

		file_qty = str(len(files))
		s.sendall("{}{}\r\n".format(inter.Command.Quantity, file_qty).encode(CODING))
		count = 0
		for file in files:
			inter.upload_file(s, file)
			if not inter.isOK(inter.recvline(s).decode(CODING)):
				print("Error with '{}' file".format(str(file)))
			else:
				inter.download_file(s)
				count += 1
				print("Completed {}/{} files".format(str(count), str(file_qty)))

	else:
		print(" Invalid file type ")
		return True

	return True

"""	Sections:
help	title	options test 	upload_file		upload_dir 	parameters """
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
		print("\n1.\tTest files")
		print("2.\tUpload file")
		print("3.\tUpload all files of one directory")

	elif section == "restart":
		time.sleep(1) #seconds
		print("\nRESTARTING")
		for i in range(3):
			time.sleep(1) #seconds
			print(".")
		time.sleep(1) #seconds

	elif section == "upload_file":
		print("\n####  UPLOAD FILE:  ####")
		print("Put the path of the file you want to analyze.")

	elif section == "upload_dir":
		print("\n####  UPLOAD FILE:  ####")
		print("Put the path of the dir with all the files you want to analyze.")

	elif section == "test":
		print("\n####  TEST FILE:  ####")
		print("Select from the available test files.")

	elif  section == "parameters":
		print("\n####  CHOOSE PARAMETERS:  ####\n")

# -1 if break
# if activate_actions == False : the function only tells you if 
# text is (return x!=0, as True) or not (return 0, as False) an especial action
def special_actions(text, activate_actions = True): 
	resul = 0
	if text == 'h':
		if activate_actions:
			print_menu(-1)
		resul = 1
	if text == 'q':
		resul = -1
	return resul

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

		selection = input('\nSelect one option:\t')
		try:
			action = special_actions(selection)
			if action:
				if action == -1:
					return False # Exit
				else:
					return ask_params(parameter) # ask again
			else:
				if int(selection) > k or int(selection) < 0:
					raise InError(err_msg_inVal)
		except:
			return ask_param(parameter) # ask again

		if int(selection) in opt_KeyDict:
			return opt_KeyDict[int(selection)]
		#else return ERROR # TODO: error

	print_menu("parameters")
	print("NOTE: \n\tJson include following tags:"+str(config['json_taggers']))
	parameters = params.keys()
	selections = {}
	for param in parameters:
		value = ask_param(param)
		if not value:
			return False # Exit
		else:
			selections[param] = value

	return selections

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
			print("{}.\t{}".format(str(i+1), str(files[i])))

		test_file = input('\nSelect one option:\t')
		try:
			action = special_actions(test_file)
			if action:
				if action == -1:
					return False # Exit
				else:
					ask_testFile(s, config) # ask again
			else:
				test_file = int(test_file) - 1
				if test_file >= len(files) or test_file < 0:
					raise InError(err_msg_inVal)
		except:
			return ask_testFile(s, config) # ask again

		test_file = str(test_file) #range [1,...) to [0,...) of the array
		return test_file		

if "__main__" == __name__:
	main()
