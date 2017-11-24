from LFSR import LFSR
import os
import utils

input_path = os.path.abspath('assets') + '/'
output_path = os.path.abspath('outputs') + '/'

class A51:

    def __init__(self, key):
        self.key_length = 64
        self.key = [int(b) for b in key]

    def init_lfsr(self):
        """ Init the 3 LFSR with:
            key : 64-bit key
        """

        # create the 3 LFSR
        self.r1 = LFSR(name="R1", length=19, taps=[13, 16, 17, 18], clocking_bit_index=8)
        self.r2 = LFSR(name="R2", length=22, taps=[20, 21], clocking_bit_index=10)
        self.r3 = LFSR(name="R3", length=23, taps=[7, 20, 21, 22], clocking_bit_index=10)

        # introduce the key in the system
        for i in range(self.key_length):
            self.r1.shift(self.r1.feedback() ^ self.key[i])
            self.r2.shift(self.r2.feedback() ^ self.key[i])
            self.r3.shift(self.r3.feedback() ^ self.key[i])

    def output_bit(self):
        """ XOR the ouput bits of the 3 registers
        """
        return self.r1.output_bit() ^ self.r2.output_bit() ^ self.r3.output_bit()

    def gen_sequence(self, l = 114):
        """ Generate a sequence of 'l' bits
            By default, l is 114
        """
        sequence = []
        for i in range(l):
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

    def run(self, m):
        """ Encrypt/Decrypt an utf-8 encoded string
        """
        # init the 3 lfsr
        self.init_lfsr()
        # use them to encrypt generate a sequence
        # and XOR the generated sequence with the message
        binary_m = utils.utf8_to_binary(m)
        binary_c = utils.binary_xor(binary_m, self.gen_sequence(len(binary_m)))
        return utils.binary_to_utf8(binary_c)

    def run_pgm(self, input_file, output_file):
        # init the 3 lfsr
        self.init_lfsr()

        f_in = open(input_file, 'rb')
        lines = f_in.readlines()

        f_out = open(output_file, 'wb')
        for i in range(len(lines)):
            lines[i] = bytearray(lines[i])
            # cipher each byte
            for j in range(len(lines[i])):
                lines[i][j] ^= int(self.gen_sequence(8), 2)
            f_out.write(lines[i])


k = "1111000011110000111100001111000011110000111100001111000011110000"
a51 = A51(k)
a51.run_pgm(input_path + 'lena.pgm', output_path + 'enc_lena.pgm')
a51.run_pgm(output_path + 'enc_lena.pgm', output_path + 'lena.pgm')

"""
m = '104 103 105  99  92  92  94 100 100  94  85  84  89 103 103  95 100 100  92  90  91 100  90  90  89  84  89  89  93  93  88  92  92  83  82  81  80  80  73  73  76  77  77  77  82  83  97  97  92  83  83  86  97  97  95  83  81  81  79  81  85  84  86  90  95  89  85  83  82  82  87  91  93  88  83  83  86  90 101  93  91  91  92  96 106 106 102  96  95  92  83  83  83  86  85  87  88  87  89  90  86  86  89  89  92 100  95  92  92  92  99 101 102 103 103 103  86  84  87  90  90  89  83  83  88  92  92  92  93  90  90  84  85  94 100  94  91  85  84  83  83  87  83  83  83  92  92  87  85  89  89  87  84  84  87  87  81  80  80  81  81  78  78  79  80  81  87  88  88  86  86  90  86  86  89  89  79  73  73  89  89  79  72  72  74  76  77  74  73  73  74  77  77  77  77  79  80  80  81  80  77  76  76  77  80  80  80  81  78  78  74  74  74  74  76  82  82  80  80  82  88  88  87  86  79  79  79  76  73  72  73  71  71  70  71  72  73  73  71  72  76  81  81  75  75  72  70  71  71  72\n 109 103 105 100  96  92  93  94  88  86  88  84  85  96  99  95  96 102  97  92  96 100  90  88  86  83  87  90  94  91  85  83  85  85  88  85  83  86  80  79  79  85  85  82  85  83  85  90  87  83  84  89  93  89  85  82  81  80  79  84  84  86  91  93  97  91  88  88  85  88  88  88  93  90  86  88  87  89 101  93  92  93  94  99 102  98  96  96  95  88  86  94 104  97  86  84  87  88  93  97  86  89  94  95  98 106 101  95  95  95 102 103 101 101 102 103  85  85  86  90  88  88  87  90  90  90  85  85  90  89  88  87  86  97 100  95  86  85  87  87  87  86  85  88  87  87  87  84  83  83  88  83  79  81  85  85  81  80  81  81  81  79  79  80  82  83  84  88  88  87  93  94  91  86  88  83  78  74  73  76  81  81  77  74  77  79  79  75  74  75  75  77  77  77  77  79  77  84  86  82  77  76  77  78  81  84  81  81  79  76  76  77  75  74  78  84  81  82  83  85  87  84  82  80  75  74  73  72  71  71  72  70  71  71  69  70  70  71  71  72  74  76  75  72  71  69  68  69  70  71'
print(m)
c = a51.run(m)
print(c)
m2 = a51.run(c)
print(m2)
print(m1==m2)
"""
