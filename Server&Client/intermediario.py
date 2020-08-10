import json

class Command:
	File, Size, Parameters, Update = ("FLE", "SZE", "PRM", "UPD")
	Close, Version, Quantity, Model = ("CLS", "VRS", "QTY", "MDL")
	#resp
	OK, Error = ('OK+', 'ER-')

class Parameters:
	Port = 50010
	Coding = "UTF-8"

	Error = {
			0:" inserted value is not valid. insert valid one ",
			1:" document not processed correctly",
			2:" unknown Error",
			3:" error with client/server connection"
		 }

#devuelve el paquete recibido con el comando y sin la marca de fin.
def recvline( s, removeEOL = True ):
	line = b''
	CRreceived = False
	while True:
		c = s.recv( 1 )
		if c == b'':
			raise EOFError( "Connection closed by the peer before receiving an EOL." )
		line += c
		if c == b'\r':
			CRreceived = True
		elif c == b'\n' and CRreceived:
			if removeEOL:
				return line[:-2]
			else:
				return line
		else:
			CRreceived = False

def recvall( s, size ):
	message = b''
	while( len( message ) < size ):
		chunk = s.recv( size - len( message ) )
		if chunk == b'':
			raise EOFError( "Connection closed by the peer before receiving the requested {} bytes.".format( size ) )
		message += chunk
	return message

def download_file(s, outDir=''):
	
	msg = recvline(s).decode(Parameters.Coding) # SZE12345#filename
	msg = msg[3:].split("#")
	size = int(msg[0])
	filename = msg[1]

	downld_data = recvall(s,size)# file data
	outfile = open(outDir+filename, "wb")
	outfile.write(downld_data)
	outfile.close()

	print("\n Downloaded '{}' file.".format(filename))
	return filename

def upload_file(s, path):

	file = open(path, "rb")
	contenido = file.read()
	size = len(contenido)
	filename = path.split("/")
	filename = filename[-1]

	msg = "{}{}#{}\r\n".format(Command.Size, str(size), filename) 
	s.sendall(msg.encode(Parameters.Coding)) # SZE1234#filename\r\n

	s.sendall(contenido) # file
	file.close()
	print("\n File uploaded")

def isOK(msg):
	comand = msg[:3]
	rest = msg[3:]
	if comand == Command.OK:
		return True
	elif comand == Command.Error:
		try:
			code = int(rest)
			error = Parameters.Error[code]
		except:
			error = Parameters.Error[2]
		print(error)
		return False

def load_appConfig(directory=''):
	file = open(directory+'settings.json', 'r')
	config = json.load(file)
	file.close()
	return config

