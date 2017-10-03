import unittest

from lib import chinese_remainder_theorem

class TestChineseRemainderTheorem(unittest.TestCase):

    def test_simple_case_one(self):
        values = [2, 5]
        modulos = [11, 7]
        self.assertEqual(chinese_remainder_theorem(values, modulos), 68)

    def test_simple_case_two(self):
        values = [2, 3, 2]
        modulos = [3, 5, 7]
        self.assertEqual(chinese_remainder_theorem(values, modulos), 23)

if __name__ == '__main__':
    unittest.main()
