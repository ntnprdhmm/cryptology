import unittest

from src.lib import sieve_of_eratosthenes, phi

class TestSieveOfEratosthenes(unittest.TestCase):

    def test_with_one(self):
        self.assertEqual(sieve_of_eratosthenes(1), [])

    def test_with_two(self):
        self.assertEqual(sieve_of_eratosthenes(2), [2])

    def test_easy_case(self):
        self.assertEqual(sieve_of_eratosthenes(4), [2, 3])

    def test_simple_case(self):
        self.assertEqual(sieve_of_eratosthenes(120), [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113])

    def test_simple_case_two(self):
        self.assertEqual(sieve_of_eratosthenes(125), [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113])

if __name__ == '__main__':
    unittest.main()
