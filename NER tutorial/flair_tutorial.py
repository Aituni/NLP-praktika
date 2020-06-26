# Source: https://github.com/flairNLP/flair/blob/master/resources/docs/TUTORIAL_2_TAGGING.md

from flair.data import Sentence
from flair.models import SequenceTagger #basic
# use a library to split into sentences
from segtok.segmenter import split_single #list
from flair.models import TextClassifier #emotions


""" 
	This function put tags in the input text, using flair, with the tagger model clas_type.
	And write the tags in the outfile the result. This funtion write extra info about tags.

	- string text: is the text that will be analyzed.
	- string clas_type: is the name of the tagger model that will be used. default:'ner'
	- _io.TextIOWrapper outfile: is the output file descriptor, where results will be writed.
"""
def tag_basic(text, clas_type, outfile):
	if not text:
		return

	tagger = SequenceTagger.load(clas_type)
	sentence = Sentence(text)

	# predict tags
	tagger.predict(sentence)

	# write in outfile sentence with predicted tags
	#outfile.write(sentence.to_tagged_string())

	#for entity in sentence.get_spans(clas_type): # imprime las etiquetas añadidas
	#    print(entity)
	dictionary = sentence.to_dict(tag_type=clas_type)
	for tag in dictionary.get('entities'):
		outfile.write(str(tag)+"\n")

""" 
	This function put tags in the input text, using flair, with the tagger model clas_type.
	And write the tags in the outfile the result. The main diference is that in this case, the input
	text can be	multiple sentences, one next to other, followed by dot (".").

	- string text: is the text that will be analyzed.
	- string clas_type: is the name of the tagger model that will be used. default:'ner'
	- _io.TextIOWrapper outfile: is the output file descriptor, where results will be writed.
"""
def tag_listSentences(text, clas_type, outfile):
	if not text:
		return

	# tokenizer se encarga de hacer las separaciones de los puntos etc.
	sentences = [Sentence(sent, use_tokenizer=True) for sent in split_single(text)] 

	# predict tags for list of sentences
	tagger: SequenceTagger = SequenceTagger.load(clas_type)
	tagger.predict(sentences)

	# iterate through sentences and outfile.write predicted labels
	#for sentence in sentences:
	#    outfile.write(sentence.to_tagged_string()+"\n")
	for sentence in sentences:
		if clas_type == 'ner':
			dictionary = sentence.to_dict(tag_type=clas_type) #imprimir las etiquetas añadidas con +info
			for tag in dictionary.get('entities'):
				outfile.write(str(tag)+"\n")
			outfile.write("\n")
		else:
			outfile.write(sentence.to_tagged_string()+"\n")

""" 
	This function analyze the input text, using flair, with the classifier clas_type.
	And write in the outfile the result.

	- string text: is the text that will be analyzed.
	- string clas_type: is the name of the classifier that will be used. default:'sentiment'
	- _io.TextIOWrapper outfile: is the output file descriptor, where results will be writed.
"""
def clas_emotions(text, clas_type, outfile):
	if not text:
		return

	# load tagger
	classifier = TextClassifier.load(clas_type)

	# predict for example sentence
	sentence = Sentence(text)
	classifier.predict(sentence)

	# check prediction
	outfile.write(sentence.to_plain_string())

	"""
	Downloaded models:
	- pos-multi: Part of speech (verb, noun, etc.), multiple languages (English, German, French,
		 Italian, Dutch, Polish, Spanish, Swedish, Danish, Norwegian, Finnish and Czech)
	- ner: 4-class Named Entity Recognition, english model.
	- sentiment: text classification, [positive, negative] sentiment. English model.
	- frame: Semantic Frame Detection (experimental). Makes a distinction between two different
			 meanings of the same word.		(Error with windows paths)
	"""