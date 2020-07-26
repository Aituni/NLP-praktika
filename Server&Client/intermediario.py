
class Command:
	File, Size, Parameters, Update, Close, Options, Version = ("FLE", "SZE", "PRM", "UPD", "CLS", "OPT", "VRS")
	#resp
	OK, Error = ('OK+', 'ER-')
	port = 50015
	coding = "UTF-8"

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

#sin modificar todavia
def recvall( s, size ):
	message = b''
	while( len( message ) < size ):
		chunk = s.recv( size - len( message ) )
		if chunk == b'':
			raise EOFError( "Connection closed by the peer before receiving the requested {} bytes.".format( size ) )
		message += chunk
	return message

def download_file(s):
	msg = recvline(s).decode(Command.coding) # SZE12345#filename
	msg = msg[3:].split("#")
	size = int(msg[0])
	filename = msg[1]

	s.sendall("{}\r\n".format(Command.OK).encode(Command.coding)) # OK+\r\n

	downld_data = recvall(s,size)# file data
	outfile = open(filename, "wb")
	outfile.write(downld_data)
	outfile.close()

	print("\n Downloaded '{}' file with the results.".format(filename))
	return filename

def upload_file(s, path):

	file = open(path, "rb")
	contenido = file.read()
	size = len(contenido)
	filename = path.split("/")
	filename = filename[-1]

	msg = "{}{}#{}\r\n".format(Command.Size, size, filename) # SZE1234#filename\r\n
	s.sendall(msg.encode(Command.coding))
	#TODO: controlar error
	resp = recvline(s).decode(Command.coding) # OK+ or ER-

	s.sendall(contenido) # file
	file.close()
