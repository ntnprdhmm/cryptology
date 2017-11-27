#!/usr/bin/env python3
# -*-coding: utf-8 -*-

""" This module contains the SHA1 class
"""

import struct

class SHA1(object):
    """ SHA 1 hash algorithm implementation
    """

    def __init__(self):
        # block size, in bytes
        self.block_size = 64
        # init the hash variables
        self.h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]

    def final_hash(self):
        """ Combine the 5 hash variables to produce the final hash
            return the 160 bits length hash
        """
        return ''.join([str(h) for h in self.h])

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
        arr.append((56 - len(arr)) % 64)

        # add the length of the original text
        arr += struct.pack(b'>Q', original_length)

        return arr


    def hash(self, text):
        # transform the string to an array of bytes
        bytes_text = bytearray(text, 'utf-8')
        # SHA-1 works with 512 bits blocks.
        # add some padding if needed
        bytes_text = self.pad(bytes_text)

text = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod \
tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, \
quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. \
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu \
fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa \
qui officia deserunt mollit anim id est laborum."

SHA1 = SHA1()
print(SHA1.hash(text))
print(SHA1.final_hash())
