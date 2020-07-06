import os.path
import requests

# Return 0 if the model is official or is downloaded in the correct path. 
# Else return code[], a list with model specs.
def clean_modelName(algorithm, tagger, language): 

	code = [] # id del modelo
	# first 	= algorithm (1-flair, 2-transformer, 3-both)
	# second 	= tagger (1-ner, 2-pos, 3-chunk, 4-manually)
	# third 	= language (1-eu, 2-es, 3-en, 4-ca, 5-gl)

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
		#TODO
		code.append(3)

	else: # insertado manualmente el modelo concreto
		if algorithm == 'FT' or algorithm == 'TF':
			print("Please, choose only one algorithm for manual models.")
			return -1, "", ""
		if fl_path: # si se ha escogido flair
			fl_path = tagger
		if tf_path: # si se ha escogido transformer
			tf_path = tagger
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
	elif language == 'ga':
		code.append(5)

	if fl_path:
		fl_path = fl_path + language + '/best-model.pt'
	if tf_path:
		tf_path = tf_path + language + '/best-model.pt'

	### MODELOS OFICIALES ###
	# first 	= algorithm (1-flair, 2-transformer, 3-both)
	# second 	= tagger (1-ner, 2-pos, 3-chunk, 4-manually)
	# third 	= language (1-eu, 2-es, 3-en, 4-ca, 5-gl)

	official = False

	if code[0]%2 == 1: #flair
		if code[1] == 1:#ner
			if code[2] == 3:#en
				fl_path = 'ner'
				official = True
		if code[1] == 2:#pos
			if code[2] == 3 or code[2] == 2: #es - en
				fl_path = 'pos-multi'
				official = True
	if code[0]%2 == 0: #transformer
		if code[1] == 1:#ner
			if code[2] == 3:#en
				tf_path = 'ner'
				official = True

	### COMPROBACION ###
	fl = True
	tf = True
	if fl_path:
		#print(fl_path)
		fl = os.path.isfile(fl_path)
	if tf_path:
		tf = os.path.isfile(tf_path)

	if (tf and fl) or official: #los modelos a usar existen en las ubicaciones adecuadas
		return 0, fl_path, tf_path
	return code, fl_path, tf_path


def download(code, fl_path, tf_path):
	# first 	= algorithm (1-flair, 2-transformer, 3-both)
	# second 	= tagger (1-ner, 2-pos, 3-chunk, 4-manually)
	# third 	= language (1-eu, 2-es, 3-en, 4-ca, 5-gl)
	exist = False
	if code[0]%2 == 1: #flair
		if code[1] == 1:#ner
			if code[2] == 1:#eu
				#ner-eu	
				url = ''
				#exist = True

	if not exist:
		print("Error. Model not found. Try downloading manually.")
		return
	r = requests.get(url)
	#print(r)
	#print(r.content)
	if r.status_code == 200:#OK
		print("downloading model...\n")
		if code[0]%2 == 1: #flair
			outfile=open( fl_path, "wb" )
		if code[0] == 2 or code[0] == 3: #transformer
			outfile=open( tf_path, "wb" )

		outfile.write(r.content)
		outfile.close() 