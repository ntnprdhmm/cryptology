#!/usr/bin/env python3

""" This module contains the LFSR class
"""

class LFSR(object):
    """ Linear-feedback shift register implementation

        Attributes:
            name -- string -- LFSR's name
            taps -- list -- bits used to generate the next bit
            clocking_bit_index -- int -- clocking bit's index
            length -- int -- LFSR's length
            register -- list -- current bits of the LFSR
    """

    def __init__(self, name, taps, clocking_bit_index=None, length=None, seed=None):
        """
            Args:
                seed -- string -- seed to init the LFSR's register

            Exemples:
                r1 = LFSR(name="R1", length=19, taps=[13, 16, 17, 18], clocking_bit_index=8)
                r2 = LFSR(name="R2", seed="1110101011011111011", taps=[13, 16, 17, 18],
                          clocking_bit_index=8)
        """
        self.name = name
        self.taps = taps
        self.clocking_bit_index = clocking_bit_index
        self.length = len(seed) if seed else length
        self.register = [int(b) for b in seed] if seed else [0] * length

    def feedback(self):
        """ Calculate and return the next bit of the register
        """
        xor = 0
        for tap in self.taps:
            xor ^= self.register[tap]
        return xor

    def shift(self, next_bit=None):
        """ shift the register
            generate the next value and remove the oldest

            next_bit -- char -- shift with this bit instead of generating the next
                bit if next_bit is set

            return the new register
        """
        self.register.insert(0, next_bit if next_bit else self.feedback())
        self.register.pop()
        return ''.join([str(b) for b in self.register])

    def clocking_bit(self):
        """ return the clocking bit
        """
        return self.register[self.clocking_bit_index]

    def output_bit(self):
        """ return the output bit
        """
        return self.register[0]

    def __str__(self):
        """ Return a string that describe the LFSR
        """
        string = ("LFSR %s\n" % self.name)
        string += ("- length         : %d\n" % self.length)
        string += ("- taps           : %s\n" % ' '.join([str(tap) for tap in self.taps]))
        string += ("- clocking bit   : %d\n" % self.clocking_bit_index)
        string += ("- register       : %s" % ' '.join([str(bit) for bit in self.register]))
        return string
