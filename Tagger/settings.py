import json, sys
# this script makes settings.json file running "python3 settings.py"
# you can see the version using "python3 settings.py v"
class config:

	# UPDATE AND EXECUTE AFTER ANY CHANGE 
	VERSION = 0.335

	# key : "explicacion"
	params = {

		# BOOLEANS
		'json' : {
			True : '(.json) Print tags in json file (only english using Flair)',
			False : '(.tsv) Print in CoNLL format'
			
		},

		'tag_info' : {
			True : 'Yes. Write extra info about tagger (only tsv)',
			False : 'No. Do not write extra info about tagger (only tsv)'
		},

		'algorithm' : {
			'Flair' : 'Flair (Recommended)',
			'Transformers' : 'Transformers (only ner, Experimental)',
		},

		'tagger' : {
			'ner' : '(ner) Named Entity Recognition',
			'pos' : '(pos) Part Of Speech (spanish and english)',
			'chunk' : '(Chunk) (only english)',
			'manual' : '(manual) Use your own model'
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
				'server_out': "../tests/srvOUT/",
				'tests': "../tests/Input/" }

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
