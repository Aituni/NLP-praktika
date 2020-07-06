import flair_tagging as fl
import transformer_tagging as tf
import preparations as prep

IN_FILE = "../tests/Input/english_text.txt"  # contain the sentences that we want to analyze. DO WRITE FORMAT
OUT_FILE = "../tests/Output/CoNLL-en_OUT" # is the file where the results will be writed. DO NOT WRITE FORMAT (.txt, ...)
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
True = print more info for each word (NER, POS, Chunking) in json format.
False = print chosen tag in TAGGER in txt format.
"""
JSON = False

"""
True = print few info about the tagger
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


if "__main__" == __name__:
	if JSON:
		OUT_FILE = OUT_FILE + ".json"
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