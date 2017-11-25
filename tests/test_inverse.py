import unittest

from src.functions import inverse

class TestInverse(unittest.TestCase):

    def test_simple_case(self):
        self.assertEqual(inverse(13, 7), -1)

    def test_normal_case(self):
        self.assertEqual(inverse(23, 120), 47)

if __name__ == '__main__':
    unittest.main()
