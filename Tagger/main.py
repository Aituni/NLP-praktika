import flair_tagging as fl
import transformer_tagging as tf
import preparations as prep
import json
import sys

"""
	void file_cases(..):

	This function analyze the sentences of 'inFile', with selected 'tf_tagger' and 'fl_tagger'.
	The results will be writed on the 'outFile', with chosen format in 'json'

	Parameters:
		File inFile: Is the file where sentences will be readed

		File outFile: Is the file where sentences will be writed, with the results

		Bool json: Is the output format. True value, will make output be writed in json format.
					False, will make output be writed in tsv format with CoNLL style.

		String tf_tagger: model name or path for tagging or classification using transformers.
							put	empty string ("") if you dont want to clasify with transformers.
		String fl_tagger: model name or path for tagging or classification using flair.
							put	empty string ("") if you dont want to clasify with flair.
"""
def file_cases(inFile, outFile, json, tf_tagger, fl_tagger, tagger_info=True):
	
	if tagger_info:
		if tf_tagger:
			outFile.write("Tagger (transformers): "+tf_tagger+ "\n")
		if fl_tagger:
			outFile.write("Tagger (flair): "+fl_tagger+ "\n")

	# Leemos el texto
	text = inFile.read()

	if tf_tagger: #TODO:
		if tagger_info:
			outFile.write("TRANSFORMERS: \n\n")
		tf.tag_basic(text, tf_tagger, outFile)

	if fl_tagger:# with flair
		if tagger_info:
			outFile.write("\nFLAIR: \n\n")
		if json:
			# to add more taggers, just add tagger name to 'json_taggers' array in settings.py
			results = []
			taggers = load_appConfig()['json_taggers']
			for tagger in taggers:
				results.append(fl.tag_listSentences(text, tagger))
			print_json(outFile, results, taggers)
		else:
			sentences = fl.tag_listSentences(text, fl_tagger)
			#print(sentences[0])
			print_CoNLL(outFile, sentences, fl_tagger)
"""
	Bool isTag(word):
	Return True only if the given 'word' is a tag. else return False.
"""
def isTag(word):
	return word[0] == '<'

def load_appConfig():
	file = open(APP_PATH+'settings.json', 'r')
	config = json.load(file)
	file.close()
	return config
"""
	Array({}) getWordDictList(...):

	return an updated dictList, with the new words and tags in 'word_list' and missing in dictList. 
	If you have multiple tagged sentences for the same sentence but different tags,
	you can use the same dictList to include the tags to each word.

	Format:
		dictList: each dictionary have one word with key 'text'. And one or more taggs for that word,
					with each tag the key '<tagger>+"_label"'.

	Parameters:
		Array({}) dictList: Is an array of dictionarys, where each dictionary 
						have one word and the tags for that word.
						Example: [{"ner_label": "<E-PER>", "text": "Washington"},
								  {"ner_label": "<B-PER>", "text": "George"}]
		Array(String) word_list: Is an array of words. Is the tagged sentence splited by white spaces.
					     Where each value can be one word or a tag. Each tag is next to their word.

		String tagger: Is the tagger used to analize word_list sentence. It will be used to identify each tag type.
"""
def getWordDictList(dictList, word_list, tagger):
	i=0#word+tags
	j=0#word
	# for each word in word_list. each itearation 
	# we put 2 words 'act' and 'nextw' which could be a tag.
	while i+1 < len(word_list):
		new_word = False
		if len(dictList) <= j: #in 'dictList' the actual word is missing
			dictList.append({})# new word 
			new_word = True

		act=word_list[i]
		nextw=word_list[i+1]
		word_dict = dictList[j]

		if new_word:
			word_dict['text'] = act
		if isTag(nextw[0]): 
			word_dict[tagger+'_label'] = nextw # nextw is a tag
			i+=1
		else:
			word_dict[tagger+'_label'] = "O" # not tag found -> Other tag
		i+=1
		j+=1

	lastw=word_list[-1]
	if not isTag(lastw[0]): # if last word is not a tag, print
		if len(dictList) <= j:
			dictList.append({})# new word
			new_word = True
		word_dict = dictList[j]
		if new_word:
			word_dict['text'] = lastw
		word_dict[tagger+'_label'] = "O" # not tag found -> Other tag
	return dictList

"""
	void print_CoNLL(...):

	print in outFile, the results with CoNLL style (word+"  "+tag).
	IMPORTANT: This function only print one tag type, indentified with 'tagger' parameter.

	Parameters:
		File outFile: is the file where results will be writed.

		Array(String) sentences: is an array of sentences, where each value
					 			 is a sentence with tags next to their word.

		String tagger: Is the tagger used to analize given sentences. 
						It will be used to identify each tag type.

"""
def print_CoNLL(outFile, sentences, tagger):
	# iterate through sentences and outFile.write predicted labels
	for sentence in sentences:
		dictList = []
		tagged_sent = sentence.to_tagged_string()
		tagged_sent = tagged_sent.strip('\n\t') # remove special characters (\n\t)
		word_list = tagged_sent.split(" ") # split by white spaces
		dictList = getWordDictList(dictList, word_list, tagger)

		for word_dict in dictList:
			text = word_dict['text']
			tag = word_dict[tagger+'_label']
			outFile.write("{:>18}\t{:<8}\n".format(text, tag))	

