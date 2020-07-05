import flair_tagging as fl
import transformer_tagging as tf
import os.path

IN_FILE = "../tests/Input/CoNLL-eu.txt"  # contain the sentences that we want to analyze.
OUT_FILE = "../tests/Output/CoNLL-eu_OUT" # is the file where the results will be writed. (if JSON = True, the file will be in 'json' format, else 'txt')

"""
'F' = Flair 	'T' = Transformers 		'FT' = Both
"""
ALGORITHM = 'F' 

"""
'eu' = euskera		'es' = español		'en' = english

TODO:		'ca' = catalan		'gl' = gallego
"""
LANGUAGE = 'eu'

"""
(manually) => insert full directory path or models official tagger name
'ner' = Named Entity Recognition
'pos' = Part Of Speech (only english and Spanish)
TODO: 'chunk' = chunking  (only english)
"""
TAGGER = 'ner'

"""
True = print more info for each word (NER, POS, Chunking) in json format.
False = print chosen tag in TAGGER in txt format.
"""
JSON = False

"""
True = print info about the tagger
False = Only print words and tags
"""
TAG_INFO = False


"""
This function analyze the sentences of the IN_FILE, with transformers
using tf_tagger and flair using fl_tagger model. The results will be 
writed on the OUT_FILE, CoNLL style outfile.write(sentence.to_tagged_string()).

String tf_tagger: model name for tagging or classification using transformers.
					put	empty string ("") if you dont want to clasify with transformers.
String fl_tagger: model name for tagging or classification using flair.
					put	empty string ("") if you dont want to clasify with flair.
"""
def file_cases(tf_tagger, fl_tagger, tagger_info=True):
	file = open(IN_FILE, "r")
	if tagger_info:
		if tf_tagger:
			outfile.write("Tagger (transformers): "+tf_tagger+ "\n")
		if fl_tagger:
			outfile.write("Tagger (flair): "+fl_tagger+ "\n")

	#file.readline() # this is for tests

	while True:

		#file.readline() # this is for tests

		# Leemos el texto
		text = file.readline()
		if text == "":
			print ("\nEND.\n")
			break

		#print("text: "+text) # this is for tests

		if tf_tagger:
			if tagger_info:
				outfile.write("TRANSFORMERS: \n\n")
			tf.tag_basic(text, tf_tagger, outfile)

		if fl_tagger:
			if tagger_info:
				outfile.write("\nFLAIR: \n\n")
			sentences = fl.tag_listSentences(text, fl_tagger, outfile)
			print_CoNLL(sentences)

	file.close()

def print_CoNLL(sentences):
	# iterate through sentences and outfile.write predicted labels
	for sentence in sentences:
		
		taged_sent = sentence.to_tagged_string()
		word_list = taged_sent.split(" ")
		#print(word_list)

		i=0
		while i+1 < len(word_list):
			act=word_list[i].strip('\n\t')
			nextw=word_list[i+1].strip('\n\t')
			if nextw[0] == '<': # is a tag
				outfile.write("{:<17}{:>8}\n".format(act, nextw))
				i+=1
			else:
				outfile.write("{:<17}{:>8}\n".format(act, "O"))
			i+=1

		lastw=word_list[-1]
		if lastw: # hay alguna palabra
			if lastw[0] != '<': # if last word is not a tag, print
				lastw=lastw.strip('\n')# remove \n from the word
				outfile.write("{:<17}{:>8}\n".format(lastw, "O"))

# Return 0 if the model is official or is downloaded in the correct path. 
# Else return code[], a list with model specs.
def clean_modelName(): 

	code = [] # id del modelo
	# first 	= algorithm (1-flair, 2-transformer, 3-both)
	# second 	= tagger (1-ner, 2-pos, 3-chunk, 4-manually)
	# third 	= language (1-eu, 2-es, 3-en, 4-ca, 5-gl)

### ALGORITMO ### code[0]

	if ALGORITHM == 'F':
		# put empty string ("") if you dont want to clasify with that alorithm.
		flair_model = '../Models/trained_models/Flair/eusk/from_epub/best-model.pt'
		transformer_model = ''
		code.append(1)
	elif ALGORITHM == 'T':
		# put empty string ("") if you dont want to clasify with that alorithm.
		flair_model = ''
		transformer_model = '../Models/trained_models/Transformer/'
		code.append(2)
	elif ALGORITHM == 'FT' or ALGORITHM == 'TF':
		flair_model = '../Models/trained_models/Flair/'
		transformer_model = '../Models/trained_models/Transformer/'
		code.append(3)

### TAGGER ### code[1]

	if TAGGER == 'ner':
		if flair_model:
			flair_model = flair_model+'ner/'
		if transformer_model:
			transformer_model = transformer_model+'ner/'
		code.append(1)

	elif TAGGER == 'pos':
		if flair_model:
			flair_model = flair_model+'pos/'
		if transformer_model:
			transformer_model = transformer_model+'pos/'
		code.append(2)

	elif TAGGER == 'chunk':
		#TODO
		code.append(3)

	else: # insertado manualmente el modelo concreto
		if flair_model: # si se ha escogido flair
			flair_model = TAGGER
		if transformer_model: # si se ha escogido transformer
			transformer_model = TAGGER
		code.append(4)

### IDIOMA ### code[2]
	if LANGUAGE = 'eu':
		code.append(1)
	elif LANGUAGE = 'es':
		code.append(2)
	elif LANGUAGE = 'en':
		code.append(3)
	elif LANGUAGE = 'ca':
		code.append(4)
	elif LANGUAGE = 'ga':
		code.append(5)

	if flair_model:
		flair_model = flair_model + LANGUAGE + '/best-model.pt'
	if transformer_model:
		transformer_model = transformer_model + LANGUAGE + '/best-model.pt'

### MODELOS OFICIALES ###
	if code[0]

### COMPROBACION ###
	fl = True
	tf = True
	if flair_model:
		fl = os.path.isfile(flair_model)
	if transformer_model:
		tf = os.path.isfile(transformer_model)

	if tf and fl: #los modelos a usar existen en las ubicaciones adecuadas
		return 0
	return code




if "__main__" == __name__:

    clean_modelName()
	try:
		outfile = open(OUT_FILE, "w")
		file_cases(transformer_model, flair_model, tagger_info=TAG_INFO) # tf, fl
	finally:
		outfile.close()

	"""
	Some interesting models (flair):
	- pos-multi: Part of speech (verb, noun, etc.), multiple languages (English, German, French,
		 Italian, Dutch, Polish, Spanish, Swedish, Danish, Norwegian, Finnish and Czech)
	- ner: 4-class Named Entity Recognition, english model.
	- sentiment: text classification, [positive, negative] sentiment. English model.
	- frame: Semantic Frame Detection (experimental). Makes a distinction between two different meanings of the same word.
			(Error with windows paths)
	"""

	"""
	Some interesting models (transformer):
	- ner: 4-class Named Entity Recognition, english model. example: I-LOC 
		notation:
			x-LOC == Location
			x-PER == Person
			x-ORG == Organization
			o == Other

			B-x == Beginning of entity
			I-x == Inside entity
			O-x == Outside entity
	- sentiment-analysis: text classification, [positive, negative] sentiment. English model.
	- frame: Semantic Frame Detection (experimental). Makes a distinction between two different meanings of the same word.
			(Error with windows paths)
	"""