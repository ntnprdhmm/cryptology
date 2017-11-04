import unittest

from src.lib import exponentiation_by_squaring

class TestExponentiationBySquaring(unittest.TestCase):

    def test_normal_case(self):
        n = 784
        exp = 121
        self.assertEqual(exponentiation_by_squaring(n, exp), n**exp)

if __name__ == '__main__':
    unittest.main()
