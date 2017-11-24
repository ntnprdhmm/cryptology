import sys

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
    initial_len = len(a)
    return bin(int(a, 2) ^ int(b, 2))[2:].zfill(initial_len)

def decimal_to_binary(n, l=None):
	""" n: the decimal value
		l: the number of bits for the binary representation
	"""
	b = bin(n)[2:]
	if l != None:
		b = b.zfill(l)
	return b

def binary_to_decimal(n):
    """ Convert a number from binary to decimal
    """
    return int(n, 2)

def print_loading(step, steps):
    sys.stdout.write("\rloading: %d%%" % ((step/steps)*100))
    sys.stdout.flush()
