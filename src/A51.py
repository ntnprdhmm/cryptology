import LFSR

class A51:

    def __init__(self):
        self.key_length = 64
        self.fn_length = 22
        self.r1 = LFSR(name="R1", length=19, taps=[13, 16, 17, 18], clocking_bit_index=8)
        self.r2 = LFSR(name="R2", length=22, taps=[20, 21], clocking_bit_index=10)
        self.r3 = LFSR(name="R3", length=23, taps=[7, 20, 21, 22], clocking_bit_index=10)

    def init_lfsr(self, key, fn):
        """ Init the 3 LFSR with:
            key : 64-bit key
            fn  : 22-bit frame number
        """
        self.key = key
        self.fn = fn
        # TODO: init the 3 LFSR with key and fn

    def output_bit(self):
        """ XOR the ouput bits of the 3 registers
        """
        return r1.output_bit() ^ r2.output_bit() ^ r3.output_bit()
