import unittest
from src import utils
from src.Feistel import Feistel

class TestFeistel(unittest.TestCase):

    def test_course_case(self):
        def F(K, D):
            f = utils.binary_sum(K, D).zfill(len(K))
            f = f[len(f) - len(K):]
            return f
        def next_key(K):
            new_K = K[2:] + K[:2]
            return new_K, new_K
            # because the subkey == the key
            # but for DES, subkey != key

        M = "01000111010100110011000100110101"
        K = "1100000000111111"
        output = "01001000010101100010110100100001"
        feist = Feistel(M, K, F, next_key)

        self.assertEqual(feist.run(3), output)

if __name__ == '__main__':
    unittest.main()
