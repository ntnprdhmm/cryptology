#!/usr/bin/python3

""" This module contains the Threefish class
"""

from src._utils import (bytearray_to_int, add_padding)
from src._functions import rotl, rotr

class Threefish(object):
    """ Threefish implementation

        Constants:
            C -- integer -- used in the rounds keys generation
            W_LEN -- integer -- the length of a word in a block
            MASK -- integer -- we work with 64 bits words. The mask is used to keep
                number on 64 bits (&)
            P -- tuple of int -- permutation table for the permutation function
            NB_ROUNDS -- integer -- the number of rounds
            NB_ROTATIONS -- integer -- the number of rotations to do in the mix function

        Attributes:
            block_size -- integer -- 32, 64 or 128 -- the size of a block, in bytes
            key -- bytes -- same length as block_size
            tweaks -- bytes -- used in the rounds's keys generation
    """

    C = bytearray.fromhex("1bd11bdaa9fc1a22")
    W_LEN = 8
    MASK = 0xffffffffffffffff
    P = (1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12, 15, 14)
    NB_ROUNDS = 76
    NB_ROTATIONS = 49

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
                round_keys.append(bytearray_to_int(next_round_key))

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

        # cast every keys in bytes
        for j in range(len(self.rounds_keys)):
            for k in range(len(self.rounds_keys[j])):
                self.rounds_keys[j][k] = self.rounds_keys[j][k].to_bytes((self.rounds_keys[j][k].bit_length() + 7) // 8, 'big')

    @staticmethod
    def mix(m1, m2):
        """ mix 2 words

            Args:
                m1 -- bytes -- a word
                m2 -- bytes -- another word

            return a tuple, with the 2 mixed words
        """
        # sum in int
        new_m1 = (int.from_bytes(m1, 'big') + int.from_bytes(m2, 'big')) & Threefish.MASK

        # Make the rotation in int
        new_rot = rotl(int.from_bytes(m2, byteorder='big'), rotations=Threefish.NB_ROTATIONS, w=Threefish.W_LEN*8)

        # Xor new_m1 with new_rot
        new_m2 = new_m1 ^ new_rot

        # Cast back in bytes
        new_m1 = new_m1.to_bytes((new_m1.bit_length() + 7) // 8, 'big')
        new_m2 = new_m2.to_bytes((new_m2.bit_length() + 7) // 8, 'big')
        return(new_m1, new_m2)

    @staticmethod
    def mix_inv(m1, m2):
        """ invert the mix on 2 words

            Args:
                m1 -- bytes -- a word
                m2 -- bytes -- another word

            return a tuple, with the 2 unmixed words
        """
        # Cast to int and xor back to get m2 after rotl
        temp_m2 = int.from_bytes(m1, 'big') ^ int.from_bytes(m2, 'big')

        # Make the rotr to cancel rotl
        new_rot = rotr(temp_m2, rotations=Threefish.NB_ROTATIONS, w=Threefish.W_LEN*8)

        # Retrieve m1 by substracting m2
        new_m1 = ((int.from_bytes(m1, 'big')) - new_rot) & Threefish.MASK

        # Cast back to bytes
        new_m1 = new_m1.to_bytes((new_m1.bit_length() + 7) // 8, 'big')
        new_m2 = new_rot.to_bytes((new_rot.bit_length() + 7) // 8, 'big')
        return(new_m1, new_m2)

    @staticmethod
    def permute(block):
        """ permute the given block using the permutation table

            Args:
                block -- list of bytes -- a block

            return the block permuted
        """
        return [block[Threefish.P[i]] for i in range(len(block))]

    @staticmethod
    def substitute(block, mix_function):
        """ permute the given block using the permutation table

            Args:
                block -- list of bytes -- a block
                mix_function -- function -- the mix function to call

            return the block substitute
        """
        # Subsitution: mix each pair of words in the given block
        for i in range(0, len(block), 2):
            block[i], block[i+1] = mix_function(block[i], block[i+1])

        return block

    @staticmethod
    def blockify(text, block_size):
        """ Cut the given text in a list of blocks,
            and each blocks in a list of words

            Args:
                text -- bytes -- the bytes string to cut in block
                block_size -- integer -- the size of a block, in bytes

            return a list: the text cutted in blocks
        """
        blocks = []
        # for each block we can make from the text
        for i in range(0, len(text)//block_size):
            # get the block
            block = text[(i*block_size):((i+1)*block_size)]
            # cut the block in words
            words = [block[(j*Threefish.W_LEN):((j+1)*Threefish.W_LEN)]
                     for j in range(0, block_size // Threefish.W_LEN)]
            # append the words to the list of blocks
            blocks.append(words)

        return blocks

    @staticmethod
    def threefish_round(block):
        """ take a block and make 1 round (substitution + permutation) on it

            Args:
                block -- list of bytes -- the block to round

            return a list of bytes: the block after the round
        """
        # Subsitution: mix each pair of words in the given block
        block = Threefish.substitute(block, Threefish.mix)
        # Permutation: apply permutation function on the block
        block = Threefish.permute(block)

        return(block)

    @staticmethod
    def threefish_round_inv(block):
        """ take a block and make 1 inverted round (permutation + substitution) on it

            Args:
                block -- list of bytes -- the block to invert 1 round

            return a list of bytes: the block after the inverted round
        """
        # Permutation
        block = Threefish.permute(block)
        # Subsitution: mix each pair of words in the given block
        block = Threefish.substitute(block, Threefish.mix_inv)

        return(block)

    @staticmethod
    def xor_with_block(block, key):
        """ xor a block with a key

            Args:
                block -- list of bytes
                key -- list of bytes

            return the block after xor on each words
        """
        # Go through words and xor key
        for j, word in enumerate(block):
            temp_to_cipher = (int.from_bytes(word, 'big')) ^ (int.from_bytes(key[j], 'big'))
            block[j] = temp_to_cipher.to_bytes((temp_to_cipher.bit_length() + 7) // 8, 'big')
        return block

    def cipher(self, plaintext, IV=None):
        """
            Cipher the given.

            Args:
                plaintext -- bytes -- the text to cipher in bytes
                IV -- bytes -- the initialization vector if case of CBC cipher mode

            By default, the cipher mode is ECB. If there is an IV (initialization vector)
            passed as parameter, the encryption mode will be CBC

            return the ciphered text as bytes
        """
        # add padding to the plaintext
        plaintext = bytes(add_padding(plaintext, block_size=self.block_size*8))
        # cut the plaintext in blocks
        blocks = self.blockify(plaintext, self.block_size)
        # cut the IV in blocks
        if IV:
            IV = self.blockify(IV, self.block_size)[0]

        ciphered_blocks = []
        # Go through blocks
        for i, block in enumerate(blocks):
            # handle CBC mode
            if IV:
                # if it's the first block, xor with the IV
                blocks[i] = Threefish.xor_with_block(block, IV if i == 0 else blocks[i-1])
            # rounds
            for j in range(Threefish.NB_ROUNDS-1):
                # Apply one of the subkey every 4 rounds
                if j % 4 == 0:
                    key = self.rounds_keys[j//4]
                    block = Threefish.xor_with_block(block, key)
                block = Threefish.threefish_round(block)

            key = self.rounds_keys[-1]
            block = Threefish.xor_with_block(block, key)
            block = Threefish.threefish_round(block)

            ciphered_blocks.append(block)
            blocks[i] = block

        # join all the words
        ciphertext = b''
        for i in range(len(ciphered_blocks)):
            for j in range(len(ciphered_blocks[i])):
                ciphertext += ciphered_blocks[i][j]
        return ciphertext

    def decipher(self, ciphertext, IV=None):
        """
            Decipher the text

            Args:
                ciphertext -- bytes -- the text to decipher

            return the deciphered text
        """
        # cut the ciphertext in blocks
        ciphered_blocks = self.blockify(ciphertext, self.block_size)
        # cut the IV in blocks
        if IV:
            IV = self.blockify(IV, self.block_size)[0]

        blocks = [None]*(len(ciphered_blocks))
        # loop through ciphered blocks
        for i, ciphered_block in reversed(list(enumerate(ciphered_blocks))):

            ciphered_block = self.threefish_round_inv(ciphered_block)
            key = self.rounds_keys[-1]
            ciphered_block = Threefish.xor_with_block(ciphered_block, key)

            # rounds
            for j in range(self.NB_ROUNDS-2, -1, -1):
                # Invert the round
                ciphered_block = self.threefish_round_inv(ciphered_block)
                # Apply one of the subkey every 4 rounds
                if j % 4 == 0:
                    key = self.rounds_keys[j//4]
                    ciphered_block = Threefish.xor_with_block(ciphered_block, key)
            # handle CBC mode
            if IV:
                # if it's the first block, xor with the IV
                ciphered_block = Threefish.xor_with_block(ciphered_block,
                                                          IV if i == 0 else ciphered_blocks[i-1])

            ciphered_blocks[i] = ciphered_block
            blocks[i] = ciphered_blocks[i]

        # join all words
        plaintext = b''
        for i in range(len(blocks)):
            for j in range(len(blocks[i])):
                plaintext += blocks[i][j]

        # remove padding
        padding_size = int.from_bytes(plaintext[-2:], byteorder="big")
        plaintext = plaintext[:len(plaintext) - padding_size]

        return plaintext
