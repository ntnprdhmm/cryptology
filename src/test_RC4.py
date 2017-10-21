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

if __name__ == '__main__':
    unittest.main()
