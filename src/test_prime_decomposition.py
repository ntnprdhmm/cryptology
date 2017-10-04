import unittest

from lib import prime_decomposition, is_prime

class TestPrimeDecomposition(unittest.TestCase):

    def test_simple_case(self):
        n = 9438
        factors = prime_decomposition(n, [])
        self.assertEqual(factors, [2, 3, 11, 11, 13])

    def test_simple_case_two(self):
        n = 81
        factors = prime_decomposition(n, [])
        self.assertEqual(factors, [3, 3, 3, 3])

if __name__ == '__main__':
    unittest.main()
