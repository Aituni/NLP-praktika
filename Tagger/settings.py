import json

class config:

	VERSION = 0.21

	# key : "explicacion"
	params = {

		# BOOLEANS
		'json' : {
			True : '(.json) Print tags in json file (only english using Flair)',
			False : '(.tsv) Print in CoNLL format (tsv)'
			
		},

		'tag_info' : {
			True : 'Yes. Write extra info about tagger (only txt)',
			False : 'No. Do not write extra info about tagger (only txt)'
		},

		'algorithm' : {
			'F' : 'Flair (Recommended)',
			'T' : 'Transformers (only ner, Experimental)',
			'FT' : 'Flair and Transformers (only ner, Experimental)'
		},

		'tagger' : {
			'ner' : '(ner) Named Entity Recognition',
			'pos' : '(pos) Part Of Speech (spanish and english)',
			'chunk' : 'Chunking (only english)'
		},

		'language' : {
			'eu' : 'Euskera',
			'es' : 'Español',
			'en' : 'English',
			'ca' : 'Catalan',
			'ga' : 'Gallego'
		}	
	}

	## PATHS

	paths = { 'in'  : "../tests/Input/",
	 		  'out' : "../tests/Output/" }

	## json

	json_taggers = ['ner', 'pos', 'chunk']

	## demo

	test_files = ['english_text.txt', 'eusk_text.txt']

	## ALL THE CONFIG (to export to json)

	ALL = { 
		'version' : VERSION,
		'params' : params,
		'paths' : paths,
		'json_taggers' : json_taggers,
		'test_files' : test_files
		}

def make_json():
	file = open('settings.json', 'w')
	file.write(json.dumps(config.ALL, indent = 4, sort_keys=True))
	file.close()

#for opt in config.params['json']: # pruebas
#	print(config.params['json'][opt])
