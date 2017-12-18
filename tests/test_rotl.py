import unittest

from src._functions import rotl

class TestROTL(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(rotl(4), 8)

    def test_normal(self):
        self.assertEqual(rotl(3, 2), 12)

if __name__ == '__main__':
    unittest.main()
