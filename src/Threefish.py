#!/usr/bin/python3

""" This module contains the Threefish class
"""

from _utils import bytearray_to_int
from _functions import rotl

class Threefish(object):
    """ Threefish implementation

        Constants:
            C -- integer -- used in the rounds keys generation
            W_LEN -- integer -- the length of a word in a block
            LEFT_ROTATION -- integer -- number of bits to rotate to the left.
                used in the mix function
            MASK -- integer -- we work with 64 bits words. The mask is used to keep
                number on 64 bits (&)

        Attributes:
            block_size -- integer -- 32, 64 or 128 -- the size of a block, in bytes
            key -- bytes -- same length as block_size
            tweaks -- bytes -- used in the rounds's keys generation
    """

    C = bytearray.fromhex("1bd11bdaa9fc1a22")
    W_LEN = 8
    LEFT_ROTATION = 49
    MASK = 0xffffffffffffffff

    def __init__(self, block_size, u_key):
        """
            Args:
                u_key -- bytes -- user's key -- contains the key and the tweaks
                    the first part of the user's key is the key (same size as a block)
                    the lasts 2 words are the tweaks
        """
        self.block_size = block_size
        self.key = u_key[:self.block_size]
        self.tweaks = [
            bytearray_to_int(u_key[self.block_size:(self.block_size + self.W_LEN)]),
            bytearray_to_int(u_key[(self.block_size + self.W_LEN):]),
            0
        ]
        # generate the third tweak
        self.tweaks[2] = self.tweaks[0] + self.tweaks[1]
        self.rounds_keys = None

    def key_schedule(self):
        """ Generate the 20 keys used in the rounds
        """
        # cut the key in words and generate the last word of the key
        key_words = []
        next_word = self.C
        for i in range(0, self.block_size // self.W_LEN):
            key_words.append(self.key[i*self.W_LEN:(i+1)*self.W_LEN])
            for j in range(self.W_LEN):
                next_word[j] ^= key_words[i][j]
        key_words.append(next_word)
        # generate the rounds's keys
        words_per_block = self.block_size // self.W_LEN
        self.rounds_keys = []
        for i in range(20):
            round_keys = []
            for n in range(0, words_per_block-3):
                next_round_key = key_words[(i+n) % (words_per_block+1)]
                round_keys.append(next_round_key)

            next_round_key = key_words[(i+words_per_block-3) % (words_per_block+1)]
            next_round_key = bytearray_to_int(next_round_key)
            next_round_key = (next_round_key + self.tweaks[i % 3]) & Threefish.MASK
            round_keys.append(next_round_key)

            next_round_key = key_words[(i+words_per_block-2) % (words_per_block+1)]
            next_round_key = bytearray_to_int(next_round_key)
            next_round_key = (next_round_key + self.tweaks[(i+1) % 3]) & Threefish.MASK
            round_keys.append(next_round_key)

            next_round_key = key_words[(i+words_per_block-1) % (words_per_block+1)]
            next_round_key = bytearray_to_int(next_round_key)
            next_round_key = (next_round_key + i) & Threefish.MASK
            round_keys.append(next_round_key)

            self.rounds_keys.append(round_keys)

    @staticmethod
    def mix(m1, m2):
        """ mix 2 words

            Args:
                m1 -- integer -- a word
                m2 -- integer -- another word

            return a tuple, with the 2 mixed words
        """
        new_m1 = (m1 + m2) & Threefish.MASK
        new_m2 = new_m1 ^ (rotl(m2, rotations=Threefish.LEFT_ROTATION, w=Threefish.W_LEN*8))
        return (new_m1, new_m2)


from random import getrandbits
key = bytearray(getrandbits(8) for _ in range(64))
fish = Threefish(64, key)
fish.key_schedule()
x1 = getrandbits(Threefish.W_LEN*8)
x2 = getrandbits(Threefish.W_LEN*8)
print(x1)
print(x2)
print(len(bin(x1)))
print(Threefish.mix(x1, x2))
