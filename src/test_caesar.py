import unittest

from Caesar import Caesar

class TestCaesar(unittest.TestCase):

    def test_cipher(self):
        M = "hello world !!!"
        K = 125
        caesar = Caesar(K)
        self.assertNotEqual(caesar.cipher(M), M)

    def test_decipher(self):
        M = "hello world 33 45 #ÉÉ~~^$!!!"
        K = 213
        caesar = Caesar(K)
        self.assertEqual(caesar.decipher(caesar.cipher(M)), M)

if __name__ == '__main__':
    unittest.main()
