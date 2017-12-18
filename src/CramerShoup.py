#!/usr/bin/env python3

""" This module contains the CramerShoup class
"""

from random import randint
import sys
from src._functions import (generate_safe_prime_number, find_safe_prime_generator)
from src._utils import (write_file, list_to_string, read_file, add_padding)
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
    def cipher(steam):
        """
            Cipher the text with the public key

            Args:
                steam -- bytes -- the text to cipher

            write the cipher text in a file
        """
        # read the public key
        p, g1, g2, X, Y, W = [int(v) for v in read_file(FILE_NAME + '.pub', 'outputs').split(',')]
        # pad the input stream
        m = add_padding(steam)
        # Pick a random int, b, of Zp
        b = randint(0, p-1)
        # calculate b1 and b2
        b1 = pow(g1, b, p)
        b2 = pow(g2, b, p)
        # cipher the text, block per block
        c = []
        for i in range(0, len(m), 128):
            block_value = int.from_bytes(m[i:i+128], byteorder="big")
            c.append((pow(W, b, p) * block_value) % p)
        # calculate the verification
        x = c[0]
        for i in range(1, len(c)):
            x ^= c[i]
        beta = int(CramerShoup._hash(b1, b2, x), 16) % p
        v = (pow(X, b, p) * pow(Y, b*beta, p)) % p

        # from 128 to 129 bytes
        for i, block in enumerate(c):
            c[i] = hex(block)[2:]
            # add leading 0 if needed, to create a block of 129 bytes (258 hex digits)
            c[i] = '0'*(258 - len(c[i])) + c[i]

        hex_c = ''.join(c)

        # write the ciphertext
        return hex(b1), hex(b2), hex_c, hex(v)

    @staticmethod
    def decipher(stream):
        """
            Decipher the message with the private key

            Args:
                stream -- bytes -- the text to decipher

            return the decipher message
        """
        # read the private and public keys
        p, _, _, _, _, _ = [int(v) for v in read_file(FILE_NAME + '.pub', 'outputs').split(',')]
        x1, x2, y1, y2, w = [int(v) for v in read_file(FILE_NAME, 'outputs').split(',')]
        # read the cipher stream
        b1, b2, c, v = stream.split(',')
        b1, b2, v = int(b1, 16), int(b2, 16), int(v, 16)
        m = [int(c[i:i+258], 16) for i in range(0, len(c), 258)]
        # verification step
        x = m[0]
        for i in range(1, len(m)):
            x ^= m[i]
        beta = int(CramerShoup._hash(b1, b2, x), 16) % p
        v2 = (pow(b1, x1, p) * pow(b2, x2, p) * (pow(pow(b1, y1, p) * pow(b2, y2, p), beta, p))) % p
        if v != v2:
            # if the verification is false, throw error
            sys.exit("err: verification failed")

        text = bytearray()
        # decipher block per block
        for block in m:
            block = (pow(b1, (p-1-w), p) * int(block)) % p
            # calculate the bytes of the original block
            b = bytearray()
            while block:
                b.append(block & 0xff)
                block >>= 8
            text += b[::-1]

        # remove padding
        padding_size = int.from_bytes(text[-2:], byteorder="big")
        text = text[:len(text) - padding_size]

        # return the decipher text
        return text.decode('utf-8')
