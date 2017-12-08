#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This module contains many helper functions
"""

import sys
import os
import math
import random

def bytes_to_int(bytes):
    result = 0

    for b in bytes:
        result = result * 256 + int(b)

    return result

def int_to_bytes(value, length):
    result = []

    for i in range(0, length):
        result.append(value >> (i * 8) & 0xff)

    result.reverse()

    return result

def read_file(filename, directory="assets", read_bytes=False):
    """ Read the content of the given asset

        Args:
            filename -- string -- the file to read
            directory -- string -- the directory name, at the project's root
            read_bytes -- boolean -- if True, read bytes

        return the content of the file
    """
    f = open(os.path.abspath(directory + "/" + filename), "rb" if read_bytes else "r")
    return f.read()

def read_file_bytes_block(filename, directory="assets", block_size=1024):
    """
        Read the content of the file in bytes, and add some padding if needed

        The padding respect the "ISO 10126" norm (random bytes, and the last
        bytes are the number of random bytes added for padding)

        Args:
            filename -- string -- the name of the file to read
            directory -- string -- the directory name, at the project's root
            block_size -- int -- the size of the blocks

        return a bytearray (the content of the file, padded if needed)
    """
    # read the content of the file in bytes
    content = list(read_file(filename, directory, True))
    # calculate the number of bytes needed to store the block size
    msb_index = len(str(bin(block_size)[2:]))
    padding_size_bytes = math.ceil(msb_index / 8)
    # calculate the padding size
    padding_size = (block_size // 8) - (len(content) % (block_size//8))
    # add padding (random bytes)
    for _ in range(0, padding_size - padding_size_bytes):
        content.append(random.randint(0, 255))
    # add padding (padding size bytes)
    binary_padding_size = str(bin(padding_size)[2:]).zfill(padding_size_bytes * 8)

    for i in range(padding_size_bytes):
        content.append(int(binary_padding_size[i*8:(i+1)*8], 2))

    return bytearray(content)

def write_file(filename, data):
    """ Write content in a file ('outputs' directory)

        Args:
            filename -- string -- the output file name
            data -- string -- the content to write in the file
    """
    f = open(os.path.abspath("outputs/" + filename), "w")
    f.write(data)
    f.close()

def list_to_string(l):
    """ Join all elements of the given list

        Args:
            l -- list

        return a string
    """
    return ','.join([str(v) for v in l])

def utf8_to_binary(text):
    """ Convert unicode (utf-8) text to binary

        Args:
            text -- string -- the text to convert

        return the binary value of text
    """
    return ''.join("{0:08b}".format(ord(c)) for c in text)

def binary_to_utf8(binary_text):
    """ Convert binary text to uncode text (utf-8)

        Args:
            binary_text -- string -- the binary string to convert

        return the utf-8 text
    """
    block_size = 8
    # start by cutting the text in blocks of 8 bits
    # then, convert each block from binary to decimal and from decimal to char
    # join the results
    return ''.join([chr(int(c, 2)) for c in \
                list(binary_text[i:i+block_size] for i in \
                    range(0, len(binary_text), block_size))])

def binary_sum(a, b):
    """ Sum the binary numbers passed in parameters as strings

        Args:
            a -- string
            b -- string

        return a + b in binary
	"""
    return bin(int(a, 2) + int(b, 2))[2:]

def binary_xor(a, b):
    """ xor the binary numbers passed in parameters as strings

        Args:
            a -- string
            b -- string

        return a ^ b in binary
    """
    initial_len = len(a)
    return bin(int(a, 2) ^ int(b, 2))[2:].zfill(initial_len)

def decimal_to_binary(n, l=None):
    """ Convert n from decimal to binary

        Args:
            n -- int -- the decimal value
    		l -- int -- the number of bits for the binary representation

        return the binary value of n
    """
    binary = bin(n)[2:]
    if l != None:
        binary = binary.zfill(l)
    return binary

def binary_to_decimal(n):
    """ Convert a number from binary to decimal

        Args:
            n -- string -- binary number

        return decimal value of n
    """
    return int(n, 2)

def print_loading(step, steps):
    """ Print a loader in the console

        Args:
            step -- int -- current step
            steps -- int -- total number of steps
    """
    sys.stdout.write("\rloading: %d%%" % ((step/steps)*100))
    sys.stdout.flush()
