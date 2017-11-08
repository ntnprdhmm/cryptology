from LFSR import LFSR

class A51:

    def __init__(self):
        self.key_length = 64
        self.r1 = LFSR(name="R1", length=19, taps=[13, 16, 17, 18], clocking_bit_index=8)
        self.r2 = LFSR(name="R2", length=22, taps=[20, 21], clocking_bit_index=10)
        self.r3 = LFSR(name="R3", length=23, taps=[7, 20, 21, 22], clocking_bit_index=10)

    def init_lfsr(self, key):
        """ Init the 3 LFSR with:
            key : 64-bit key
        """
        self.key = [int(b) for b in key]

        # introduce the key in the system
        for i in range(self.key_length):
            self.r1.shift(self.r1.feedback() ^ self.key[i])
            self.r2.shift(self.r2.feedback() ^ self.key[i])
            self.r3.shift(self.r3.feedback() ^ self.key[i])

    def output_bit(self):
        """ XOR the ouput bits of the 3 registers
        """
        return self.r1.output_bit() ^ self.r2.output_bit() ^ self.r3.output_bit()

    def gen_sequence(self):
        """ Generate a sequence of 114 bits
        """
        sequence = []
        for i in range(114):
            # check the clocking bit of each register
            # to determine the majority bit
            c = {0:0, 1:0}
            c[self.r1.clocking_bit()] += 1
            c[self.r2.clocking_bit()] += 1
            c[self.r3.clocking_bit()] += 1

            majority_bit = 0 if c[0] > c[1] else 1

            # update LFSR where clocking_bit = majority_bit
            if self.r1.clocking_bit() == majority_bit:
                self.r1.shift()
            if self.r2.clocking_bit() == majority_bit:
                self.r2.shift()
            if self.r3.clocking_bit() == majority_bit:
                self.r3.shift()

            sequence.append(self.output_bit())

        return ''.join([str(b) for b in sequence])

alg = A51()
alg.init_lfsr("1111000011110000111100001111000011110000111100001111000011110000")
print(alg.gen_sequence())
