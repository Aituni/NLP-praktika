# info Source: https://github.com/flairNLP/flair/blob/master/resources/docs/TUTORIAL_2_TAGGING.md

from flair.data import Sentence
from flair.models import SequenceTagger #basic
from segtok.segmenter import split_single #list # use a library to split into sentences
#from flair.models import TextClassifier #emotions
#from flair.embeddings import TransformerWordEmbeddings#transformers

""" 
	tag_listSentences(...):
		This function put tags in the input text, using flair, with the tagger model 'clas_type'.
		And return a list of tagged sentences.The input	text can be multiple sentences, 
		one next to other, followed by dot (".").

	Parameters:
	- string text: is the text that will be analyzed.
	- string clas_type: is the name of the tagger model that will be used. default:'ner'

	return [sentence,s...] : list of tagged (flair) sentences
"""
def tag_listSentences(text, clas_type):

	if not text:
		return

	sentences = [] 
	for sent in split_single(text):
		# meter solo aquellas frases que contengan texto.
		if sent:
			# tokenizer se encarga de hacer las separaciones de los puntos etc.
			sentences.append( Sentence(sent, use_tokenizer=True) )

	# predict tags for list of sentences
	tagger: SequenceTagger = SequenceTagger.load(clas_type)
	tagger.predict(sentences)

	return sentences

	"""
	Interesting models:
	- pos-multi: Part of speech (verb, noun, etc.), multiple languages (English, German, French,
		 Italian, Dutch, Polish, Spanish, Swedish, Danish, Norwegian, Finnish and Czech)
	- ner: 4-class Named Entity Recognition, english model.
	"""

"""
from flair.embeddings import TransformerWordEmbeddings
embeddings = TransformerWordEmbeddings('xlm-roberta-base', fine_tune=True)
print(tag_listSentences( "Gaur goizean, Iker Tolosarekin batera Tolosara joan dira inauteriak ospatzera. Atzo Kattalin iphone bat erosi zun Apple denda ofizialean.", 
	"../Models/trained_models/Transformer/NER/eu/best-model.pt"))
"""
