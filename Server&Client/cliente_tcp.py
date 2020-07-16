#!/usr/bin/env python3

import socket, sys, intermediario, time

PORT = 50003
CODIFICATION = "UTF-8"

def main():
	if len( sys.argv ) != 2:
		print( "Uso: {} <servidor>".format( sys.argv[0] ) )
		exit( 1 )

	dir_serv = (sys.argv[1], PORT)

	s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
	s.connect( dir_serv )

	while True:
		print_menu("title")
		### PARAMETERS ###
		"""
		lan, alg, tag, json, tag_info = get_params()
		msg = "{}{}{}{}{}{}\r\n".format(intermediario.Command.Parameters, lan, alg, tag, json, tag_info) #PRM\r\n
		s.sendall( msg.encode( CODIFICATION ))
		#TODO: controlar error
		intermediario.recvline(s)#OK+ or ER-
		"""
		### FILE ###
		print_menu("options")#file type
		file_type = input() # 1 test or 2 upload
		if special_actions(file_type):
			break
		msg = "{}{}\r\n".format(intermediario.Command.File, file_type) #FLE1\r\n
		s.sendall( msg.encode( CODIFICATION ))

		if file_type == "2":
			upload_file(s)
			download_file(s)

		else:
			print_menu("test")
			test_file = input()
			if special_actions(test_file):
				break
			msg = "{}{}\r\n".format(intermediario.Command.File, test_file) #FLE1\r\n
			s.sendall( msg.encode( CODIFICATION ))

		time.sleep(3) #seconds
	s.close()
"""	help	title	options 	test 	upload 	parameters 	language 	algorithm 	tagger 	json 	tag_info"""
def print_menu(section):
	
	if section == "title":
		print("{}".format("-"*40))
		print("{:^40}".format("NLP-TAGGER"))
		print("{}".format("-"*40))
		print("\nWrite the option's id and press <ENTER> to confirm.")
		print("<q> to quit. \t <h> for help.\n")
	
	elif section == "help": #help
		"""
			Parameters:
		String in_filename: Is the name of the file that contain the sentences that we want to analyze. DO WRITE FORMAT
					default: 'english_text.txt'

		String out_filename: Is the file name where the results will be writed. DO NOT WRITE FORMAT (.txt, ...)
					  		 if JSON = True, the file will be in 'json' format, else 'txt'.
					  default: '1'

		String algorithm:  Is the algorithm we want to use. 
				Options:	'F' = Flair 	'T' = Transformers (experimental) 		'FT' = Both
					default: 'F'

		String language: Is the language of input document.
				Options:	 'eu' = euskera		'es' = español		'en' = english		'ca' = catalan		'gl' = gallego
				 	default: 'en'

		String tagger: Is the tagger that we want to use to analyze the document.
				Options: - (manually) => insert full directory path or models official tagger name. In this case, use only one algorithm. 
					 - 'ner' = Named Entity Recognition
					 - 'pos' = Part Of Speech (only English and Spanish)
					 - 'chunk' = chunking  (only English)
					default: 'ner'
		Bool json: outfile format (json or txt).
				Options:   	True = print more info for each word (NER, POS, Chunking) in json format. ('only en')
					   		False = print chosen tag in 'tagger' in txt format, CoNLL style.
					default = False
		Bool tag_info: Used Tagger info.
				Options:   	True = print few info about the tagger (ONLY WITH JSON = False)
					   		False = Only print words and tags.
					default = False
		"""
	elif section == "options":
		print("####  TAGGING FILE:  ####")
		print("choose which file do you want to analyze")
		print("\n  1. Test Files")
		print("  2. Upload File")

	elif section == "test":
		print("####  TEST FILE:  ####")
		print("choose which file do you want to analyze")
		print("\n  1. English file")
		print("  2. Spanish File")
		print("  3. Basque File")
		print("  4. Catalan File")
		print("  5. Galician File")

	elif section == "upload":
		print("####  UPLOAD FILE:  ####")
		print("Put the path of the file.")

	elif  section == "parameters":
		print("####  CHOOSE PARAMETERS:  ####")

	elif  section == "algorithm":
		print("## Algorithm:")
		print("'F' = Flair(Recommended) 	'T' = Transformers (experimental) 		'FT' = Both (experimental)")

	elif  section == "language":
		print("## Language:")
		print("'eu' = euskera		'es' = español		'en' = english		'ca' = catalan		'gl' = gallego")
	
	elif  section == "tagger":
		print("## Tagger:")
		print("'ner' =  (all languages)		'pos' = (only English and Spanish)		'chunk' = (only English)")

	elif  section == "json":
		print("## json:")
		print(" 1. True 	2. False")

	elif  section == "tag_info":
		print("## Tag info:")
		print(" 1. True 	2. False")
		"""
			in_filename = 'eusk_text.txt', # do write format
			out_filename = 'chunk_eu', 	  # do NOT write format
			algorithm = 'F',	 #	
			language = 'eu',	#  
			tagger = 'chunk',		# 
			json = False,	# outfile format.
			tag_info = True)  # info about tagger
		"""

def special_actions(text): #true if break
	resul = False
	if text == 'h':
		print_menu(-1)
	if text == 'q':
		resul = True
	return resul

""" Currently cant exit """
def upload_file(s):
	print_menu("upload")
	path = input()

	file = open(path, "rb")
	contenido = file.read()
	size = len(contenido)

	msg = "{}{}\r\n".format(intermediario.Command.Size, size) #SZE1234\r\n
	s.sendall(msg.encode(CODIFICATION))
	#TODO: controlar error
	intermediario.recvline(s)#OK+ or ER-


	s.sendall(contenido)#archivo

	file.close()

def download_file(s):
	size = intermediario.recvline(s).decode(CODIFICATION) #FLE 12345
	size = int(size[3:])
	downld_data = intermediario.recvall(s,size).decode(CODIFICATION) # file data
	outfile = open("outfile.txt", "wb")
	outfile.write(downld_data)
	outfile.close

#TODO: control de errores
def get_params():
	print_menu("parameters")
	print_menu("language")
	lan = input()
	print_menu("algorithm")
	alg = input()
	print_menu("tagger")
	tag = input()
	print_menu("json")
	json = input()
	print_menu("tag_info")
	tag_info = input()

	return lan, alg, tag, json, tag_info


if "__main__" == __name__:
	main()