import os
from flair.data import Sentence
from flair.models import SequenceTagger #basic

def analyze(text):
	sentences = Sentence(text)
	tagger: SequenceTagger = SequenceTagger.load('ner')
	tagger.predict(sentences)
	print(sentences)

if "__main__" == __name__:
	if os.fork(): 
		print("proceso padre")
		analyze("George Washington went to Washington .") # works well
	else:
		print( "proceso hijo" )
		analyze("He had a look at different hats in Mora .") # Error
		# RuntimeError: Cannot re-initialize CUDA in forked subprocess.
		# To use CUDA with multiprocessing, you must use the 'spawn' start method
