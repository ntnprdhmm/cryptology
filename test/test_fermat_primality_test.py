import unittest

from src.lib import fermat_primality_test

class TestFermatPrimalityTest(unittest.TestCase):

    def test_really_simple_prime(self):
        self.assertTrue(fermat_primality_test(3))

    def test_really_simple_composite(self):
        self.assertFalse(fermat_primality_test(4, 2))

    def test_simple_prime(self):
        self.assertTrue(fermat_primality_test(23, 3))

    def test_simple_composite(self):
        self.assertFalse(fermat_primality_test(35, 6))

    def test_normal_prime(self):
        self.assertTrue(fermat_primality_test(99929))

    """
    def test_big_prime(self):
        self.assertTrue(fermat_primality_test(1203793))
    """

    def test_normal_composite(self):
        self.assertFalse(fermat_primality_test(398745, 2))

if __name__ == '__main__':
    unittest.main()
