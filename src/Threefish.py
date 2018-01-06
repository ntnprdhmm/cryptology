#!/usr/bin/python3

""" This module contains the Threefish class
"""

from _utils import bytearray_to_int
from _functions import rotl, rotr

class Threefish(object):
    """ Threefish implementation

        Constants:
            C -- integer -- used in the rounds keys generation
            W_LEN -- integer -- the length of a word in a block
            MASK -- integer -- we work with 64 bits words. The mask is used to keep
                number on 64 bits (&)

        Attributes:
            block_size -- integer -- 32, 64 or 128 -- the size of a block, in bytes
            key -- bytes -- same length as block_size
            tweaks -- bytes -- used in the rounds's keys generation
    """

    C = bytearray.fromhex("1bd11bdaa9fc1a22")
    W_LEN = 8
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
        # Addition in int
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
        # Cast in integers and xor back to get m2 after rotl
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
        """ permute 1 block

            Args:
                b -- bytearray -- a block

            return a permuted block
        """
        length = len(block)
        if length == 4: block[0], block[1], block[2], block[3] = block[0], block[3], block[2], block[1]
        elif length == 8: block[0], block[1], block[2], block[3], block[4], block[5], block[6], block[7] = block[2], block[1], block[4], block[7], block[6], block[5], block[0], block[3]
        elif length == 16: block[0], block[1], block[2], block[3], block[4], block[5], block[6], block[7], block[8], block[9], block[10], block[11], block[12], block[13], block[14], block[15] = block[0], block[9], block[2], block[13], block[6], block[11], block[4], block[15], block[10], block[7], block[12], block[3], block[14], block[5], block[8], block[1]
        else: print ("Error in permutation, block length = {}".format(length))
        return block

    @staticmethod
    def permute_inv(block):
        """ invert the permute on a block

            Args:
                b -- bytearray -- a block

            return a unpermuted block
        """
        length = len(block)
        if length == 4: block[0], block[3], block[2], block[1] = block[0], block[1], block[2], block[3]
        elif length == 8: block[2], block[1], block[4], block[7], block[6], block[5], block[0], block[3] = block[0], block[1], block[2], block[3], block[4], block[5], block[6], block[7]
        elif length == 16: block[0], block[9], block[2], block[13], block[6], block[11], block[4], block[15], block[10], block[7], block[12], block[3], block[14], block[5], block[8], block[1] = block[0], block[1], block[2], block[3], block[4], block[5], block[6], block[7], block[8], block[9], block[10], block[11], block[12], block[13], block[14], block[15]
        else: print ("Error in permutation, block length = {}".format(length))
        return(block)

    @staticmethod
    def put_in_blocks(text, block_size):
        """ put a bytes into a bytearray of "block" with block_size as each block size and each block is a bytearray of words of W_LEN size in bytes

            Args:
                text -- bytes -- a bytes string containing the string to splice in blocks
                block_size -- integer -- the size of a returned block

            return a bytearray
        """

        res = []
        i = 0

        #run through the text
        while i < len(text):
            block = []
            if (i + block_size) < len(text):
                temp_block = text[i:i+block_size]

                # if not enough bits, add padding
                while len(temp_block) < block_size:
                    temp_block += bytes("\x00", 'utf-8')

                # Slice in words
                j = 0
                while j in range(len(temp_block)):
                    block.append(temp_block[j:j+Threefish.W_LEN])
                    j += Threefish.W_LEN

                res.append(block)
                i += block_size
            else:
                temp_block = text[i:len(text)]

                # if not enough bits, add padding
                while len(temp_block) < block_size:
                    temp_block += bytes("\x00", 'utf-8')

                # Slice in words
                j = 0
                while j in range(len(temp_block)):
                    block.append(temp_block[j:j+Threefish.W_LEN])
                    j += Threefish.W_LEN

                res.append(block)
                i = len(text)

        return res

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
        block = Threefish.permute_inv(block)
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
        # Put the text to cipher in blocks of words of W_LEN and of block_size in bytes (32 = 256 or 64 = 512 or 128 = 1024) and add a padding if necessary
        to_cipher = self.put_in_blocks(bytes_to_cipher, self.block_size)
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
                while (len(ciphered_text[i][j]) != 8): ciphered_text[i][j] = bytes("\x00", 'utf-8') + ciphered_text[i][j]
                result += ciphered_text[i][j]

        return result

    def decipher(self, bytes_to_decipher, IV=None):
        """
            Decipher the text

            Args:
                bytes_to_decipher -- bytes -- the text to decipher

            return the deciphered text
        """
        # Put the text to decipher in blocks of words of W_LEN and of block_size in bytes (32 = 256 or 64 = 512 or 128 = 1024) and add a padding if necessary
        to_decipher = self.put_in_blocks(bytes_to_decipher, self.block_size)
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
                while (len(deciphered_text[i][j]) != 8): deciphered_text[i][j] = bytes("\x00", 'utf-8') + deciphered_text[i][j]
                result += deciphered_text[i][j]

        return result



