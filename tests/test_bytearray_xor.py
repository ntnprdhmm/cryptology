import unittest

from src._functions import bytearray_xor

class TestBytearrayXor(unittest.TestCase):

    def test_simple(self):
        b1 = bytearray([12, 45, 32])
        b2 = bytearray([46, 32, 13])
        b3 = bytearray([34, 13, 45])
        self.assertEqual(bytearray_xor(b1, b2), b3)

if __name__ == '__main__':
    unittest.main()
