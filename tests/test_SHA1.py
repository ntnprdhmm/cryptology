import unittest

from src.SHA1 import SHA1

class TestGCD(unittest.TestCase):

    def test_simple_1(self):
        sha_1 = SHA1()
        text = "Hello world !"
        bytetext = bytearray(text, 'utf-8')
        self.assertEqual(len(sha_1.pad(bytetext)) % sha_1.block_size, 0)

    def test_simple_2(self):
        sha_1 = SHA1()
        text = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
        bytetext = bytearray(text, 'utf-8')
        self.assertEqual(len(sha_1.pad(bytetext)) % sha_1.block_size, 0)

if __name__ == '__main__':
    unittest.main()
