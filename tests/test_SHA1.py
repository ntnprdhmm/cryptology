import unittest

from src.SHA1 import SHA1

class TestGCD(unittest.TestCase):

    def test_simple_2(self):
        sha_1 = SHA1()
        text = "Hello world !"
        bytetext = bytearray(text, 'utf-8')
        print(sha_1.pad(bytetext))
        not_block = len(sha_1.pad(bytetext)) % sha_1.block_size
        self.assertEqual(not_block, 0)

if __name__ == '__main__':
    unittest.main()
