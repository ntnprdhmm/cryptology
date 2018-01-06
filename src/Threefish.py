#!/usr/bin/python3

""" This module contains the Threefish class
"""

from _utils import (bytearray_to_int, add_padding)
from _functions import rotl, rotr

class Threefish(object):
    """ Threefish implementation

        Constants:
            C -- integer -- used in the rounds keys generation
            W_LEN -- integer -- the length of a word in a block
            MASK -- integer -- we work with 64 bits words. The mask is used to keep
                number on 64 bits (&)
            P -- tuple of int -- permutation table for the permutation function

        Attributes:
            block_size -- integer -- 32, 64 or 128 -- the size of a block, in bytes
            key -- bytes -- same length as block_size
            tweaks -- bytes -- used in the rounds's keys generation
    """

    C = bytearray.fromhex("1bd11bdaa9fc1a22")
    W_LEN = 8
    MASK = 0xffffffffffffffff
    P = (0, 3, 2, 1, 4, 7, 5, 6, 15, 9, 11, 13, 8, 14, 10, 12)

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
        new_rot = rotl(int.from_bytes(m2, byteorder='big'), rotations=42, w=Threefish.W_LEN*8)

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
        new_rot = rotr(temp_m2, rotations=42, w=Threefish.W_LEN*8)

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
                b -- list -- a block

            return the block permuted
        """
        return [block[Threefish.P[i]] for i in range(len(block))]

    @staticmethod
    def blockify(text, block_size):
        """ Cut the given text in a list of blocks,
            and each blocks in a list of words

            Args:
                text -- bytes -- the bytes string to cut in block
                block_size -- integer -- the size of a block, in bytes

            return a list: the text cutted in blocks
        """
        assert(len(text)%block_size == 0), "The text need some padding."

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

    def threefish_round(self, block):
        """ take a block and make 1 round (substitution + permutation) on it

            Args:
                block -- bytearray -- the block to round

            return a bytearray, the block after the round
        """
        # Substitution (8*2) because we are taking pairs of numbers
        for i in range(0, self.block_size // (8*2)):
            block[2*i], block[2*i + 1] = Threefish.mix(block[2*i], block[2*i+1])
        # Permutation
        block = Threefish.permute(block)
        return(block)

    def threefish_round_inv(self, block):
        """ take a block and make 1 inverted round (substitution + permutation) on it

            Args:
                block -- bytearray -- the block to invert 1 round

            return a bytearray, the block after the inveted round
        """
        # Permutation
        block = Threefish.permute(block)
        # Subsitution (8*2) because we are taking pairs of numbers
        for i in range(0, self.block_size // (8*2)):
            block[2*i], block[2*i + 1] = Threefish.mix_inv(block[2*i], block[2*i+1])
        return(block)

    def cipher(self, bytes_to_cipher, IV=None):
        """
            Cipher the text with ECB or CBC encryption methods

            Args:
                bytes_to_cipher -- bytes -- the text to cipher
                IV -- bytearray -- the initialization vector if we are in CBC encryption method

            return the ciphered text as bytes
        """
        # add padding to the text
        bytes_to_cipher = bytes(add_padding(bytes_to_cipher, block_size=self.block_size*8))

        # Put the text to cipher in blocks of words of W_LEN and of block_size in bytes (32 = 256 or 64 = 512 or 128 = 1024)
        to_cipher = self.blockify(bytes_to_cipher, self.block_size)
        ciphered_text = [None]*(len(to_cipher))
        # Go through blocks
        for i in range(len(to_cipher)):
            # Treating CBC encryption instead of ECB if an Initialization Vector has been passed as parameters
            if(IV):
                if(i==0):
                    for j in range(0, len(to_cipher[i])):
                        temp_to_cipher = (int.from_bytes(to_cipher[i][j], 'big')) ^ (int.from_bytes(IV[j], 'big'))
                        to_cipher[i][j] = temp_to_cipher.to_bytes((temp_to_cipher.bit_length() + 7) // 8, 'big')
                else:
                    for j in range(0, len(to_cipher[i])):
                        temp_to_cipher = (int.from_bytes(to_cipher[i-1][j], 'big')) ^ (int.from_bytes(to_cipher[i][j], 'big'))
                        to_cipher[i][j] = temp_to_cipher.to_bytes((temp_to_cipher.bit_length() + 7) // 8, 'big')
            # Which key should we use ?
            count = 0
            # Doing 1 round
            for j in range(0,76):
                # Apply one of the subkey every 4 rounds
                if (j % 4 == 0) or (j == 75):
                    key = self.rounds_keys[count]
                    # Go through words and xor keys
                    for k in range(0, len(to_cipher[i])):
                        temp_to_cipher = (int.from_bytes(to_cipher[i][k], 'big')) ^ (int.from_bytes(key[k], 'big'))
                        to_cipher[i][k] = temp_to_cipher.to_bytes((temp_to_cipher.bit_length() + 7) // 8, 'big')
                    # Increment key counter
                    count += 1
                to_cipher[i] = self.threefish_round(to_cipher[i])
            ciphered_text[i] = to_cipher[i]

        result = b''
        # Set result as a big bytes containing the entire ciphered text
        for i in range(len(ciphered_text)):
            for j in range(len(ciphered_text[i])):
                result += ciphered_text[i][j]

        return result

    def decipher(self, bytes_to_decipher, IV=None):
        """
            Decipher the text

            Args:
                bytes_to_decipher -- bytes -- the text to decipher

            return the deciphered text
        """
        # Put the text to decipher in blocks of words of W_LEN and of block_size in bytes (32 = 256 or 64 = 512 or 128 = 1024)
        to_decipher = self.blockify(bytes_to_decipher, self.block_size)
        deciphered_text = [None]*(len(to_decipher))
        # Go through blocks
        for i in range(len(to_decipher)-1, -1, -1):
            # Which key should we use ?
            count = 19
            # Doing 1 round
            for j in range(75, -1, -1):
                # Invert the round
                to_decipher[i] = self.threefish_round_inv(to_decipher[i])
                # Apply one of the subkey every 4 rounds
                if (j % 4 == 0) or (j == 75):
                    key = self.rounds_keys[count]
                    # Go through words and add keys
                    for k in range(0, len(to_decipher[i])):
                        temp_to_decipher = (int.from_bytes(to_decipher[i][k], 'big')) ^ (int.from_bytes(key[k], 'big'))
                        to_decipher[i][k] = temp_to_decipher.to_bytes((temp_to_decipher.bit_length() + 7) // 8, 'big')
                    # Increment key counter
                    count -= 1
            # Treating CBC encryption instead of ECB if an Initialization Vector has been passed as parameters
            if(IV):
                if(i==0):
                    for k in range(0, len(to_decipher[i])):
                        temp_to_decipher = (int.from_bytes(to_decipher[i][k], 'big')) ^ (int.from_bytes(IV[k], 'big'))
                        to_decipher[i][k] = temp_to_decipher.to_bytes((temp_to_decipher.bit_length() + 7) // 8, 'big')
                else:
                    for k in range(0, len(to_decipher[i])):
                        temp_to_decipher = (int.from_bytes(to_decipher[i-1][k], 'big')) ^ (int.from_bytes(to_decipher[i][k], 'big'))
                        to_decipher[i][k] = temp_to_decipher.to_bytes((temp_to_decipher.bit_length() + 7) // 8, 'big')
            deciphered_text[i] = to_decipher[i]

        result = b''
        # Set result as a big bytes containing the entire ciphered text
        for i in range(len(deciphered_text)):
            for j in range(len(deciphered_text[i])):
                result += deciphered_text[i][j]

        # remove padding
        padding_size = int.from_bytes(result[-2:], byteorder="big")
        result = result[:len(result) - padding_size]

        return result


from _functions import (generate_random_unicode_string)

#### TEST PART ####
# Key randomly generated
# Create a Threefish on 1024 bits block with the key
key = bytes(generate_random_unicode_string(32 + 16), 'utf-8')
fish = Threefish(32, key)
# Generate the keys
fish.key_schedule()

# Bytes size = 10240 -> 81920 bits
to_cipher = bytes("yolo swagg yolo swaggyolo swagg yolo swaggyolo swagg yolo swaggyolo swagg yolo swaggyolo swagg yolo swaggyolo swagg yolo swaggyolo swagg yolo swagg",'utf-8')

# IV to test CBC
#InitVect = [bytes("abcdefgh", 'utf-8'), bytes("abcdefgh", 'utf-8'), bytes("abcdefgh", 'utf-8'), bytes("abcdefgh", 'utf-8'), bytes("abcdefgh", 'utf-8'), bytes("abcdefgh", 'utf-8'), bytes("abcdefgh", 'utf-8'), bytes("abcdefgh", 'utf-8'), bytes("abcdefgh", 'utf-8'), bytes("abcdefgh", 'utf-8'), bytes("abcdefgh", 'utf-8'), bytes("abcdefgh", 'utf-8'), bytes("abcdefgh", 'utf-8'), bytes("abcdefgh", 'utf-8'), bytes("abcdefgh", 'utf-8'), bytes("abcdefgh", 'utf-8')]

# Print in string encoded in utf-8
print(to_cipher.decode('utf-8'))
print("ciphertext :")
things_ciphered = fish.cipher(to_cipher)
print(things_ciphered)
"""
things_ciphered = int.from_bytes(things_ciphered, byteorder='big')
things_ciphered = things_ciphered.to_bytes(32, byteorder='big')

things_ciphered = str(things_ciphered)

things_ciphered = bytes(things_ciphered[2:-1], 'utf-8')
print(things_ciphered)
"""

print("deciphered text :")
deciphered = fish.decipher(things_ciphered)
print(deciphered)
print(deciphered.decode('utf-8'))
