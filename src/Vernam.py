#!/usr/bin/env python3
# -*- coding:utf-8 -*-

""" This module contains the Vernam class
"""

import sys

from src import utils

class Vernam(object):
    """ Vernam cipher
    """

    @staticmethod
    def xor(plaintext, key):
        """ Using XOR, it's the same method to cipher and decipher

            Args:
                plaintext -- string -- the text to xor
                key -- string
    	"""
        # make sure the key is at least as big as the text
        if len(key) < len(plaintext):
            sys.exit("The key is smaller than the text")

        # convert both plaintext and key in binary
        binary_text = utils.utf8_to_binary(plaintext)
        binary_key = utils.utf8_to_binary(key)

        # ciphertext[i] = plaintext[i] xor key[i]
        ciphertext = ''.join([str(int(binary_text[i])^int(binary_key[i])) \
                              for i in range(len(binary_text))])

        return utils.binary_to_utf8(ciphertext)

    @staticmethod
    def cipher(plaintext, key):
        """ Cipher the plaintext using the key

            Args:
                plaintext -- string -- the text to cipher
                key -- string

            return the ciphertext
        """
        # make sure the key is at least as big as the text
        if len(key) < len(plaintext):
            sys.exit("The key is smaller than the text")

        return ''.join([chr((ord(plaintext[i]) + ord(key[i])) & 0xFF) \
                        for i in range(len(plaintext))])

    @staticmethod
    def decipher(ciphertext, key):
        """ Decipher the ciphertext using the key

            Args:
                ciphertext -- string -- the text to decipher
                key -- string

            return the plaintext
        """
        # make sure the key is at least as big as the text
        if len(key) < len(ciphertext):
            sys.exit("The key is smaller than the text")

        return ''.join([chr((ord(ciphertext[i]) - ord(key[i])) % 256) \
                        for i in range(len(ciphertext))])
