from src.lib import inverse

class Affine:

    def __init__(self, a, b):
        self.a = a
        self.b = b
        # mod 256 => utf-8
        self.ia = inverse(a, 256)

    def cipher(self, M):
        C = []
        for c in M:
            # convert c from char to unicode
            # apply affine function (a*c + b) % 256
            # convert the new value of c from unicode to char
            C.append(chr((self.a * ord(c) + self.b) & 0xFF))
        return ''.join(C)

    def decipher(self, C):
        M = []
        for c in C:
            # convert c from char to unicode
            # apply affine function ((c-b) * a^-1) % 256
            # convert the new value of c from unicode to char
            M.append(chr(((ord(c) - self.b) * self.ia) & 0xFF))
        return ''.join(M)
