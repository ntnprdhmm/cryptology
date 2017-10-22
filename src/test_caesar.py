import unittest

from lib import simple_caesar_cipher

class TestCaesar(unittest.TestCase):

    def test_lowercase(self):
        M = "troyes"
        K = 22
        self.assertEqual(simple_caesar_cipher(M, K), "PNKUAO")

    def test_reserve(self):
        M = "CARTMAN"
        K = 16
        self.assertEqual(simple_caesar_cipher(simple_caesar_cipher(M, K), (26-K)), M)

if __name__ == '__main__':
    unittest.main()
