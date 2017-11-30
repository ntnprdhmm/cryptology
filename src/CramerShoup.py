#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This module contains the CramerShoup class
"""

from random import randint
import sys
from src.functions import (random_prime, find_group_generators)
from src.utils import (write_file, list_to_string, read_file)
from src.SHA1 import SHA1

MIN_PRIME = 100
MAX_PRIME = 500
FILE_NAME = 'cramer_shoup'

class CramerShoup(object):
    """ CramerShoup implementation
    """

    @staticmethod
    def key_generation():
        """ Generate the keys, and save it into files

            To calculate:
                p -- int -- a prime number
                g1, g2 -- int -- two distinct generators of p
                x1, x2, y1, y2, w -- int -- randomly picked numbers in range [0:p]
                X -- int -- result of g1**x1 + g2**x2
                Y -- int -- result of g1**y1 + g2**y2
                W -- int -- result of g1**w

            To save in files:
                public key: (p, g1, g2, X, Y, W)
                private key: (x1, x2, y1, y2, w)
        """
        # start by generate randomly a prime number p
        p = random_prime(MIN_PRIME, MAX_PRIME)
        # get the generators of p
        generators = find_group_generators(p)
        # pick 2 distinct generators randomly
        g1 = generators[randint(0, len(generators)-1)]
        g2 = g1
        while g2 == g1:
            g2 = generators[randint(0, len(generators)-1)]
        # pick randomly 5 integers in range [0:P]
        x1 = randint(0, p-1)
        x2 = randint(0, p-1)
        y1 = randint(0, p-1)
        y2 = randint(0, p-1)
        w = randint(0, p-1)
        # calculate X, Y and W
        X = ((g1**x1) * (g2**x2)) % p
        Y = ((g1**y1) * (g2**y2)) % p
        W = (g1**w) % p

        # save the public key
        write_file(FILE_NAME + '.pub', list_to_string([p, g1, g2, X, Y, W]))
        # save the private key
        write_file(FILE_NAME, list_to_string([x1, x2, y1, y2, w]))

    @staticmethod
    def _hash(b1, b2, c):
        """
            Caculate the hash for the verification, using SHA1

            Args:
                b1 -- int
                b2 -- int
                c -- int

            return string of 40 bytes (hexa number)
        """
        return SHA1().hash(str(b1) + str(b2) + str(c))

    @staticmethod
    def cipher():
        """
            Cipher the message with the public key

            write the cipher message in a file
        """
        # read the public key
        p, g1, g2, X, Y, W = [int(v) for v in read_file(FILE_NAME + '.pub', 'outputs').split(',')]
        # read the message
        m = int(read_file(FILE_NAME + '.txt'))
        # Pick a random int, b, of Zp
        b = randint(0, p-1)
        # calculate b1 and b2
        b1 = (g1**b) % p
        b2 = (g2**b) % p
        # cipher the message
        c = ((W**b) * m) % p
        # calculate the verification
        beta = int(CramerShoup._hash(b1, b2, c), 16) % p
        v = ((X**b) * (Y**(b*beta))) % p

        # write the ciphertext in a file
        write_file(FILE_NAME + '.cipher', ','.join([str(v) for v in [b1, b2, c, v]]))

    @staticmethod
    def decipher():
        """
            Decipher the message with the private key

            return the decipher message
        """
        # read the private and public keys
        p, _, _, _, _, _ = [int(v) for v in read_file(FILE_NAME + '.pub', 'outputs').split(',')]
        x1, x2, y1, y2, w = [int(v) for v in read_file(FILE_NAME, 'outputs').split(',')]
        # read the cipher text
        b1, b2, c, v = [int(v) for v in read_file(FILE_NAME + '.cipher', 'outputs').split(',')]
        # verification step
        beta = int(CramerShoup._hash(b1, b2, c), 16) % p
        v2 = ((b1**x1) * (b2**x2) * ((b1**y1 * b2**y2)**beta)) % p
        if v != v2:
            # if the verification is false, throw error
            sys.exit("err: verification failed")

        # write the decipher text in a file
        write_file(FILE_NAME + '.decipher',  str(((b1**(p - 1 - w)) * c) % p))
