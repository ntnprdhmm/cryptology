import unittest

from RC4 import RC4

class TestGCD(unittest.TestCase):

    def test_rc4_1(self):
        text = "wiki"
        key = "pedia"
        rc4 = RC4(key)
        self.assertEqual(rc4.cipher(text), "ÙÌîÃ")

    def test_rc4_2(self):
        text = "Plaintext"
        key = "Key"
        rc4 = RC4(key)
        self.assertEqual(rc4.cipher(text), "»ó\x16èÙ@¯\nÓ")

    def test_rc4_decrypt(self):
        text = "Hello world 45 ! azeaze è&"
        key = "ALittleKey:3"
        rc4 = RC4(key)
        self.assertEqual(rc4.cipher(rc4.cipher(text)), text)

if __name__ == '__main__':
    unittest.main()
