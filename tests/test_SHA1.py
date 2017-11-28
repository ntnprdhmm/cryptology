import unittest

from src.SHA1 import SHA1

class TestSHA1(unittest.TestCase):

    def test_padding_simple_1(self):
        sha_1 = SHA1()
        text = "Hello world !"
        bytetext = bytearray(text, 'utf-8')
        self.assertEqual(len(SHA1._padding(bytetext)) % sha_1.block_size, 0)

    def test_padding_simple_2(self):
        sha_1 = SHA1()
        text = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
        bytetext = bytearray(text, 'utf-8')
        self.assertEqual(len(SHA1._padding(bytetext)) % sha_1.block_size, 0)

    def test_prepare_simple(self):
        sha_1 = SHA1()
        text = "Hello world !"
        bytetext = bytearray(text, 'utf-8')

        # value of b'Hell'
        result = 1214606444

        # test 'Hell', the first word of the first block
        self.assertEqual(SHA1._prepare(SHA1._padding(bytetext))[0][0], result)

if __name__ == '__main__':
    unittest.main()
