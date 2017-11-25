import unittest

from src.LFSR import LFSR

class TestLFSR(unittest.TestCase):

    def test_simple(self):
        lfsr = LFSR(name="test", taps=[0, 1, 3], length=4, seed='0110')
        self.assertEqual(lfsr.shift(), '1011')
        self.assertEqual(lfsr.shift(), '0101')
        self.assertEqual(lfsr.shift(), '0010')
        self.assertEqual(lfsr.shift(), '0001')
        self.assertEqual(lfsr.shift(), '1000')
        self.assertEqual(lfsr.shift(), '1100')
        self.assertEqual(lfsr.shift(), '0110')

if __name__ == '__main__':
    unittest.main()
