import unittest
import utils


class MyTestCase(unittest.TestCase):
    def test_donchian1(self):
        h,l = utils.buildDonchian(1, [1, 2, 3], [1, 2, 3])
        self.assertEqual(h, [1, 2, 3])
        self.assertEqual(l, [1, 2, 3])

    def test_donchian2(self):
        h,l = utils.buildDonchian(2, [1, 2, 3], [1, 2, 3])
        self.assertEqual(h, [0, 2, 3])
        self.assertEqual(l, [0, 1, 2])

    def test_donchian5(self):
        h,l = utils.buildDonchian(3, [1, 0, 3.5, 7, 2, 3, 0], [1, 0, 3.5, 7, 2, 3, 0])
        self.assertEqual(h, [0,0,3.5,7,7,7,3])
        self.assertEqual(l, [0,0,0,0,2,2,0])

    def test_donchian3(self):
        h,l = utils.buildDonchian(2, [], [])
        self.assertEqual(h, [])
        self.assertEqual(l, [])

    def test_donchian4(self):
        h,l = utils.buildDonchian(2, [1], [1])
        self.assertEqual(h, [0])
        self.assertEqual(l, [0])

    def test_stopLow1(self):
        donchianLowStop = [1]
        index = 0
        stopdays = 3
        timebase = 1440
        e = utils.setStopLow(donchianLowStop, index, stopdays, timebase)
        self.assertEqual(e,-1)

    def test_stopLow2(self):
        donchianLowStop = [1]
        index = 5
        stopdays = 1
        timebase = 1
        e = utils.setStopLow(donchianLowStop, index, stopdays, timebase)
        self.assertEqual(e,-1)

    def test_stopLow3(self):
        donchianLowStop = [1,1,2,2,3,3]
        index = 2
        stopdays = 1
        timebase = 1
        e = utils.setStopLow(donchianLowStop, index, stopdays, timebase)
        self.assertEqual(e,1)

    def test_stopLow4(self):
        donchianLowStop = [1,1,2,2,3,3]
        index = 3
        stopdays = 1
        timebase = 1
        e = utils.setStopLow(donchianLowStop, index, stopdays, timebase)
        self.assertEqual(e,2)

    def test_stopLow5(self):
        donchianLowStop = [1,1,2,2,3,3]
        index = 5
        stopdays = 2
        timebase = 2
        e = utils.setStopLow(donchianLowStop, index, stopdays, timebase)
        self.assertEqual(e,1)

    def test_stopLow6(self):
        donchianLowStop = [1,1,2,2,3,3,2,2,1,1,2,2,3,3]
        index = 5
        stopdays = 2
        timebase = 3
        e = utils.setStopLow(donchianLowStop, index, stopdays, timebase)
        self.assertEqual(e,-1)

    def test_stopLow7(self):
        donchianLowStop = [1,1,2 ,2,3,3, 2,2,4, 1,2,2, 3,3]
        index = 8
        stopdays = 2
        timebase = 3
        e = utils.setStopLow(donchianLowStop, index, stopdays, timebase)
        self.assertEqual(e,1)

    def test_stopLow8(self):
        donchianLowStop = [1,1,2 ,2,3,3, 2,2,4, 1,2,2, 3,3]
        index = 9
        stopdays = 2
        timebase = 3
        e = utils.setStopLow(donchianLowStop, index, stopdays, timebase)
        self.assertEqual(e,2)

    def test_stopLow9(self):
        donchianLowStop = [1,1,2 ,2,3,3, 2,2,4, 1,2,2, 3,3]
        index = 13
        stopdays = 2
        timebase = 3
        e = utils.setStopLow(donchianLowStop, index, stopdays, timebase)
        self.assertEqual(e,1)

    def test_stopLow10(self):
        donchianLowStop = [1,1,2 ,2,3,3, 2,2,4, 1,2,2, 3,3]
        index = 10
        stopdays = 2
        timebase = 3
        e = utils.setStopLow(donchianLowStop, index, stopdays, timebase)
        self.assertEqual(e,2)

if __name__ == '__main__':
    unittest.main()
