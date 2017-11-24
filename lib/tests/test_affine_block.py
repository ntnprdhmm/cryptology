import unittest

from src.functions import affine_block_encryption, affine_block_decryption

class TestAffine(unittest.TestCase):

    def test_simple_encryption(self):
        M = "CETTEUVESTGENIALEE"
        a = 7
        b = 100
        C = "SYLZLGVYEZUYTAGVGY"
        self.assertEqual(affine_block_encryption(M, a, b), C)

    def test_simple_decryption(self):
        M = "CETTEUVESTGENIALEE"
        a = 7
        b = 100
        C = "SYLZLGVYEZUYTAGVGY"
        self.assertEqual(affine_block_decryption(C, a, b), M)

if __name__ == '__main__':
    unittest.main()
