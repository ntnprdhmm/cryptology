import unittest

from src.functions import gcd

class TestGCD(unittest.TestCase):

    def test_same_prime_number(self):
        self.assertEqual(gcd(13, 13), 13)

    def test_two_prime_number(self):
        self.assertEqual(gcd(23, 7), 1)

    def test_two_prime_number_reverse_order(self):
        self.assertEqual(gcd(5, 23), 1)

    def test_a_prime_number(self):
        self.assertEqual(gcd(37, 500), 1)

    def test_one_is_multiple_of_other(self):
        self.assertEqual(gcd(50, 100), 50)

    def test_normal_simple_case(self):
        self.assertEqual(gcd(15, 33), 3)

    def test_normal_hard_case(self):
        self.assertEqual(gcd(624129, 2061517), 18913)

if __name__ == '__main__':
    unittest.main()
