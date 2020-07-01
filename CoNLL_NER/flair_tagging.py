# Source: https://github.com/flairNLP/flair/blob/master/resources/docs/TUTORIAL_2_TAGGING.md

from flair.data import Sentence
from flair.models import SequenceTagger #basic
# use a library to split into sentences
from segtok.segmenter import split_single #list
from flair.models import TextClassifier #emotions

""" 
	This function put tags in the input text, using flair, with the tagger model clas_type.
	And write the tags in the outfile the result with CoNLL style. The main diference is
	that in this case, the input text can be multiple sentences, one next to other, 
	followed by dot (".").

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
	for sentence in sentences:
		
		taged_sent = sentence.to_tagged_string()
		word_list = taged_sent.split(" ")
		#print(word_list)

		i=0
		while i+1 < len(word_list):
			act=word_list[i].strip('\n\t')
			nextw=word_list[i+1].strip('\n\t')
			if nextw[0] == '<': # is a tag
				outfile.write(act+" "+nextw+"\n")
				i+=1
			else:
				outfile.write(act+" O\n")
			i+=1

		lastw=word_list[-1]
		if lastw: # hay alguna palabra
			if lastw[0] != '<': # if last word is not a tag, print
				lastw=lastw.strip('\n')# remove \n from the word
				outfile.write(lastw+" O\n")

	"""
	Downloaded models:
	- pos-multi: Part of speech (verb, noun, etc.), multiple languages (English, German, French,
		 Italian, Dutch, Polish, Spanish, Swedish, Danish, Norwegian, Finnish and Czech)
	- ner: 4-class Named Entity Recognition, english model.
	"""