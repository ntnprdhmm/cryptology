import unittest

from src.lib import lcm

class TestLCM(unittest.TestCase):

    def test_normal_case(self):
        self.assertEqual(lcm(4, 6), 12)

    def test_with_prime_number(self):
        self.assertEqual(lcm(4, 7), 28)

    def test_with_one(self):
        self.assertEqual(lcm(1, 7), 7)

if __name__ == '__main__':
    unittest.main()
