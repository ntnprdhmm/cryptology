#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This module contains the RC4 class
"""

class RC4(object):
    """ RC4 stream cipher implementation

        Attributes:
            S -- list -- permutations
            key -- string
    """

    def __init__(self, key):
        self.S = []
        self.key = key

    def key_scheduling(self):
        """ Initialise the permutation array S avec la clé
        """
        self.S = list(range(256))
        j = 0
        for i in range(256):
            j = (j + self.S[i] + ord(self.key[i % len(self.key)])) & 0xFF
            self.S[i], self.S[j] = self.S[j], self.S[i]

    def cipher(self, plaintext):
        """ cipher the plaintext

            Args:
                plaintext -- string -- the message to cipher

            return the ciphertext
        """
        self.key_scheduling()

        ciphertext = [None] * len(plaintext)
        i = 0
        j = 0
        for index, char in enumerate(plaintext):
            i = (i + 1) & 0xFF
            j = (j + self.S[i]) & 0xFF
            self.S[i], self.S[j] = self.S[j], self.S[i]
            ciphertext[index] = chr((ord(char) ^ self.S[(self.S[i] + self.S[j]) & 0xFF]))

        return ''.join(ciphertext)
