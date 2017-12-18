import unittest

from src._functions import prime_decomposition, is_prime

class TestPrimeDecomposition(unittest.TestCase):

    def test_simple_case(self):
        n = 9438
        factors = prime_decomposition(n)
        primes = [2, 3, 11, 11, 13]
        i = 0
        for factor in factors:
            self.assertEqual(primes[i], factor)
            i += 1

    def test_simple_case_two(self):
        n = 81
        factors = prime_decomposition(n)
        primes = [3, 3, 3, 3]
        i = 0
        for factor in factors:
            self.assertEqual(primes[i], factor)
            i += 1

if __name__ == '__main__':
    unittest.main()
