# initial permutation table
IP = (57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7, 56, 48, 40, 32, 24, 16, 8, 0, 58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6)
# expension
E = (31, 0, 1, 2, 3, 4, 3, 4, 5, 6, 7, 8, 7, 8, 9, 10, 11, 12, 11, 12, 13, 14, 15, 16, 15, 16, 17, 18, 19, 20, 19, 20, 21, 22, 23, 24, 23, 24, 25, 26, 27, 28, 27, 28, 29, 30, 31, 0)
# permutation
P = (15, 6, 19, 20, 28, 11, 27, 16, 0, 14, 22, 25, 4, 17, 30, 9, 1, 7, 23, 13, 31, 26, 2, 8, 18, 12, 29, 5, 21, 10, 3, 24)
# final permutation
IPinv = (39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25, 32, 0, 40, 8, 48, 16, 56, 24)
# permuted choice 1
PC1 = (57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36, 63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4)
# Permuted choice 2
PC2 = (13, 16, 10, 23, 0, 4, 2, 27, 14, 5, 20, 9, 22, 18, 11, 3, 25, 7, 15, 6, 26, 19, 12, 1, 40, 51, 30, 36, 46, 54, 29, 39, 50, 44, 32, 47, 43, 48, 38, 55, 33, 52, 45, 41, 49, 35, 28, 31)

sBox = 8*[64*[0]]

sBox[0] = (14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7,
            0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8,
            4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0,
           15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13)

sBox[1] = (15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10,
            3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5,
            0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15,
           13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9)
sBox[2] = (10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8,
           13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1,
           13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7,
            1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12)

sBox[3] = ( 7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15,
           13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9,
           10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4,
            3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14)

sBox[4] = ( 2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9,
           14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6,
            4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14,
           11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3)

sBox[5] = (12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11,
           10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8,
            9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6,
            4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13)

sBox[6] = ( 4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1,
           13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6,
            1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2,
            6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12)

sBox[7] = (13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7,
            1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2,
            7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8,
            2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11)

from src import utils
from Feistel import Feistel

class DES:

    def __init__(self, key):
        self.rounds = 16
        # original key
        self.key = key
        # 64-bits key to 56-bits permuted key
        self.permuted_key = ''.join([self.key[i] for i in PC1])

    def generate_next_subkey(self, k):
        """ From the current key
            generate the new key (left rotation)
            and the next subkey using the new key
            return the new key and next subkey
        """
        # split the 56-bits key in 2 blocks
        k_left = k[:26]
        k_right = k[26:]
        # rotate by one to the left each block
        k_left = k_left[1:] + k_left[0]
        k_right = k_right[1:] + k_right[0]
        # generate the next subkey
        new_k = k_left + k_right
        # return new key and the subkey generated
        return new_k, ''.join([new_k[i] for i in PC2])

    def expansion(self, m):
        """ Step 1:
            the 32-bit half-block is expanded to 48 bits
            using the expansion permutation
        """
        return ''.join([m[i] for i in E])

    def key_mixing(self, k, m):
        """ Step 2:
            combine the key with expended message
            using xor operator
        """
        return utils.binary_xor(k, m)

    def substitution(self, c):
        """ Step 3:
            the block is divided into eight 6-bit pieces
            Blocks are processing by substitution boxes
            [8 blocks of 6 bits --> 8 blocks of 4 bits]
        """
        ouputs = []
        for i in range(8):
            block = c[i*6:(i+1)*6]
            row = int(c[0]+c[5], 2)
            column = int(c[1]+c[2]+c[3]+c[4], 2)
            ouputs.append(sBox[i][row*16 + column])
        return ''.join([utils.decimal_to_binary(ouput, 4) for ouput in ouputs])

    def permutation(self, c):
        """ Step 4:
            the 32 output bits from the S-boxes are rearranged
            according to a fixed permutation,
        """
        return ''.join([c[i] for i in P])

    def F(self, k, m):
        """ Feistel function for DES
        """
        expended_m = self.expansion(m)
        c = self.key_mixing(k, expended_m)
        substituted = self.substitution(c)
        permuted = self.permutation(substituted)

        return ''.join([str(b) for b in permuted])

    def cipher(self, m):
        # initial permutation
        m = [m[i] for i in IP]
        m = ''.join([str(b) for b in m])

        # run the 16 feistel rounds
        feistel = Feistel(m, self.permuted_key, self.F, self.generate_next_subkey)
        c = feistel.run(self.rounds)

        # final permutation
        c = [c[i] for i in IPinv]

        return ''.join(c)


des = DES("1100110011001100110011001100110011001100110011001100110011001100")
#des.F("11111111000000001111111100000000")
print(des.cipher("1111111100000000111111110000000011111111000000001111111100000000"))