"""
	void print_json(...):

	print in outFile, the results in json format.

	Parameters:
		File outFile: is the file where results will be writed.

		Array(Array(String)) sentences_listOfModels: is an array of sentences, where each value
									 			 is a list of sentences tagged with one different tagger,
									 			 where each sentence have tags next to their word. 
									 			 *

		Array(String) taggers: Is an array of strings, with the different taggers
							   used to analize given sentences. 
							   It will be used to identify each tag type.
							   *
	* NOTE: There are in the same position the tagger and the sentences tagged with that tagger. 
			For example:
				sentences_listOfModels[0] = (sentences tagged with 'ner')
				tagger[0] = 'ner'

"""
def print_json(outFile, sentences_listOfModels, taggers):
	word_dict = {}
	
	# iterate through sentences and outFile.write predicted labels
	# every model have the same sentences, same words, different tags
	for i in range(len(sentences_listOfModels[0])):#for sentence
		dictList = []
		for model in range(len(taggers)):# for model

			model_sentences = sentences_listOfModels[model]#modelo "model"
			sentence = model_sentences[i]#sentencia i-esima
			tagged_sent = sentence.to_tagged_string()
			tagged_sent = tagged_sent.strip('\n\t')#limpiar saltos de linea y tabs
			word_list = tagged_sent.split(" ")
			# son las mismas frases por lo que el numero de palabras son las mismas. solo varian las etiquetas
			# cada diccionario corresponde a una palabra
			dictList = getWordDictList(dictList, word_list, taggers[model])

		for word_dict in dictList:
			outFile.write(json.dumps(word_dict, indent = 4, sort_keys=True))


"""
	void main(...):
		main function. 
		It will analyze given document ('in_filename') with choosen settings in the parameters
		and print results in 'out_filename' document.

		Given document path is defined by an global variable. Default: "../tests/Input/" 
		Output document path is defined by an global variable. Default: "../tests/Output/" 

	Parameters:
		String in_filename: Is the name of the file that contain the sentences that we want to analyze. DO WRITE FORMAT
					default: 'english_text.txt'

		String out_filename: Is the file name where the results will be writed. DO NOT WRITE FORMAT (.txt, ...)
					  		 if JSON = True, the file will be in 'json' format, else 'tsv'.
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
		Bool json: outfile format (json or tsv).
				Options:   	True = print more info for each word (NER, POS, Chunking) in json format. ('only en')
					   		False = print chosen tag in 'tagger' in tsv format, CoNLL style.
					default = False
		Bool tag_info: Used Tagger info.
				Options:   	True = print few info about the tagger (ONLY WITH JSON = False)
					   		False = Only print words and tags.
					default = False
"""
def main(
	in_filename = 'english_text.txt',
	out_filename = '1',
	algorithm = 'F',
	language = 'en',
	tagger = 'ner',
	json = False,
	tag_info = False):

	in_filePath = in_filename
	if json:
		out_filePath = out_filename + ".json"
		tag_info = False # can not insert info in json format
	else:
		out_filePath = out_filename + ".tsv"

	code, flair_model, transformers_model = prep.obtain_model(algorithm, tagger, language)
	if code[0] == -1:#ERROR
		print("Error with selected parameter.")
		#END
	elif code[0] != 0: #not found
		print(code, flair_model, transformers_model)
	else:
		try:
			outFile = open(out_filePath, "w")
			inFile = open(in_filePath, "r")
			file_cases(inFile, outFile, json, transformers_model, flair_model, tagger_info=tag_info) # tf, fl
		finally:
			outFile.close()
			inFile.close()
		print ("\nEnded tagging process.\n")


if "__main__" == __name__:
	#################
	### MAIN CALL ###
	#################
	"""
	main(	
			in_filename = "../tests/Input/eusk_text.txt", # do write format
			out_filename = "../tests/Output/CoNLL-eu_TRFM", 	  # do NOT write format
			algorithm = 'F',	 #	'F' = Flair(Recommended) 	'T' = Transformers (experimental) 		'FT' = Both (experimental)
			language = 'eu',	#  'eu' = euskera		'es' = español		'en' = english		'ca' = catalan		'gl' = gallego
			tagger = '../Models/trained_models/Transformer/NER/eu/best-model.pt',		# 'ner'= (all languages)		'pos' = (only English and Spanish)		'chunk' = (only English)
			json = False,	# outfile format.
			tag_info = True)  # info about tagger
	"""
	
	if len( sys.argv ) != 8 and len( sys.argv ) !=1:
		print( "Uso: {} <in_filename> <out_filename> <algorithm> <language> <tagger> <json> <tag_info>".format( sys.argv[0] ) )
		exit( 1 )
	elif len( sys.argv ) == 8:
		main(	
			in_filename = sys.argv[1], # do write format
			out_filename = sys.argv[2], 	  # do NOT write format
			algorithm = sys.argv[3],	 #	'F' = Flair(Recommended) 	'T' = Transformers (experimental) 		'FT' = Both (experimental)
			language = sys.argv[4],	#  'eu' = euskera		'es' = español		'en' = english		'ca' = catalan		'gl' = gallego
			tagger = sys.argv[5],		# 'ner'= (all languages)		'pos' = (only English and Spanish)		'chunk' = (only English)
			json = sys.argv[6] == "True",	# outfile format.
			tag_info = sys.argv[7])  # info about tagger

	#END


"""
----------------------------------------------------------------------------------------------------------------------
For text classification is needed other functions. At the moment does not work with this script. Only text tagging works 
(for example: 'ner', 'pos' or 'pos-multi')

Some interesting models (flair):
- pos-multi: Part of speech (verb, noun, etc.), multiple languages (English, German, French,
	 Italian, Dutch, Polish, Spanish, Swedish, Danish, Norwegian, Finnish and Czech)
- ner: 4-class Named Entity Recognition, english model.
- sentiment: text classification, [positive, negative] sentiment. English model.
- frame: Semantic Frame Detection (experimental). Makes a distinction between two different meanings of the same word.
		(Error with windows paths)


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