import unittest

from src.lib import vernam

class TestGCD(unittest.TestCase):

    def test_vernam_simple(self):
        message = "moon11"
        key = "apollo"
        self.assertEqual(vernam(vernam(message, key), key), message)

    def test_vernam_simple(self):
        message = "J'ai mangé des pâtes."
        key = "miam!miam!miam!miam!miam!"
        self.assertEqual(vernam(vernam(message, key), key), message)

if __name__ == '__main__':
    unittest.main()
