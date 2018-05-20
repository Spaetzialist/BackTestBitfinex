import unittest
import utils


class MyTestCase(unittest.TestCase):
    def test_donchian1(self):
        h,l = utils.buildDonchian(1, [1, 2, 3], [1, 2, 3])
        self.assertEqual(h, [1, 2, 3])
        self.assertEqual(l, [1, 2, 3])

    def test_donchian2(self):
        h,l = utils.buildDonchian(2, [1, 2, 3], [1, 2, 3])
        self.assertEqual(h, [2, 3])
        self.assertEqual(l, [1, 2])

    def test_donchian5(self):
        h,l = utils.buildDonchian(3, [1, 0, 3.5, 7, 2, 3, 0], [1, 0, 3.5, 7, 2, 3, 0])
        self.assertEqual(h, [3.5,7,7,7,3])
        self.assertEqual(l, [0,0,2,2,0])

    def test_donchian3(self):
        h,l = utils.buildDonchian(2, [], [])
        self.assertEqual(h, [])
        self.assertEqual(l, [])

    def test_donchian4(self):
        h,l = utils.buildDonchian(2, [1], [1])
        self.assertEqual(h, [])
        self.assertEqual(l, [])

if __name__ == '__main__':
    unittest.main()
