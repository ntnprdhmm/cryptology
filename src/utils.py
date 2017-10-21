def read_file_per_block(filepath, k=1):
	""" Read a file block per block of size 'n'
		where n = k*8
	"""
	f = open(filepath)
	while True:
		data = f.read(k * 8)
		if not data:
			break
		print(data)


def utf8_to_binary(text):
    """ Convert unicode (utf-8) text to binary
    """
    return ''.join("{0:08b}".format(ord(c)) for c in text)
