#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This module contains many helper functions
"""

import sys
import os

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
