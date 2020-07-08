import flair_tagging as fl
import transformer_tagging as tf
import preparations as prep
import json

IN_FILE = "../tests/Input/english_text.txt"  # contain the sentences that we want to analyze. DO WRITE FORMAT
OUT_FILE = "../tests/Output/json-en_OUT" # is the file where the results will be writed. DO NOT WRITE FORMAT (.txt, ...)
			#(if JSON = True, the file will be in 'json' format, else 'txt')

"""
'F' = Flair 	'T' = Transformers 		'FT' = Both
"""
ALGORITHM = 'F' 

"""
'eu' = euskera		'es' = español		'en' = english

TODO:		'ca' = catalan		'gl' = gallego
"""
LANGUAGE = 'en'

"""
(manually) => insert full directory path or models official tagger name. In this case, use only one algorithm. 
'ner' = Named Entity Recognition
'pos' = Part Of Speech (only english and Spanish)
TODO: 'chunk' = chunking  (only english)
"""
TAGGER = 'pos'

"""
True = print more info for each word (NER, POS, Chunking) in json format. ('only en')
False = print chosen tag in TAGGER in txt format.
"""
JSON = True

"""
True = print few info about the tagger (ONLY WITH JSON = False)
False = Only print words and tags
"""
TAG_INFO = True

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

	# Leemos el texto
	text = file.read()

	if tf_tagger: #TODO:
		if tagger_info:
			outfile.write("TRANSFORMERS: \n\n")
		tf.tag_basic(text, tf_tagger, outfile)

	if fl_tagger:
		if tagger_info:
			outfile.write("\nFLAIR: \n\n")
		if JSON:
			sentences_ner = fl.tag_listSentences(text, 'ner')
			sentences_pos = fl.tag_listSentences(text, 'pos')
			#TODO: chunking
			print_json(sentences_ner, sentences_pos)
		else:
			sentences = fl.tag_listSentences(text, fl_tagger)
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
			if isTag(nextw[0]): # is a tag
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
def isTag(word):
	return word[0] == '<'
def print_json(sentences_ner, sentences_pos):
	word_dict = {}
	# iterate through sentences and outfile.write predicted labels
	for i in range(len(sentences_ner)):
		ner_s = sentences_ner[i]
		pos_s = sentences_pos[i]
	
		ner_tagged_sent = ner_s.to_tagged_string()
		pos_tagged_sent = pos_s.to_tagged_string()

		ner_word_list = ner_tagged_sent.split(" ")
		pos_word_list = pos_tagged_sent.split(" ")
		#print(word_list)

		i=0
		j=0
		#son las mismas frases por lo que el numero de palabras son las mismas. solo varian las etiquetas
		while (i+1 < len(ner_word_list)) and (j+1 < len(pos_word_list)):# for each word
			ner_act = ner_word_list[i].strip('\n\t')#limpiar saltos de linea y tabs
			pos_act = pos_word_list[j].strip('\n\t')
			if ner_act != pos_act:
				print("WARNING no match")
				print(pos_act)
				print(ner_act)

			ner_nextw = ner_word_list[i+1].strip('\n\t')
			pos_nextw = pos_word_list[j+1].strip('\n\t')

			word_dict['text'] = ner_act

			if isTag(ner_nextw[0]): 
				word_dict['NER_label'] = ner_nextw
				i+=1
			else:
				word_dict['NER_label'] = "O"

			if isTag(pos_nextw[0]): # is a tag
				word_dict['POS_label'] = pos_nextw
				j+=1
			else:
				word_dict['POS_label'] = "O"

			outfile.write(json.dumps(word_dict, indent = 4, sort_keys=True))
			i+=1
			j+=1

		ner_lastw = ner_word_list[-1]
		pos_lastw = pos_word_list[-1]
		if ner_lastw: # hay alguna palabra
			if not isTag(ner_lastw[0]): # if last word is not a tag, print
				ner_lastw = ner_lastw.strip('\n')# remove \n from the word
				word_dict['text'] = ner_lastw
				word_dict['NER_label'] = "O"
			if not isTag(pos_lastw[0]): # if last word is not a tag, print
				word_dict['POS_label'] = "O"
			outfile.write(json.dumps(word_dict, indent = 4, sort_keys=True))



if "__main__" == __name__:
	if JSON:
		OUT_FILE = OUT_FILE + ".json"
		TAG_INFO = False
	else:
		OUT_FILE = OUT_FILE + ".txt"

	code, FLAIR_MODEL, TRANSFORMERS_MODEL = prep.clean_modelName(ALGORITHM, TAGGER, LANGUAGE)
	if code == -1:
		print("Error with selected parameter.")
		#END
	else:
		if code != 0:# model not found
			prep.download(code, FLAIR_MODEL, TRANSFORMERS_MODEL)#download model if is accesible

		try:
			outfile = open(OUT_FILE, "w")
			file_cases(TRANSFORMERS_MODEL, FLAIR_MODEL, tagger_info=TAG_INFO) # tf, fl
		finally:
			outfile.close()
			print ("\nEND.\n")

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