#### TEST PART ####
# Key randomly generated
key = bytearray('\xcdH=\x9f\x86\xf9.\xad\xf0<s\\\x9a\xc4@\xaa\xea\x9f\'!N\xcd\xfe<?\x8a\xab\xbc_O\xb1\'kK\x97$\xac\xbe\x81b\x9228L\xf3]\x1b 0\x93\xfda\xbb"|\xa1~\x81\xe4s\'p\x1d)\xa3\xcc\\\xd8\x1b\xe7\xb4M\xf4C\xff\xde,\xb8\xb9K\x96]!h}K\x13\x8e\xfd\xe5\xd5\xc8\xd9\'XV1\x15R\xf3|\x85\xc8.\x07U\xba\xaf\xe1E\x1e\xb3D1\xf6\xa3\xd5=#N\x07\xee\tO~\x19:\xca\x95\xfe&\xb2\x8bK\xb0\xf9\xab\xba\x05\xdc\xb5\xfb\x87\xe5@.\xb9\xc8\xeeqX\x93\n\xf9\x86\x95N\x04\x0f\x03\xc3_\xf5;\xe3G\xc0\xa6\xde\x142\xb8\xb3\x01\xe6\xd7\x18\xf6B\xe2\xc3l\x83\x97\xe00\xdb\x85\xefLv#\x92 \x837\xdc\x8d\x10\x9f\x8e\xe4\x06\xb1\x02y8\xdcc\x93\xf2\x908\xb3\xdf6W\xbc\xe2\x8a\x1bm\xfa\xca\xb1\x1c\x07\xde+u\xd0A\xf0\n\x8eL\r\x8f\xf4a\xaf\xc7T\x1d\x84ea\xfeO\xfb\xcag|\xb3Y', 'utf-8')
# Create a Threefish on 1024 bits block with the key
fish = Threefish(128, key)
# Generate the keys
fish.key_schedule()

# Bytes size = 10240 -> 81920 bits
things_to_cipher = bytes("abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghij",'utf-8')

# IV to test CBC
InitVect = [bytes("abcdefgh", 'utf-8'), bytes("abcdefgh", 'utf-8'), bytes("abcdefgh", 'utf-8'), bytes("abcdefgh", 'utf-8'), bytes("abcdefgh", 'utf-8'), bytes("abcdefgh", 'utf-8'), bytes("abcdefgh", 'utf-8'), bytes("abcdefgh", 'utf-8'), bytes("abcdefgh", 'utf-8'), bytes("abcdefgh", 'utf-8'), bytes("abcdefgh", 'utf-8'), bytes("abcdefgh", 'utf-8'), bytes("abcdefgh", 'utf-8'), bytes("abcdefgh", 'utf-8'), bytes("abcdefgh", 'utf-8'), bytes("abcdefgh", 'utf-8')]

# Print in string encoded in utf-8
print(things_to_cipher.decode('utf-8'))
print(len(things_to_cipher))
print("Things ciphered :")
# Print the ciphered one with padding (if padding was needed)
things_ciphered = fish.cipher(things_to_cipher, InitVect)
print(things_ciphered)
print(len(things_ciphered))
print("Things deciphered :")
things_deciphered = fish.decipher(things_ciphered, InitVect)
# Print the deciphered one with padding (if padding was needed)
print(things_deciphered)
print(len(things_deciphered))
# Print in string encoded in utf-8 (padding is now absent)
print(things_deciphered.decode('utf-8'))
