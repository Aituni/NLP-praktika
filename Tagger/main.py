import sys, os
import preparations as prep
import file_tagging as ftag
import json

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
				Options:	'F' = Flair 	'T' = Transformers (experimental) 
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
	
	config = load_appConfig()

	in_filePath = in_filename
	if json:
		out_filePath = out_filename + ".json"
		tag_info = False # can not insert info in json format
	else:
		out_filePath = out_filename + ".tsv"

	code, flair_model = prep.obtain_model(algorithm, tagger, language, config)
	if code[0] == -1:#ERROR
		print("Error with selected parameter.")
		#END
	elif code[0] != 0: #not found
		print(code, flair_model)
	else:
		try:
			outFile = open(out_filePath, "w")
			inFile = open(in_filePath, "r")
			if ftag.file_cases(inFile, outFile, json, flair_model, config, tagger_info = tag_info) < 0:
				#ERROR
				outFile.close()
				os.remove(out_filePath)
				
		finally:
			if outFile:
				outFile.close()
			if inFile:
				inFile.close()
		print ("\nEnded tagging process.\n")

def load_appConfig():
	file = open('settings.json', 'r')
	config = json.load(file)
	file.close()
	return config

if "__main__" == __name__:
	#################
	### MAIN CALL ###
	#################

	main(	
			in_filename = "../tests/Input/english_text.txt", # do write format
			out_filename = "../tests/Output/flair_en", 	  # do NOT write format
			algorithm = 'Flair',
			language = 'en',	#  'eu' = euskera		'es' = español		'en' = english		'ca' = catalan		'gl' = gallego
			tagger = '../Models/trained_models/Flair/time/en/best-model.pt',		# 'ner'= (all languages)		'pos' = (only English and Spanish)		'chunk' = (only English)
			json = False,	# outfile format.
			tag_info = True)  # info about tagger
	
	if len( sys.argv ) != 8:
		print( "Uso: {} <in_filename> <out_filename> <algorithm> <language> <tagger> <json> <tag_info>".format( sys.argv[0] ) )
		exit( 1 )
	elif len( sys.argv ) == 8:
		if type(sys.argv[6]) == 'bool' and type(sys.argv[7]) == 'bool':
			js = sys.argv[6]
			tag = sys.argv[7]
		else:
			js = sys.argv[6] == "True"
			tag = sys.argv[7] == "True"

		main(	
			in_filename = sys.argv[1], # do write format
			out_filename = sys.argv[2], # do NOT write format
			algorithm = sys.argv[3],	 #	Flair(Recommended) 	Transformers (experimental) 
			language = sys.argv[4],	#  'eu' = euskera		'es' = español		'en' = english		'ca' = catalan		'gl' = gallego
			tagger = sys.argv[5],		# 'ner'= (all languages)		'pos' = (only English and Spanish)		'chunk' = (only English)
			json = js,	# outfile format.
			tag_info = tag)  # info about tagger

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