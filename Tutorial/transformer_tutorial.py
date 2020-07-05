# Source: https://github.com/huggingface/transformers/blob/master/notebooks/03-pipelines.ipynb

from transformers import pipeline

""" 
	This function put tags in the input text, using transformers, with the tagger model clas_type.
	And write in the outfile the result. This funtion write extra info about tags.

	- string text: is the text that will be analyzed.
	- string clas_type: is the name of the tagger model that will be used. default:'ner'
	- _io.TextIOWrapper outfile: is the output file descriptor, where results will be writed.
"""
def tag_basic(text, clas_type, outfile):
	# load tagger
	classifier = pipeline(clas_type)
	# check prediction
	dictionary = classifier(text)
	for word in dictionary:
		outfile.write(str(word)+"\n")


	"""
	Downloaded models:
	- pos-multi: Part of speech (verb, noun, etc.), multiple languages (English, German, French,
		 Italian, Dutch, Polish, Spanish, Swedish, Danish, Norwegian, Finnish and Czech)
	- ner: 4-class Named Entity Recognition, english model.
	- sentiment-analysis: text classification, [positive, negative] sentiment. English model.
	- frame: Semantic Frame Detection (experimental). Makes a distinction between two different meanings of the same word.
			(Error with windows paths)
	"""