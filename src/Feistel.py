#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This module contains the Feistel class
"""

from src import utils

class Feistel(object):
    """ Feistel block cipher implementation

        Attributes:
            plaintext -- string -- the original message to cipher
            key -- string -- the current key
            right -- string -- the right part of the current ciphertext
            left -- string -- the left part of the current ciphertext
            func_f -- function -- the F function of the Feistel network
            func_next_subkey -- function -- function to generate the next subkey
                used in in func_F
    """

    def __init__(self, plaintext, key, func_f, func_next_subkey):
        # original message
        self.plaintext = plaintext
        # split the message in 2 blocks
        self.left = plaintext[:(len(plaintext)//2)]
        self.right = plaintext[len(plaintext)//2:]
        # the original key
        self.key = key
        # Feistel F function
        self.func_f = func_f
        # function to generate the next key
        self.func_next_subkey = func_next_subkey

    def get_ciphertext(self):
        """ Combine the left and right part and return the ciphertext
        """
        return self.left + self.right

    def next_round(self):
        """ Run the next Feistel round
        """
        # generate the next subkey and the new k
        self.key, subkey = self.func_next_subkey(self.key)
        # calculate the result of func_f
        func_f_result = self.func_f(subkey, self.right)
        # calculate the new left and right
        next_left = self.right
        next_right = utils.binary_xor(self.left, func_f_result).zfill(len(self.plaintext) // 2)
        # set left and right attributes
        self.left, self.right = next_left, next_right

    def run(self, nb_rounds):
        """ Run the Feistel cipher algorithm

            Args:
                nb_rounds -- int -- the number of Feistel rounds

            return the ciphertext
        """
        for _ in range(nb_rounds):
            self.next_round()
        return self.get_ciphertext()
