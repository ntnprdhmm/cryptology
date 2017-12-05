#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This module contains the CramerShoup class
"""

from random import randint
import sys
from src.functions import (generate_safe_prime_number, find_safe_prime_generator)
from src.utils import (write_file, list_to_string, read_file, read_file_bytes_block)
from src.SHA1 import SHA1

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
        p = generate_safe_prime_number()
        # pick 2 distinct generators randomly
        g1 = find_safe_prime_generator(p, (p-1)//2)
        g2 = g1
        while g2 == g1:
            g2 = find_safe_prime_generator(p, (p-1)//2)
        # pick randomly 5 integers in range [0:P]
        x1 = randint(0, p-1)
        x2 = randint(0, p-1)
        y1 = randint(0, p-1)
        y2 = randint(0, p-1)
        w = randint(0, p-1)
        # calculate X, Y and
        X = (pow(g1, x1, p) * pow(g2, x2, p))
        Y = (pow(g1, y1, p) * pow(g2, y2, p))
        W = pow(g1, w, p)

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
            Cipher the text with the public key

            write the cipher text in a file
        """
        # read the public key
        p, g1, g2, X, Y, W = [int(v) for v in read_file(FILE_NAME + '.pub', 'outputs').split(',')]
        # read the text
        m = read_file_bytes_block(FILE_NAME + '.txt')
        # Pick a random int, b, of Zp
        b = randint(0, p-1)
        # calculate b1 and b2
        b1 = pow(g1, b, p)
        b2 = pow(g2, b, p)
        # cipher the text, block per block
        block_value = int.from_bytes(m[:128], byteorder="big")
        c = (pow(W, b, p) * block_value) % p
        # calculate the verification
        beta = int(CramerShoup._hash(b1, b2, c), 16) % p
        v = (pow(X, b, p) * pow(Y, b*beta, p)) % p

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
        v2 = (pow(b1, x1, p) * pow(b2, x2, p) * (pow(pow(b1, y1, p) * pow(b2, y2, p), beta, p))) % p
        if v != v2:
            # if the verification is false, throw error
            sys.exit("err: verification failed")

        # decipher c
        m = (pow(b1, (p-1-w), p) * c) % p
        # calculate the bytes of the original text
        b = bytearray()
        while m:
            b.append(m & 0xff)
            m >>= 8
        b = b[::-1]
        # remove padding
        padding_size = int.from_bytes(b[-2:], byteorder="big")
        b = b[:len(b) - padding_size]
        # write the decipher text in a file
        write_file(FILE_NAME + '.decipher', b.decode('utf-8'))
