import unittest

from lib import prime_decomposition, is_prime

def check_factors(facs):
    p = 1
    for f in facs:
        #self.assertTrue(is_prime(f))
        p *= f
    return p

class TestPrimeDecomposition(unittest.TestCase):

    def test_simple_case(self):
        n = 9438
        factors = prime_decomposition(n)
        p = 1
        for f in factors:
            self.assertTrue(is_prime(f))
            p *= f
        self.assertEqual(p, n)
        self.assertEqual(factors, [2, 3, 11, 11, 13])

if __name__ == '__main__':
    unittest.main()
