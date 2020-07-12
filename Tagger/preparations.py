import requests
import glob
import os

"""
	obtain_model(...):	MAIN function
	Return : Array(int), string, string

	With given parameters, it will obtain wich model we will use. If does not exist locally,
	it will create the directory and will try to download the correct model.
"""
def obtain_model(algorithm, tagger, language):

	### Directorio ###
	code, fl_path, tf_path = obtain_dir(algorithm, tagger, language)
	if code[0] == -1: #ERROR
		return code, fl_path, tf_path
	make_dirs(fl_path, tf_path)

	### file ###
	code, fl_path, tf_path = official_or_manual_models(code, fl_path, tf_path, tagger)
	if code[0] != 0:
		code, fl_path, tf_path = obtain_FilePath(code, fl_path, tf_path)
		if code[0] != 0: # file not found
			download(code, fl_path, tf_path)#download model if is accesible

	return code, fl_path, tf_path
"""
	obtain_dir(...):
	Return : Array(int), string, string

	This function return the model code, flair model directory path, and transformer model directory path.
	If flair or transformer model is not selected, it will return empty string ('') for that model.

	array(int) code: have all the info about the model.
		each position and value meaning:
			#pos 0. = algorithm (1-flair, 2-transformer, 3-both) -- Special (-1 ERROR, 0 Success)
			#pos 1. = tagger (1-ner, 2-pos, 3-chunk, 4-manually)
			#pos 2. = language (1-eu, 2-es, 3-en, 4-ca, 5-gl)
		example: [1,1,3] = flair ner model for english language

"""
def obtain_dir(algorithm, tagger, language): 	
	# 0. = algorithm (1-flair, 2-transformer, 3-both) -- Special (-1 ERROR, 0 Success)
	# 1. = tagger (1-ner, 2-pos, 3-chunk, 4-manually)
	# 2. = language (1-eu, 2-es, 3-en, 4-ca, 5-gl)
	code = [] # id del modelo

	### ALGORITMO ### code[0]

	if algorithm == 'F':
		# put empty string ("") if you dont want to clasify with that alorithm.
		fl_path = '../Models/trained_models/Flair/'
		tf_path = ''
		code.append(1)
	elif algorithm == 'T':
		# put empty string ("") if you dont want to clasify with that alorithm.
		fl_path = ''
		tf_path = '../Models/trained_models/Transformer/'
		code.append(2)
	elif algorithm == 'FT' or algorithm == 'TF':
		fl_path = '../Models/trained_models/Flair/'
		tf_path = '../Models/trained_models/Transformer/'
		code.append(3)
	else:
		print("Please, choose one valid algorithm.")
		return [-1], "", ""

	### tagger ### code[1]

	if tagger == 'ner':
		if fl_path:
			fl_path = fl_path+'ner/'
		if tf_path:
			tf_path = tf_path+'ner/'
		code.append(1)

	elif tagger == 'pos':
		if fl_path:
			fl_path = fl_path+'pos/'
		if tf_path:
			tf_path = tf_path+'pos/'
		code.append(2)

	elif tagger == 'chunk':
		if fl_path:
			fl_path = fl_path+'chunk/'
		if tf_path:
			tf_path = tf_path+'chunk/'
		code.append(3)

	else: # insertado manualmente el modelo concreto
		if algorithm == 'FT' or algorithm == 'TF':
			print("Please, choose only one algorithm for manual models.")
			return [-1], "", ""
		code.append(4)

	### IDIOMA ### code[2]

	if language == 'eu':
		code.append(1)
	elif language == 'es':
		code.append(2)
	elif language == 'en':
		code.append(3)
	elif language == 'ca':
		code.append(4)
	elif language == 'gl':
		code.append(5)
	else:
		print("Please, choose one valid language.")
		return [-1], "", ""

	if fl_path:
		fl_path = fl_path + language
	if tf_path:
		tf_path = tf_path + language 

	return code, fl_path, tf_path
"""
	void make_dir's(...):
	If the model's path does not exist. it will create it.
"""
def make_dirs(fl_path, tf_path):
	fl_exist = True
	tf_exist = True
	if fl_path:
		fl_exist = os.path.isdir(fl_path)
	if tf_path:
		tf_exist = os.path.isdir(tf_path)

	if not (fl_exist and tf_exist): #si los directorios no existen, crearlos
		if fl_path:
			os.makedirs(fl_path, exist_ok = True)
		if tf_path:
			os.makedirs(tf_path, exist_ok = True)
