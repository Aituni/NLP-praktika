import flair_tagging as fl
import transformer_tagging as tf

IN_FILE = "../tests/Input/CoNLL-eu.txt"  # contain the sentences that we want to analyze.
OUT_FILE = "../tests/Output/CoNLL-eu_OUT.txt" # is the file where the results will be writed

# put empty string ("") if you dont want to clasify with transformers.
FLAIR_MODEL = '../MODEL_NER-eusk/trained_models/from_epub/best-model.pt'
TRANSFORMERS_MODEL = ''
TAG_INFO = False


"""
This function analyze the sentences of the IN_FILE, with transformers
using tf_tagger and flair using fl_tagger model. The results will be 
writed on the OUT_FILE, CoNLL styloutfile.write(sentence.to_tagged_string()).

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

		#print("text: "+text)

		if tf_tagger:
			if tagger_info:
				outfile.write("TRANSFORMERS: \n\n")
			tf.tag_basic(text, tf_tagger, outfile)

		if fl_tagger:
			if tagger_info:
				outfile.write("\nFLAIR: \n\n")
			fl.tag_listSentences(text, fl_tagger, outfile)

	file.close()


if "__main__" == __name__:
    
	try:
		outfile = open(OUT_FILE, "w")
		file_cases(TRANSFORMERS_MODEL, FLAIR_MODEL, tagger_info=TAG_INFO) # tf, fl
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