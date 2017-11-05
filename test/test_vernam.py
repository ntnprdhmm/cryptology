import unittest

from src.Vernam import Vernam

class TestGCD(unittest.TestCase):

    def test_binary_xor_cipher(self):
        message = "moon11"
        key = "apollo"
        vernam = Vernam()
        self.assertNotEqual(vernam.xor(message, key), message)

    def test_binary_xor_cipher_decipher(self):
        message = "J'ai mangé des pâtes."
        key = "miam!miam!miam!miam!miam!"
        vernam = Vernam()
        self.assertEqual(vernam.xor(vernam.xor(message, key), key), message)

if __name__ == '__main__':
    unittest.main()
