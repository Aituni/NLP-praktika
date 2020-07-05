from time import time
import flair_tutorial as fl
import transformer_tutorial as tf

IN_FILE = "../tests/Input/test.txt"  # contain the sentences that we want to analyze.
OUT_FILE = "../tests/Output/test-en_Output.txt" # is the file where the results will be writed

# put empty string ("") if you dont want to clasify with transformers.
FLAIR_MODEL = 'ner'
TRANSFORMERS_MODEL = ''

"""
(IN_FILE) FILE FORMAT:
First of all, The number of examples you want to analyze.
If you want to analyze all of them put 0.
Then after one empty new line, put the examples.
Between every example, put new empty line.
"""

"""
This function analyze the sentences of the IN_FILE, with transformers
using tf_tagger and flair using fl_tagger model. The results will be 
writed on the OUT_FILE.

String tf_tagger: model name for tagging or classification using transformers.
					put	empty string ("") if you dont want to clasify with transformers.
String fl_tagger: model name for tagging or classification using flair.
					put	empty string ("") if you dont want to clasify with flair.
"""
def file_cases(tf_tagger, fl_tagger):
	file = open(IN_FILE, "r")
	if tf_tagger:
		outfile.write("Tagger (transformers): "+tf_tagger+ "\n")
	if fl_tagger:
		outfile.write("Tagger (flair): "+fl_tagger+ "\n")

	# Número de ejemplos
	nTestCases = int(file.readline())
	if nTestCases == 0: 
		nTestCases = float('inf')
	k=0
	while k < nTestCases:

		# Lee la linea vacia
		file.readline()
		# Leemos el texto
		text = file.readline()
		if text == "":
			if nTestCases != float('inf'):
				print ("\nNOT FOUND MORE EXAMPLES.\n")
			break

		outfile.write("\n------------ Caso "+str(k)+" ------------\n")
		outfile.write("text: "+text+"\n")

		if tf_tagger:
			outfile.write("TRANSFORMERS: \n\n")
			t1 = time()
			tf.tag_basic(text, tf_tagger, outfile)
			outfile.write("\n+++ (transformer) time: "+str(time()-t1)+"\n")

		if fl_tagger:
			outfile.write("\nFLAIR: \n\n")
			t1 = time()
			fl.tag_listSentences(text, fl_tagger, outfile)
			outfile.write("\n+++ (flair) time: "+str(time()-t1)+"\n")

		"""
		t1 = time()
		clas_emotions(text, tagger)
		fl.outfile.write("\n+++ (emotions) time: "+str(time()-t1)+"\n")
		"""
		k += 1

	file.close()

"""
This function is to try manually different functions and texts 
using the tagger model. The output will be writed in the OUT_FILE. 
"""
def manual_cases(tagger):
	text = "En un lugar de la mancha de cuyo nombre no quiero acordarme yace el quijote. Junto a su fiel escudero sancho panza fueron a Malaga"

	outfile.write("\n-------- tagger: ("+ tagger +")\n")
	outfile.write("text: "+text+"\n\n")
	t1 = time()
	fl.tag_listSentences(text, tagger, outfile)
	outfile.write("\n\n+++ (list_sentences) time: "+str(time()-t1)+"\n")


if "__main__" == __name__:
    
	try:
		outfile = open(OUT_FILE, "w")
		file_cases(TRANSFORMERS_MODEL, FLAIR_MODEL) # tf, fl
		#manual_cases('pos-multi')
	finally:
		outfile.close()



	#IMPORTANT: for tagging and classification, may use different functions (change functions inside file_cases or manual_cases for it).

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