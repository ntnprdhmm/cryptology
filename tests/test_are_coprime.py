import unittest

from src._functions import are_coprime

class TestBezout(unittest.TestCase):

    def test_with_prime(self):
        a = 13
        b = 5
        self.assertTrue(are_coprime(a, b))

    def test_with_prime_harder(self):
        a = 1299709
        b = 129608
        self.assertTrue(are_coprime(a, b))

    def test_factors(self):
        a = 25
        b = 50
        self.assertFalse(are_coprime(a, b))

if __name__ == '__main__':
    unittest.main()
