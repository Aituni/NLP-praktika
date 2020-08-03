import json, sys

class config:

	VERSION = 0.3

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
			'Flair' : 'Flair (Recommended)',
			'Transformers' : 'Transformers (only ner, Experimental)',
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

	paths = { 	'server_in': "../tests/srvIN/",
				'server_out': "../tests/srvOUT/" }

	## json

	json_taggers = ['ner', 'pos', 'chunk']

	## demo

	test_files = ['english_text.txt', 'eusk_text.txt']

	## url

	url = {
		'Flair': {
			'ner':{
				'es':'',
				'en':''
			},
			'pos':{
				'en':''
			}
		}
	}

	## ALL THE CONFIG (to export to json)

	ALL = { 
		'version' : VERSION,
		'params' : params,
		'paths' : paths,
		'json_taggers' : json_taggers,
		'test_files' : test_files,
		'url' : url
		}

def make_json():
	file = open('settings.json', 'w')
	file.write(json.dumps(config.ALL, indent = 4, sort_keys=True))
	file.close()

def get_version():
	print(config.VERSION)

if "__main__" == __name__:
	if len( sys.argv ) == 2:
		if sys.argv[1] == "v":
			get_version()
		else:
			print( "Use: {} <v> or nothing else".format( sys.argv[0] ) )
	elif len( sys.argv ) == 1:
		make_json()
	else:
			print( "Use: {} <v> or nothing else".format( sys.argv[0] ) )
