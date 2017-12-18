#!/usr/bin/env python3

""" This module contains the Affine class
"""

from src._functions import inverse

class Affine(object):
    """ Affine cipher implementation (monoalphabetic substitution)

        Attributes:
            a -- int -- 'a' in 'ax+b'
            b -- int -- 'b' in 'ax+b'
    """

    def __init__(self, a, b):
        self.a = a
        self.b = b
        # mod 256 => utf-8
        self.inverse_a = inverse(a, 256)

    def cipher(self, plaintext):
        """ Cipher a plaintext using Affine cipher

            Args:
                plaintext -- string -- the text to cipher

            return the ciphertext
        """
        ciphertext = []
        for char in plaintext:
            # convert c from char to unicode
            # apply affine function (a*c + b) % 256
            # convert the new value of c from unicode to char
            ciphertext.append(chr((self.a * ord(char) + self.b) & 0xFF))
        return ''.join(ciphertext)

    def decipher(self, ciphertext):
        """ Decipher a ciphertext using Affine decipher

            Args:
                ciphertext -- string -- the text to decipher

            return the plaintext
        """
        plaintext = []
        for char in ciphertext:
            # convert c from char to unicode
            # apply affine function ((c-b) * a^-1) % 256
            # convert the new value of c from unicode to char
            plaintext.append(chr(((ord(char) - self.b) * self.inverse_a) & 0xFF))
        return ''.join(plaintext)
