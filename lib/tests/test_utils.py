import unittest

from src.utils import binary_sum, binary_xor

class TestUtils(unittest.TestCase):

    def test_binary_sum_normal_case(self):
        self.assertEqual(binary_sum('10101010', '01001001'), '11110011')

    def test_binary_xor_normal_case(self):
        self.assertEqual(binary_xor('10101010', '01001001'), '11100011')

if __name__ == '__main__':
    unittest.main()