"""
	official_or_manual_models(...):
		if it exists an official model for wanted tagger, it will choose it.
		if the model is a manually writed path of a model it will choose it.

	Return : Array(int), string, string
		it returns an updated parameters (except tagger)

"""
def official_or_manual_models(code, fl_path, tf_path, tagger):

	### MODELOS OFICIALES ###
	# 0. = algorithm (1-flair, 2-transformer, 3-both)
	# 1. = tagger (1-ner, 2-pos, 3-chunk, 4-manually)
	# 2. = language (1-eu, 2-es, 3-en, 4-ca, 5-gl)

	modified = False

	if code[0] == 1 or code[0] == 3: #flair
		if code[1] == 1:#ner
			if code[2] == 3:#en
				fl_path = 'ner'
				modified = True
		if code[1] == 2:#pos
			if code[2] == 2:#es
				fl_path = 'pos-multi'
				modified = True
			if code[2] == 3: #en
				fl_path = 'pos'
				modified = True
		if code[1] == 3:#chunk
			if code[2] == 3:#en
				fl_path = 'chunk'
				modified = True
				
	if code[0] == 2 or code[0] == 3: #transformer
		if code[1] == 1:#ner
			if code[2] == 3:#en
				tf_path = 'ner'
				modified = True

	### MANUAL - Full path ###

	# en este modo solo se utiliza un algoritmo, flair o transformer
	if code[1] == 3:# MANUAL
		fl_path = tagger
		tf_path = tagger
		modified = True

	if modified:
		code = [0]

	return code, fl_path, tf_path
"""
	obtain_FilePath(...):
		once we have the model path, this function will find between 
		files and choose the first '*.pt' found model file. And update the
		model path with it.

	Return : Array(int), string, string
		it returns an updated parameters
"""
def obtain_FilePath(code, fl_path, tf_path):
	### Nombre del fichero del modelo ###
	if fl_path:
		#lista de archivos *.pt en el directorio.
		file_list = glob.glob(fl_path+'/*.pt')
		if len(file_list)!=0:# si la lista no esta vacia
			#fichero encontrado
			code = [0]
			#escoger primer archivo *.pt por orden alfabetico
			fl_path = str(file_list[0])
	
	if tf_path:#misma estructura, pero con transformers
		file_list = glob.glob(tf_path+'/*.pt')
		if len(file_list)!=0:
			code = [0]
			tf_path = str(file_list[0])

	return code, fl_path, tf_path
"""
	download(...):
	 	This function try to download choosen model. In their 
	 	correspondent path. Downloaded model's name by default will be 
	 	'downloaded-model.pt'

	Return : Array(int), string, string
		it returns an updated parameters
"""
def download(code, fl_path, tf_path):
	filename = 'downloaded-model.pt'
	url = download_url(code)
	if not url:
		print("Error. Model not found. Try downloading manually.")
		return #end

	### DESCARGAR ###
	r = requests.get(url)
	#print(r)
	#print(r.content)
	if r.status_code == 200:#OK
		print("downloading model...\n")
		if code[0]%2 == 1: #flair
			outfile=open( fl_path + "/" + filename, "wb" )
		if code[0] == 2 or code[0] == 3: #transformer
			outfile=open( tf_path + "/" +  filename, "wb" )

		outfile.write(r.content)
		outfile.close()
		code=[0]

	return code, fl_path + filename, tf_path + filename
"""
	String download_url(code):

		This function return the correspondent model's download url.
"""
def download_url(code):

	### ESCOGER URL ###

	# code[0] = algorithm (1-flair, 2-transformer, 3-both)
	# code[1] = tagger (1-ner, 2-pos, 3-chunk, 4-manually)
	# code[2] = language (1-eu, 2-es, 3-en, 4-ca, 5-gl)
	url = ''
	if code[0]%2 == 1:#flair
		if code[1] == 1: #ner
			if code[2] == 1:#eu
				#flair-ner-eu
				url = ''
			if code[2] == 2:#es
				url = ''	
			if code[2] == 3:#en
				url = ''	
			if code[2] == 4:#ca
				url = ''	
			if code[2] == 5:#gl
				url = ''
		if code[1] == 2:#pos
			if code[2] == 1:#eu
				url = ''	
			if code[2] == 2:#es
				url = ''	
			if code[2] == 3:#en
				url = ''
		# ...

	return url
