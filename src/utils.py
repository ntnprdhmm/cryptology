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

def binary_to_utf8(b):
    """ Convert binary text to uncode text (utf-8)
    """
    block_size = 8
    # start by cutting the text in blocks of 8 bits
    # then, convert each block from binary to decimal and from decimal to char
    # join the results
    return ''.join([chr(int(c, 2)) for c in list(b[i:i+block_size] for i in range(0, len(b), block_size))])

def binary_sum(a, b):
	""" Sum the binary numbers passed in parameters as strings
	"""
	return bin(int(a, 2) + int(b, 2))[2:]

def binary_xor(a, b):
	""" xor the binary numbers passed in parameters as strings
	"""
	return bin(int(a, 2) ^ int(b, 2))[2:]
