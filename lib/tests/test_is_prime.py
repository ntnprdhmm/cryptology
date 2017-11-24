import unittest

from src.functions import is_prime

class TestIsPrime(unittest.TestCase):

    def test_one(self):
        self.assertFalse(is_prime(1))

    def test_simple_prime(self):
        self.assertTrue(is_prime(13))

    def test_big_prime(self):
        self.assertTrue(is_prime(93179))

    def test_hard_prime(self):
        self.assertTrue(is_prime(1299709))

    def test_harder_prime(self):
        self.assertTrue(is_prime(999999000001))

    def test_not_prime_easy_1(self):
        self.assertFalse(is_prime(555))

    def test_not_prime_easy_2(self):
        self.assertFalse(is_prime(333))

    def test_not_prime_harder_1(self):
        self.assertFalse(is_prime(333668))

    def test_not_prime_harder_2(self):
        self.assertFalse(is_prime(999999000002))

if __name__ == '__main__':
    unittest.main()
