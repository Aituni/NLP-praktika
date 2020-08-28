import requests
import glob
import os

CONFIG = []
URL = []

"""
	obtain_model(...):	MAIN function
	Return : Array(int), string, string

	With given parameters, it will obtain wich model we will use. If does not exist locally,
	it will create the directory and will try to download the correct model.
"""
def obtain_model(algorithm, tagger, language, settings):
	CONFIG.append(settings['params'])
	URL.append(settings['url'])

	### Directorio ###
	code, fl_path = obtain_dir(algorithm, tagger, language)
	if code[0] == -1: #ERROR
		return code, fl_path

	### file ###
	code, fl_path = official_or_manual_models(code, fl_path, tagger)
	if code[0] != 0:# not found official or manual path
		make_dirs(fl_path)
		code, fl_path = obtain_FilePath(code, fl_path) # get local model, on the path
		if code[0] != 0: # file not found locally
			download(code, fl_path)#download model if is accesible

	return code, fl_path
"""
	obtain_dir(...):
	Return : Array(int), string, string

	This function return the model code, flair model directory path, and transformer model directory path.
	If flair or transformer model is not selected, it will return empty string ('') for that model.

	array(int) code: have all the info about the model.
		each position and value meaning:
			#pos 0. = algorithm (1-flair, 2-transformer) -- Special (-1 ERROR, 0 Success)
			#pos 1. = tagger (1-ner, 2-pos, 3-chunk, 4-manually)
			#pos 2. = language (1-eu, 2-es, 3-en, 4-ca, 5-gl)
		example: [1,1,3] = flair ner model for english language

"""
def obtain_dir(algorithm, tagger, language): 	
	# 0. = algorithm (1-flair, 2-transformer) -- Special (-1 ERROR, 0 Success)
	# 1. = tagger (1-ner, 2-pos, 3-chunk, 4-manually)
	# 2. = language (1-eu, 2-es, 3-en, 4-ca, 5-gl)
	code = [] # id del modelo
	fl_path = '../Models/trained_models/'

	### ALGORITMO ### code[0]
	done = False
	for alg in CONFIG[0]['algorithm']:
		if algorithm == alg:
			fl_path = fl_path + alg + "/"
			code.append(alg)
			done = True
			break
	if not done:
		print("Please, choose one valid algorithm.")
		return [-1], "", ""

	### TAGGER ### code[1]
	done = False
	for tag in CONFIG[0]['tagger']:
		if tagger == tag:
			fl_path = fl_path + tag + "/"
			code.append(tag)
			done = True
			break
	if not done: # insertado manualmente el modelo concreto
		code.append(4)

	### IDIOMA ### code[2]
	done = False
	for lan in CONFIG[0]['language']:
		if language == lan:
			fl_path = fl_path + lan + "/"
			code.append(lan)
			done = True
			break
	if not done: # insertado manualmente el modelo concreto
		print("Please, choose one valid language.")
		return [-1], "", ""

	return code, fl_path
"""
	void make_dir's(...):
	If the model's path does not exist. it will create it.
"""
def make_dirs(fl_path):
	if fl_path:
		if not os.path.isdir(fl_path): #si los directorios no existen, crearlos
			os.makedirs(fl_path, exist_ok = True)
"""
	official_or_manual_models(...):
		if it exists an official model for wanted tagger, it will choose it.
		if the model is a manually writed path of a model it will choose it.

	Return : Array(int), string, string
		it returns an updated parameters (except tagger)

"""
def official_or_manual_models(code, fl_path, tagger):

	### MODELOS OFICIALES ###
	# 0. = algorithm (1-flair, 2-transformer)
	# 1. = tagger (1-ner, 2-pos, 3-chunk, 4-manually)
	# 2. = language (1-eu, 2-es, 3-en, 4-ca, 5-gl)

	modified = False

	if code[0] == 'Flair': 
		if code[1] == 'ner':
			if code[2] == 'en':
				fl_path = 'ner'
				modified = True
		if code[1] == 'pos':
			if code[2] == 'es':
				fl_path = 'pos-multi'
				modified = True
			if code[2] == 'en': 
				fl_path = 'pos'
				modified = True
		if code[1] == 'chunk':
			if code[2] == 'en':
				fl_path = 'chunk'
				modified = True

	### MANUAL - Full path ###

	# en este modo solo se utiliza un algoritmo, flair o transformer
	if code[1] == 4:# MANUAL
		fl_path = tagger
		modified = True

	if modified:
		code = [0]

	return code, fl_path
"""
	obtain_FilePath(...):
		once we have the model path, this function will find between 
		files and choose the first '*.pt' found model file. And update the
		model path with it.

	Return : Array(int), string, string
		it returns an updated parameters
"""
def obtain_FilePath(code, fl_path):
	### Nombre del fichero del modelo ###
	if fl_path:
		#lista de archivos *.pt en el directorio.
		file_list = glob.glob(fl_path+'/*.pt')
		if len(file_list)!=0:# si la lista no esta vacia
			#fichero encontrado
			code = [0]
			#escoger primer archivo *.pt por orden alfabetico
			fl_path = str(file_list[0])

	return code, fl_path
"""
	download(...):
	 	This function try to download choosen model. In their 
	 	correspondent path. Downloaded model's name by default will be 
	 	'downloaded-model.pt'

	Return : Array(int), string, string
		it returns an updated parameters
"""
def download(code, fl_path):
	filename = 'downloaded-model.pt'
	try:
		url = URL[code[0]][code[1]][code[2]]
	except:
		url = ''

	if not url:
		print("Error. Model not found. Try downloading manually.")
		return #end

	### DESCARGAR ###
	r = requests.get(url)
	#print(r)
	#print(r.content)
	if r.status_code == 200:#OK
		print("downloading model...\n")
		outfile=open( fl_path + "/" + filename, "wb" )
		outfile.write(r.content)
		outfile.close()
		code = [0]

	return code, fl_path + filename

