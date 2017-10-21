import unittest

from lib import rc4

class TestGCD(unittest.TestCase):

    def test_rc4_1(self):
        text = "wiki"
        key = "pedia"
        self.assertEqual(rc4(text, key), "ÙÌîÃ")

    def test_rc4_2(self):
        text = "Plaintext"
        key = "Key"
        self.assertEqual(rc4(text, key), "»ó\x16èÙ@¯\nÓ")

    def test_rc4_decrypt(self):
        text = "Hello world 45 ! azeaze è&"
        key = "ALittleKey:3"
        self.assertEqual(rc4(rc4(text, key), key), text)

if __name__ == '__main__':
    unittest.main()
