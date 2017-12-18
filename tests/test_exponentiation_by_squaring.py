import unittest

from src._functions import exponentiation_by_squaring, exponentiation_by_squaring_recursive

class TestExponentiationBySquaring(unittest.TestCase):

    def test_iterative(self):
        n = 784
        exp = 121
        self.assertEqual(exponentiation_by_squaring(n, exp), n**exp)

    def test_recursive(self):
        n = 784
        exp = 121
        self.assertEqual(exponentiation_by_squaring_recursive(n, exp), n**exp)

if __name__ == '__main__':
    unittest.main()
