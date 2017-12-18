#!/usr/bin/env python3

""" This module contains the Caesar class
"""

class Caesar(object):
    """ Caesar cipher implementation

        Attributes:
            shift -- int -- left shift value
    """

    def __init__(self, shift):
        self.shift = shift

    def cipher(self, plaintext):
        """ Cipher the plaintext

            Args:
                plaintext -- string -- the text to cipher

            return the ciphertext
        """
        return ''.join([chr((ord(c) + self.shift) & 0xFF) for c in plaintext])

    def decipher(self, ciphertext):
        """ Decipher the ciphertext

            Args:
                ciphertext -- string -- the text to decipher

            return the plaintext
        """
        return ''.join([chr((ord(c) + (256 - self.shift)) & 0xFF) for c in ciphertext])
