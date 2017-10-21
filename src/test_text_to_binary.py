import unittest

from utils import utf8_to_binary, binary_to_utf8

class TestTextToBinary(unittest.TestCase):

    def test_to_binary_simple_case(self):
        self.assertEqual(utf8_to_binary('hello world'), '0110100001100101011011000110110001101111001000000111011101101111011100100110110001100100')

    def test_to_binary_with_accents(self):
        self.assertEqual(utf8_to_binary("J'ai été à la pèche."), '0100101000100111011000010110100100100000111010010111010011101001001000001110000000100000011011000110000100100000011100001110100001100011011010000110010100101110')

    def test_utf8_binary_utf8(self):
        text = "J'ai été à la pèche."
        self.assertEqual(binary_to_utf8(utf8_to_binary(text)), text)

if __name__ == '__main__':
    unittest.main()
