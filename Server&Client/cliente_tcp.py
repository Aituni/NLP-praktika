#!/usr/bin/env python3

import socket, sys, time
import intermediario as inter
import glob, os

PORT = inter.Parameters.Port
CODING = inter.Parameters.Coding
ER_MSG = inter.Parameters.Error
OUTDIR = ["./Output/"]
CONFIG = [0]

def main():
	if len( sys.argv ) != 2:
		print( "Uso: {} <servidor>".format( sys.argv[0] ) )
		exit( 1 )

	dir_serv = (sys.argv[1], PORT)

	s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	#print(dir_serv)
	s.connect( dir_serv )

	while True:
		if not client(s):
			print_menu('turn_off')
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
		print(str(version))
		try:
			if not CONFIG[0]:
				CONFIG[0] = inter.load_appConfig()
				print(str(CONFIG[0]['version']))
			if CONFIG[0]['version'] < version:
				update_appConfig(s)
				CONFIG[0] = inter.load_appConfig()
		except:
			update_appConfig(s)
			CONFIG[0] = inter.load_appConfig()

		print(str(CONFIG[0]['version']))
		
	if not os.path.exists(OUTDIR[0]):
		os.makedirs(OUTDIR[0])

	#----------------#
	#   PARAMETERS   #
	#----------------#
	p = ask_params()
	if not p:
		return False # Exit
	msg = "{}{}#{}#{}#{}#{}\r\n".format(
		inter.Command.Parameters, p['json'], p['tag_info'], 
		p['algorithm'], p['tagger'], p['language']) # PRMFalse#True#...\r\n
	s.sendall( msg.encode( CODING ))

	if p['tagger'] == 'manual':
		if not getSendModel(s):
			return False # Exit

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
					print( ER_MSG[0] )
					continue
				else:
					break # valid value
		except:
			continue # ask again
	
	if int(file_type) == 1: 
	# Test file
		file_num_str = ask_testFile(s) #FLE1\r\n
		if not file_num_str:
			return False # Exit
		msg = "{}{}\r\n".format(inter.Command.File, file_num_str) # FLE1\r\n
		s.sendall( msg.encode( CODING ))

		if not inter.isOK(inter.recvline(s).decode(CODING)):
			return False #Exit
		inter.download_file(s, outDir=OUTDIR[0])

	elif int(file_type) == 2: 
	# Upload file
		obtainSendDownload_file( s )

	elif int(file_type) == 3: 
	# dir files
		obtainSendDownload_file( s, directory = True )
	else:
		print(" Invalid file type ")
		return True
	return True

def obtainSendDownload_file(s, directory = False):
	if directory:
		print_menu("upload_dir")
	else:
		print_menu("upload_file")

	# OBTAIN
	while True:
		path = input(" Write file path: ")
		if path.find("'")!=-1:
			path=path[:-1].replace("'", "")
		action = special_actions(path)

		if action:
			# special actions
			if action == -1:
				return False # Exit
		elif directory and os.path.isdir(path):
			# dir 
			files = glob.glob(path+"/*")
			if len(files) == 0:
				print(" {} dir is empty".format(path))
			else:
				break
		elif not directory and os.path.isfile(path):
			# file
			break
		else:
			# error
			if directory:
				print(" {} dir not found.".format(path))
			else:
				print("{} File not found.".format(path))

	if not directory:
		files = [path]
		outdir = OUTDIR[0]
	else:
		outdir = OUTDIR[0] + "OUT_" + path.split("/")[-1] + "/" #TOTEST
		if not os.path.isdir(outdir):
			os.makedirs(outdir)

	# SEND
	file_qty = str(len(files))
	s.sendall("{}{}\r\n".format(inter.Command.Quantity, file_qty).encode(CODING))
	count = 0
	for file in files:
		inter.upload_file(s, file)
		if not inter.isOK(inter.recvline(s).decode(CODING)):
			print("Error with '{}' file".format(str(file)))
		else:
			inter.download_file(s, outDir=outdir)
			count += 1
			print("Completed {}/{} files".format(str(count), str(file_qty)))

