#!/usr/bin/env python3
# -*-coding: utf-8 -*-

""" This module contains the SHA1 class
"""

import struct
from src.functions import bytearray_xor, rotl

class SHA1(object):
    """ SHA 1 hash algorithm implementation

        Attributes:
            block_size -- int -- block size, in bytes
            h -- list -- hash variables
    """

    def __init__(self):
        self.block_size = 64
        self.h = [0x67452301,
                  0xEFCDAB89,
                  0x98BADCFE,
                  0x10325476,
                  0xC3D2E1F0]

    def produce_digest(self):
        """ Combine the 5 hash variables to produce the final hash
            return the 160 bits length hash
        """
        # we return 5 blocks of 8 hexadecimal digits
        return '%08x%08x%08x%08x%08x' % (self.h[0] & 0xffffffff,
                                         self.h[1] & 0xffffffff,
                                         self.h[2] & 0xffffffff,
                                         self.h[3] & 0xffffffff,
                                         self.h[4] & 0xffffffff)

    def pad(self, arr):
        """
            SHA-1 works with blocks of 64 bytes (512 bits). If the number of bits
            in the text is not a multiple of 512, add some padding:
                - add '1' at the end of the text
                - fill with '0' (but let 64 bits available at the end)
                - the 64 last bits are the length of the original text

            Args:
                arr -- bytearray -- the text to hash in bytes

            return arr, padded if needed
        """
        original_length = len(arr)

        if len(arr) % self.block_size == 0:
            return arr

        # append the bit 1
        arr.append(0x80)

        # add k*'0', with len(arr) + k = 56 (mod 64)
        # => to let 8 bytes (64 bits) for original text length
        nb_zero_to_add = ((7*self.block_size)//8 - len(arr)) % self.block_size
        for _ in range(nb_zero_to_add):
            arr.append(0)

        # add the length of the original text
        arr += struct.pack(b'>Q', original_length)

        return arr

    def hash(self, text):
        """
            Hash the given text

            Args:
                text -- string -- the text to hash

            return the 40 bytes digest
        """
        # transform the string to an array of bytes
        bytes_text = bytearray(text, 'utf-8')
        # SHA-1 works with 512 bits blocks.
        # add some padding if needed
        bytes_text = self.pad(bytes_text)

        # process the text in blocks of 64 bits
        for i in range(0, len(bytes_text), self.block_size):
            self.process_block(bytes_text[i:i+self.block_size])

        # return the digest
        return self.produce_digest()

    def process_block(self, block):
        """
            Hash the current block and update the hash variable

            Args:
                block -- bytearray -- the block to hash
        """
        w = [0]*80
        # cut the block in 16 words of 4 bytes
        for t in range(16):
            w[t] = struct.unpack(b'>I', block[t*4:(t+1)*4])[0]
        # => extend it to 80 words
        for t in range(16, 80):
            w[t] = rotl((w[t-3] ^ w[t-8] ^ w[t-14] ^ w[t-16]))

        # initialize hash value for this block
        a = self.h[0]
        b = self.h[1]
        c = self.h[2]
        d = self.h[3]
        e = self.h[4]

        # main loop
        for i in range(80):
            if i <= 19:
                f = (b and c) or ((not b) and d)
                k = 0x5A827999
            elif i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif i <= 59:
                f = (b and c) or (b and d) or (c and d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            T = (rotl(a, 5) + f + e + k + w[i]) & 0xffffffff
            e = d
            d = c
            c = rotl(b, 30)
            b = a
            a = T

        # add the block hash to the result
        self.h[0] += (self.h[0] + a) & 0xffffffff
        self.h[1] += (self.h[1] + b) & 0xffffffff
        self.h[2] += (self.h[2] + c) & 0xffffffff
        self.h[3] += (self.h[3] + d) & 0xffffffff
        self.h[4] += (self.h[4] + e) & 0xffffffff
