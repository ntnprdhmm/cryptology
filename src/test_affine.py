import unittest

from lib import affine_encryption

class TestAffine(unittest.TestCase):

    def test_lowercase(self):
        M = "troyes"
        a = 7
        b = 3
        C = "GSXPFZ"
        self.assertEqual(affine_encryption(M, a, b), C)

if __name__ == '__main__':
    unittest.main()