"""	Sections:
help	title	options test 	upload_file		upload_dir 	parameters """
def print_menu(section):
	
	if section == "title":
		print("\n{}".format("-"*40))
		print("{:^40}".format("NLP-TAGGER"))
		print("{:^40}".format("(with Flair)"))
		print("{}".format("-"*40))
		print("\nWrite the option's id and press <ENTER> to confirm.")
		print("\t<q> to quit. \n")
	
		#TODO
	elif section == "options":
		print("\n####  TAGGING FILE:  ####")
		print("choose which file do you want to analyze")
		print("\n1.\tTest files")
		print("2.\tUpload file")
		print("3.\tUpload all files of one directory")

	elif section == "restart":
		time.sleep(1) #seconds
		print("\nRESTARTING")
		for i in range(3):#animacion prescindible
			time.sleep(0.5) #seconds
			print("\r.")
		time.sleep(1) #seconds
	elif section == "turn_off":
		print("\n Turning off. Bye.")

	elif section == "upload_file":
		print("\n####  UPLOAD FILE:  ####")
		print("Put the path of the file you want to analyze.")

	elif section == "upload_dir":
		print("\n####  UPLOAD DIRECTORY:  ####")
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
	if text == 'q':#exit
		resul = -1
	return resul

def ask_params():

	params = CONFIG[0]['params']

	def ask_param(parameter):
		print("\n## {:^15} ##\n".format(parameter))
		k = 1
		opt_KeyDict={}
		for opt in params[parameter]:
			print( '  {}. {}'.format(str(k), str(params[parameter][opt])) )
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
				if int(selection) >= k or int(selection) < 0:
					print( ER_MSG[0] )
					return ask_params(parameter) # ask again
		except:
			return ask_param(parameter) # ask again

		if int(selection) in opt_KeyDict:
			return opt_KeyDict[int(selection)]
		else:
			print( ER_MSG[0] )
			return ask_params(parameter) # ask again

	print_menu("parameters")
	print("NOTE: \n   Json include following tags:"+str(CONFIG[0]['json_taggers']))
	parameters = params.keys()
	selections = {}
	for param in parameters:
		value = ask_param(param)
		if not value:
			return False # Exit
		else:
			selections[param] = value

	return selections

def update_appConfig(s):
	print(" Updating...")
	msg = inter.Command.Update+'\r\n'
	s.sendall(msg.encode(CODING)) # UPD\r\n
	inter.download_file(s)
	print("\n Updated")

def ask_testFile(s):
		print_menu("test")
		files = CONFIG[0]['test_files']
		for i in range(len(files)):
			print("{}.\t{}".format(str(i+1), str(files[i])))

		test_file = input('\nSelect one option:\t')
		try:
			action = special_actions(test_file)
			if action:
				if action == -1:
					return False # Exit
				else:
					ask_testFile(s) # ask again
			else:
				test_file = int(test_file) - 1
				if test_file >= len(files) or test_file < 0:
					print( ER_MSG[0] )
					return ask_testFile(s) # ask again
		except:
			return ask_testFile(s) # ask again

		test_file = str(test_file) #range [1,...) to [0,...) of the array
		return test_file		

def getSendModel(s):
	print("\n NOTE:  Don't worry if choosen values are not the same of your model's. \n")
	# Get model
	while True:
		path = input(" Insert here the model's path:\t")
		if path.find("'")!=-1:
			path=path[:-1].replace("'", "")
		action = special_actions(path)

		if action:
			# special actions
			if action == -1:
				return False # Exit
		elif os.path.isfile(path):
			# file
			break
		else:
			# error
			print("{} File not found.".format(path))
	# Send
	inter.upload_file(s, path)
	modelID = path.split("/")
	modelID = modelID[-2] +"/"+ modelID[-1] # dir/file : to prevent files with the same name
	s.sendall("{}{}\r\n".format(inter.Command.Model, modelID).encode(CODING))
	CONFIG[0]['params']['tagger'][modelID] = path # local config
	return True

if "__main__" == __name__:
	main()
