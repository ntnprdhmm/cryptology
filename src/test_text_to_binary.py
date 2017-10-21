import unittest

from utils import utf8_to_binary

class TestTextToBinary(unittest.TestCase):

    def test_simple_case(self):
        self.assertEqual(utf8_to_binary('hello world'), '0110100001100101011011000110110001101111001000000111011101101111011100100110110001100100')

    def test_with_accents(self):
        self.assertEqual(utf8_to_binary("J'ai été à la pèche."), '0100101000100111011000010110100100100000111010010111010011101001001000001110000000100000011011000110000100100000011100001110100001100011011010000110010100101110')

if __name__ == '__main__':
    unittest.main()
