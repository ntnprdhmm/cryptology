import unittest

from src.functions import miller_rabin_primality_test

class TestMillerRabinPrimalityTest(unittest.TestCase):

    def test_easy_case_prime(self):
        self.assertTrue(miller_rabin_primality_test(11))

    def test_normal_prime(self):
        self.assertTrue(miller_rabin_primality_test(19891))

    def test_big_prime(self):
        self.assertTrue(miller_rabin_primality_test(1203793))

    def test_easy_composite(self):
        self.assertFalse(miller_rabin_primality_test(25))

    def test_normal_composite(self):
        self.assertFalse(miller_rabin_primality_test(36936))

    def test_big_composite(self):
        self.assertFalse(miller_rabin_primality_test(3693652))

if __name__ == '__main__':
    unittest.main()
