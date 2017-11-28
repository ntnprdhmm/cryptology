import unittest

from src.SHA1 import SHA1

class TestSHA1(unittest.TestCase):

    def test_padding_simple_1(self):
        sha_1 = SHA1()
        text = "Hello world !"
        bytetext = bytearray(text, 'utf-8')
        self.assertEqual(len(SHA1._padding(bytetext)) % 64, 0)

    def test_padding_simple_2(self):
        sha_1 = SHA1()
        text = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
        bytetext = bytearray(text, 'utf-8')
        self.assertEqual(len(SHA1._padding(bytetext)) % 64, 0)

    def test_hello_world(self):
        sha_1 = SHA1()
        text = text = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        h = "a3da7877f94ad4cf58636a395fff77537cb8b919"
        self.assertEqual(sha_1.hash(text), h)

    def test_lorem(self):
        sha_1 = SHA1()
        text = "Hello world !"
        h = "7c0a529d2e9e40f54944674b0de7e806fba33262"
        self.assertEqual(sha_1.hash(text), h)

if __name__ == '__main__':
    unittest.main()
