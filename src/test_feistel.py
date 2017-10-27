import unittest

from lib import feistel

class TestFeistel(unittest.TestCase):

    def test_feistel(self):
        M = "01000111010100110011000100110101"
        K = "0000000011111111"
        output = "01001000010101100010110100100001"
        self.assertEqual(feistel(M, K), output)

if __name__ == '__main__':
    unittest.main()
