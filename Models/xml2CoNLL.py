#!/usr/bin/python3
import glob
from bs4 import BeautifulSoup
from segtok.segmenter import split_single #list # use a library to split into sentences

ENCODING = 'utf8'#'iso8859_15'

"""
Este script ha sido usado para transformar los archivos de 
TimeBank y TempEval3 en xml/tml a formato CoNLL .tsv.
Tanto para los ficheros de entrenamiento como para los de prueba.
"""

def parseXML(filename):
	f= open(filename, "r", encoding=ENCODING)
	contents = f.read()
	soup = BeautifulSoup(contents, 'xml')

	results = ""

	for elem in soup.find_all(True):
		nameTag = elem.name
		text = elem.text
		if nameTag == 'TIMEX3': # por cada tag timex3 encontrado:
			result = text.replace('\n', '')
			if result:
				found = results.find(result)
				if found == -1:# not found
					results = results + result
				else: #found
					result = " <TIME " + result + " > "
					results = results.replace(text, result)

		elif nameTag != 'DCT' and nameTag != 'TimeML' and nameTag != 'DOCID':
			if nameTag != 'EXTRAINFO' and nameTag != 'TITLE' and nameTag != 'LASTEXTRAINFO':
				result = text.replace('\n', '')
				if result: 
					results = results + " " + result

		elif nameTag == 'DCT': #ANCLA TEMPORAL DEL DOCUMENTO
			result = text.replace('\n', '')
			if result: 
				results = results + " " + result

	return(results)

def insert_tags(text):
	resul = []
	topen = False #tag open
	text = text.replace('\n', '')
	text = text.split(" ")
	separador = "\t"
	first_dot = True

	for word in text:
		if word:
			if topen:
				if not first_dot:
					word_tag = word_tag + separador + "O\n\n"
					first_dot = True
					resul.append(word_tag) # los puntos
				if first:
					word_tag = word + separador + "B-TIME\n"
					first = False
				else:
					word_tag = word + separador + "I-TIME\n"
			elif word == ".":
				if first_dot:
					word_tag = word 
					first_dot = False
				else:
					word_tag = word_tag + word
			else:
				if not first_dot:
					word_tag = word_tag + separador + "O\n\n"
					first_dot = True
					resul.append(word_tag) # los puntos

				word_tag = word + separador + "O\n"
			
			if first_dot:
				resul.append(word_tag)
				if word == "<TIME":
					topen = True
					first = True
					resul.pop()
				elif word == ">":
					topen = False
					resul.pop()
	if not first_dot:
		resul.append(word_tag + separador + "O\n")
	return resul

def noTags_test(text):
	resul = []
	topen = False #tag open
	text = text.replace('\n', '')
	text = text.split(" ")
	for word in text:
		if word:
			if word != "<TIME" and word != ">":
				resul.append(word+"\n")

	return resul

def main(outfile): 

	file_list = glob.glob('./Test/EN/tagged/*.tml')# Poner aqui el nombre de la carpeta con los *.tml
	for file in file_list:
		print(file)
		# parse xml file 
		try:
			text = parseXML(file) # devuelve texto con las partes temporales marcadas entre '<TIME' y '>'
			frases = split_single(text) # separador de frases + separador manual (mediante puntos)
			for frase in frases:
				frase = frase.replace(".", " . ").replace(",", " , ")
				#text = noTags_test(frase)
				text = insert_tags(frase)
				for fragment in text:
					outfile.write(fragment)	
					if fragment == "\n":
						separado = True
					else: 
						separado = False
				if not separado:
					outfile.write("\n")
		except UnicodeDecodeError:
			print('wrong file: ' + file + "\n error: "+error+'\n')
	
if __name__ == "__main__": 
	out = open('./EN_test.tsv', 'w', encoding=ENCODING)# poner aqui el nombre deseado para el archivo de salida
	# calling main function 
	main(out) 
	out.close()
