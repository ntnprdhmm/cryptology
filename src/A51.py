#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" This module contains the A5/1 class
"""

import src.utils as utils
from src.LFSR import LFSR

class A51(object):
    """ A5/1 stream cipher implementation

        Attributes:
            key_length -- int -- the length of the key
            key -- list of int -- the key's bits
            rg1 -- None or LFSR -- the LFSR 1
            rg2 -- None or LFSR -- the LFSR 2
            rg3 -- None or LFSR -- the LFSR 3
    """

    def __init__(self, key):
        """
            Args:
                key -- string -- string containing 64 bits
        """
        self.key_length = 64
        self.key = [int(b) for b in key]
        self.rg1 = None
        self.rg2 = None
        self.rg3 = None

    def init_lfsr(self):
        """ Init the 3 LFSR rg1, rg2, rg3:
            - instanciate 3 LFSR
            - introduce the key
        """

        # create the 3 LFSR
        self.rg1 = LFSR(name="R1", length=19, taps=[13, 16, 17, 18],
                        clocking_bit_index=8)
        self.rg2 = LFSR(name="R2", length=22, taps=[20, 21],
                        clocking_bit_index=10)
        self.rg3 = LFSR(name="R3", length=23, taps=[7, 20, 21, 22],
                        clocking_bit_index=10)

        # introduce the key in the system
        for i in range(self.key_length):
            self.rg1.shift(self.rg1.feedback() ^ self.key[i])
            self.rg2.shift(self.rg2.feedback() ^ self.key[i])
            self.rg3.shift(self.rg3.feedback() ^ self.key[i])

    def output_bit(self):
        """ XOR the ouput bits of the 3 registers
            return the result
        """
        return self.rg1.output_bit() \
                ^ self.rg2.output_bit() \
                ^ self.rg3.output_bit()

    def gen_sequence(self, length=114):
        """ Generate a sequence of bits

            Args:
                length -- int -- the length of the sequence to generate

            return a string that represente the binary sequence generated
        """
        sequence = []
        for _ in range(length):
            # check the clocking bit of each register
            # to determine the majority bit
            counter = {0:0, 1:0}
            counter[self.rg1.clocking_bit()] += 1
            counter[self.rg2.clocking_bit()] += 1
            counter[self.rg3.clocking_bit()] += 1

            majority_bit = 0 if counter[0] > counter[1] else 1

            # update LFSR where clocking_bit = majority_bit
            if self.rg1.clocking_bit() == majority_bit:
                self.rg1.shift()
            if self.rg2.clocking_bit() == majority_bit:
                self.rg2.shift()
            if self.rg3.clocking_bit() == majority_bit:
                self.rg3.shift()

            sequence.append(self.output_bit())

        return ''.join([str(b) for b in sequence])

    def run(self, text):
        """ Encrypt/Decrypt an utf-8 encoded text

            Args:
                text -- string -- the text to encode / decode

            return the encoded / decoded text
        """
        # init the 3 lfsr
        self.init_lfsr()
        # use them to encrypt generate a sequence
        # and XOR the generated sequence with the message
        binary_text = utils.utf8_to_binary(text)
        binary_result = utils.binary_xor(binary_text,
                                         self.gen_sequence(len(binary_text)))
        return utils.binary_to_utf8(binary_result)

    def run_pgm(self, input_file, output_file):
        """ Encrypt/Decrypt a .pgm image

            Args:
                input_file -- string -- the input file path
                output_file -- string -- the output file path

            Exemple:
                k = "1111000011110000111100001111000011110000111100001111000011110000"
                A51 = A51(k)
                A51.run_pgm(INPUT_PATH + 'lena.pgm', OUTPUT_PATH + 'enc_lena.pgm')
                A51.run_pgm(OUTPUT_PATH + 'enc_lena.pgm', OUTPUT_PATH + 'lena.pgm')
        """
        # init the 3 lfsr
        self.init_lfsr()

        f_in = open(input_file, 'rb')
        lines = f_in.readlines()

        f_out = open(output_file, 'wb')
        for i, line in enumerate(lines):
            lines[i] = bytearray(line)
            # cipher each byte
            for j in range(len(lines[i])):
                lines[i][j] ^= int(self.gen_sequence(8), 2)
            f_out.write(lines[i])
