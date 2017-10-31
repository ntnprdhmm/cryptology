class LFSR:

    def __init__(self, name, taps, clocking_bit_index = None, length = None, seed = None):
        """
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

            - next_bit: to use as next bit instead. If now, the next bit
            will be the feedback of the LFSR
        """
        self.register.insert(0, next_bit if next_bit else self.feedback())
        self.register.pop()

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
        s = ("LFSR %s\n" % self.name)
        s += ("- length         : %d\n" % self.length)
        s += ("- taps           : %s\n" % ' '.join([str(tap) for tap in self.taps]))
        s += ("- clocking bit   : %d\n" % self.clocking_bit_index)
        s += ("- register       : %s" % ' '.join([str(bit) for bit in self.register]))
        return s

"""
r1 = LFSR(name="R1", length=19, taps=[13, 16, 17, 18], clocking_bit_index=8)
r2 = LFSR(name="R2", seed="1110101011011111011", taps=[13, 16, 17, 18], clocking_bit_index=8)
print(r2)
r2.shift()
print(r2)
"""
