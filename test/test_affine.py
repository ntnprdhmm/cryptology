import unittest

from src.Affine import Affine

class TestAffine(unittest.TestCase):

    def test_simple(self):
        M = "troyes"
        affine = Affine(a=7, b=3)
        self.assertEqual(affine.decipher(affine.cipher(M)), M)

    def test_harder(self):
        M = "a5665sd648s4dSDFSFSDé\"$*****'---(___&&&)'"
        affine = Affine(a=7, b=3)
        self.assertEqual(affine.decipher(affine.cipher(M)), M)

if __name__ == '__main__':
    unittest.main()
