import unittest

from lib import affine_encryption, affine_decryption

class TestAffine(unittest.TestCase):

    def test_simple_encryption(self):
        M = "troyes"
        a = 7
        b = 3
        C = "GSXPFZ"
        self.assertEqual(affine_encryption(M, a, b), C)

    def test_simple_decryption(self):
        M = "TROYES"
        a = 7
        b = 3
        C = "GSXPFZ"
        self.assertEqual(affine_decryption(C, a, b), M)

if __name__ == '__main__':
    unittest.main()
