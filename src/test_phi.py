import unittest

from lib import phi

class TestPhi(unittest.TestCase):

    def test_simple_case(self):
        self.assertEqual(phi(12), 4)

    def test_simple_case_prime(self):
        self.assertEqual(phi(7), 6)

    def test_simple_case_four(self):
        self.assertEqual(phi(36), 12)

    def test_simple_case_two(self):
        self.assertEqual(phi(90), 24)

    def test_simple_case_three(self):
        self.assertEqual(phi(81), 54)

    """
    def test_hard_case(self):
        self.assertEqual(phi(9007199254740881), 9007199254740880)
    """

if __name__ == '__main__':
    unittest.main()
