import flair_tagging as fl
import transformer_tagging as tf
import json

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
							
		String fl_tagger: model name or path for tagging or classification using flair.

		Bool tagger_info: model's name will be printed, and the style will be prettier

"""
def file_cases(inFile, outFile, json, fl_tagger, settings, tagger_info=True):
	
	if tagger_info:
		if fl_tagger.find("/") != -1:
			taggername = fl_tagger.split("/")[-3:]
			taggername = "/".join(taggername)
		else:
			taggername = fl_tagger

		outFile.write("Tagger: " + taggername + "\n")
		outFile.write("\nRESULTS: \n\n")

	# Leemos el texto
	text = inFile.read()
		
	if json:
		# to add more taggers, just add tagger name to 'json_taggers' array in settings.py
		results = []
		taggers = settings['json_taggers']
		for tagger in taggers:
			sentences = fl.tag_listSentences(text, tagger)
			if not sentences:
				return -1
			results.append(sentences)
		print_json(outFile, results, taggers)
	else:
		sentences = fl.tag_listSentences(text, fl_tagger)
		if not sentences:
			return -1
		print_CoNLL(outFile, sentences, fl_tagger, tagger_info)
	return 0
"""
	Bool isTag(word):
	Return True only if the given 'word' is a tag. else return False.
"""
def isTag(word):
	return word[0] == '<'

"""
	Array({}) getWordDictList(...):

	return an updated dictList, with the new words and tags in 'word_list' missing in dictList. 
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

	print in outFile, the results with CoNLL style (word+"/t"+tag).
	IMPORTANT: This function only print one tag type, indentified with 'tagger' parameter.

	Parameters:
		File outFile: is the file where results will be writed.

		Array(String) sentences: is an array of sentences, where each value
					 			 is a sentence with tags next to their word.

		String tagger: Is the tagger used to analize given sentences. 
						It will be used to identify each tag type.

		Bool tagger_info: model's name will be printed, and the style will be prettier

"""
def print_CoNLL(outFile, sentences, tagger, tagger_info):
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
			if tagger_info:
				outFile.write("{:>18}\t{:<8}\n".format(text, tag))
			else:
				outFile.write("{}\t{}\n".format(text, tag))

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
