import unittest

from tests.common import get_day_result


class TestSolutions2015(unittest.TestCase):
    year = 2015

    def test_y2015d01(self):
        assert get_day_result(self.year, 1) == (3, 1)

    def test_y2015d02(self):
        assert get_day_result(self.year, 2) == (58 + 43, 34 + 14)

    def test_y2015d03(self):
        assert get_day_result(self.year, 3) == (4, 3)

    def test_y2015d04(self):
        assert get_day_result(self.year, 4) == (609043, 6742839)

    def test_y2015d05(self):
        assert get_day_result(self.year, 5) == (1, 0)

    def test_y2015d06(self):
        assert get_day_result(self.year, 6) == (998996, 1001996)

    def test_y2015d07(self):
        assert get_day_result(self.year, 7) == (65079, 0)

    def test_y2015d08(self):
        assert get_day_result(self.year, 8) == (12, 19)

    def test_y2015d09(self):
        assert get_day_result(self.year, 9) == (605, 982)

    def test_y2015d10(self):
        assert get_day_result(self.year, 10) == (82350, 1166642)

    def test_y2015d11(self):
        assert get_day_result(self.year, 11) == ('abcdffaa', 'abcdffbb')

    def test_y2015d12(self):
        assert get_day_result(self.year, 12) == (15, 0)

    def test_y2015d13(self):
        assert get_day_result(self.year, 13) == (330, 286)

    def test_y2015d14(self):
        assert get_day_result(self.year, 14) == (1120, 689)

    def test_y2015d15(self):
        assert get_day_result(self.year, 15) == (62842880, 57600000)

    def test_y2015d16(self):
        assert get_day_result(self.year, 16) == (5, 4)

    def test_y2015d17(self):
        assert get_day_result(self.year, 17) == (4, 3)

    def test_y2015d18(self):
        assert get_day_result(self.year, 18) == (4, 17)

    def test_y2015d19(self):
        assert get_day_result(self.year, 19) == (7, 6)

    def test_y2015d20(self):
        assert get_day_result(self.year, 20) == (6, 6)

    def test_y2015d21(self):
        assert get_day_result(self.year, 21) == ((0, 2, 7), 0)

    def test_y2015d22(self):
        assert get_day_result(self.year, 22) == ((True, -1, 1, 9), 392)

    def test_y2015d23(self):
        assert get_day_result(self.year, 23) == (2, 7)

    def test_y2015d24(self):
        assert get_day_result(self.year, 24) == (99, 44)

    def test_y2015d25(self):
        assert get_day_result(self.year, 25) == (31663883, 0)
